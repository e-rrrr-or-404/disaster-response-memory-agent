# Disaster-specific domain knowledge
# Har disaster type ke valid response options define
DISASTER_PROFILES = {
    "flood": {
        "responses": [
            "early warning + evacuation",
            "evacuation + relief camps",
            "local response only"
        ]
    },
    "wildfire": {
        "responses": [
            "firebreaks",
            "aerial suppression",
            "evacuation"
        ]
    },
    "cyclone": {
        "responses": [
            "early warning",
            "coastal evacuation",
            "shelter activation"
        ]
    }
}
# Required imports
# Qdrant: vector search + memory
# SentenceTransformer: text embeddings
# math + datetime: time decay logic
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import math
from datetime import datetime

# Time decay logic
# Purane disasters ko automatically kam weight dene ke liye
# Idea: jitna purana event, utna kam trust

CURRENT_YEAR = datetime.now().year

def apply_time_decay(confidence, event_year):
    age = CURRENT_YEAR - event_year
    return confidence * math.exp(-age / 5)

# System setup
# Qdrant se connect
# Text embedding model load

client = QdrantClient(url="http://localhost:6333")
text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("System ready")

# Explicit demo scenario
# consciously ek disaster type fix
# Demo ke time bas isko flood / wildfire / cyclone me switch

disaster_type = "wildfire"   # change to flood / cyclone for demo
query = "A wildfire is spreading near forested regions. What should responders do?"

# Query ko vector me convert
query_vector = text_model.encode(query).tolist()

# relevant disaster type ke memories retrieve karne ke liye filter
disaster_filter = Filter(
    must=[FieldCondition(key="disaster_type", match=MatchValue(value=disaster_type))]
)

# Qdrant retrieval
# Text vector ke through similar past disasters

hits = client.query_points(
    collection_name="disasters",
    query=query_vector,
    using="text_vector",
    query_filter=disaster_filter,
    limit=5
)

# Retrieval + memory-aware filtering

print("\nRetrieved similar disasters:")

# response_scores:
# key   → response strategy
# value → list of decayed confidence scores
response_scores = {}

for h in hits.points:
    payload = h.payload
    response = payload.get("response_used")
    failed = payload.get("response_failed")

    # Domain validity check
    # Galat disaster ke response ko ignore
    if response not in DISASTER_PROFILES[disaster_type]["responses"]:
        continue

    # Negative memory handling
    # Agar historically ye response fail hua hai → skip
    if response == failed:
        continue

    # Time decay apply
    raw_confidence = payload.get("confidence")
    decayed_confidence = apply_time_decay(raw_confidence, payload["year"])

    # Response-wise confidence collect
    response_scores.setdefault(response, []).append(decayed_confidence)

    # Transparent logging — dikhane ke liye
    print(
        f"- {payload['location']} {payload['year']} | "
        f"response={response} | "
        f"outcome_reliability={round(decayed_confidence, 2)} | "
        f"similarity={round(h.score, 2)}"
    )

# Disagreement-aware summary
# Single answer dene ke bajay trade-offs dikhate hain

print("\nHISTORICAL RESPONSE SUMMARY:")

for response, scores in response_scores.items():
    avg_conf = sum(scores) / len(scores)
    print(
        f"- {response} "
        f"(outcome reliability: {round(avg_conf, 2)})"
    )

# reliable response choose kar rahe hain (average basis pe)
recommended_response = max(
    response_scores.items(),
    key=lambda x: sum(x[1]) / len(x[1])
)[0]

print(f"\nMost historically reliable response: {recommended_response}")
print(f"Based on historical {disaster_type} outcomes")

# Real-world constraint
print("\nOperational note:")
print(
    "Evacuation has historically reduced casualties "
    "but requires transport availability and sufficient early warning lead time."
)

# Evidence trace
# Ye section auditability dikhata hai
# Kaunse past disasters ne decision influence kiya

print("\nEVIDENCE TRACE:")
for h in hits.points:
    print(
        f"- {h.payload['disaster_type'].title()} | "
        f"{h.payload['location']} {h.payload['year']} | "
        f"similarity={round(h.score, 2)}"
    )
