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

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import math
from datetime import datetime

# -------------------------
# Time decay logic
# -------------------------
CURRENT_YEAR = datetime.now().year

def apply_time_decay(confidence, event_year):
    age = CURRENT_YEAR - event_year
    return confidence * math.exp(-age / 5)

# -------------------------
# Setup
# -------------------------
client = QdrantClient(url="http://localhost:6333")
text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("System ready")

# -------------------------
# Explicit scenario setup
# -------------------------
disaster_type = "wildfire"   # change to flood / cyclone for demo
query = "A wildfire is spreading near forested regions. What should responders do?"

query_vector = text_model.encode(query).tolist()

disaster_filter = Filter(
    must=[FieldCondition(key="disaster_type", match=MatchValue(value=disaster_type))]
)

hits = client.query_points(
    collection_name="disasters",
    query=query_vector,
    using="text_vector",
    query_filter=disaster_filter,
    limit=5
)

# -------------------------
# Retrieval + filtering
# -------------------------
print("\nRetrieved similar disasters:")

response_scores = {}   # 🔑 response → list of decayed confidences

for h in hits.points:
    payload = h.payload
    response = payload.get("response_used")
    failed = payload.get("response_failed")

    # 1️⃣ Domain validity
    if response not in DISASTER_PROFILES[disaster_type]["responses"]:
        continue

    # 2️⃣ Negative memory: skip failed responses
    if response == failed:
        continue

    raw_confidence = payload.get("confidence")
    decayed_confidence = apply_time_decay(raw_confidence, payload["year"])

    response_scores.setdefault(response, []).append(decayed_confidence)

    print(
        f"- {payload['location']} {payload['year']} | "
        f"response={response} | "
        f"outcome_reliability={round(decayed_confidence, 2)} | "
        f"similarity={round(h.score, 2)}"
    )

# -------------------------
# 🥉 Disagreement-aware summary
# -------------------------
print("\nHISTORICAL RESPONSE SUMMARY:")

for response, scores in response_scores.items():
    avg_conf = sum(scores) / len(scores)
    print(
        f"- {response} "
        f"(outcome reliability: {round(avg_conf, 2)})"
    )

# Choose the most historically reliable response
recommended_response = max(
    response_scores.items(),
    key=lambda x: sum(x[1]) / len(x[1])
)[0]

print(f"\nMost historically reliable response: {recommended_response}")
print(f"Based on historical {disaster_type} outcomes")

print("\nOperational note:")
print("Evacuation has historically reduced casualties but requires transport availability and sufficient early warning lead time.")


# -------------------------
# Evidence trace
# -------------------------
print("\nEVIDENCE TRACE:")
for h in hits.points:
    print(
        f"- {h.payload['disaster_type'].title()} | "
        f"{h.payload['location']} {h.payload['year']} | "
        f"similarity={round(h.score, 2)}"
    )
