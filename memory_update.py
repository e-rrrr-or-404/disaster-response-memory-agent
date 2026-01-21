from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import random

client = QdrantClient(url="http://localhost:6333")

print("Connected to Qdrant")

# -----------------------------
# STEP 6: Add memory fields
# -----------------------------
print("Updating disasters with memory fields...")

#flood_filter = Filter(
#    must=[FieldCondition(key="disaster_type", match=MatchValue(value="flood"))]
#) 

DISASTER_TYPES = ["flood", "wildfire", "cyclone"]

for disaster_type in DISASTER_TYPES:
    disaster_filter = Filter(
        must=[FieldCondition(key="disaster_type", match=MatchValue(value=disaster_type))]
    )

    results = client.scroll(
        collection_name="disasters",
        scroll_filter=disaster_filter,
        limit=100
    )[0]

    for point in results:
        response_used = random.choice({
            "flood": [
                "early warning + evacuation",
                "evacuation + relief camps",
                "local response only"
            ],
            "wildfire": [
                "firebreaks",
                "aerial suppression",
                "evacuation"
            ],
            "cyclone": [
                "early warning",
                "coastal evacuation",
                "shelter activation"
            ]
        }[disaster_type])

        outcome = random.choice([
            "reduced casualties",
            "moderate damage",
            "response delayed"
        ])

        confidence = {
            "reduced casualties": 0.9,
            "moderate damage": 0.7,
            "response delayed": 0.4
        }[outcome]

        payload = point.payload.copy()
        failed_response = None
        failure_reason = None

        if outcome == "response delayed":
            failed_response = response_used
            failure_reason = "delayed or insufficient response"

        payload.update({
            "response_used": response_used,
            "outcome": outcome,
            "confidence": confidence,
            "response_failed": failed_response,
            "failure_reason": failure_reason
        })

        client.set_payload(
            collection_name="disasters",
            payload=payload,
            points=[point.id]
        )


results = client.scroll(
    collection_name="disasters",
    scroll_filter=disaster_filter,
    limit=100
)[0]

for point in results:
    # Simulate response effectiveness
    response_used = random.choice([
        "evacuation + relief camps",
        "early warning + evacuation",
        "local response only"
    ])

    outcome = random.choice([
        "reduced casualties",
        "moderate damage",
        "response delayed"
    ])

    confidence = {
        "reduced casualties": 0.9,
        "moderate damage": 0.7,
        "response delayed": 0.4
    }[outcome]

    new_payload = point.payload.copy()
    new_payload.update({
        "response_used": response_used,
        "outcome": outcome,
        "confidence": confidence
    })

    client.set_payload(
        collection_name="disasters",
        payload=new_payload,
        points=[point.id]
    )

print("Memory fields added to all disasters")
