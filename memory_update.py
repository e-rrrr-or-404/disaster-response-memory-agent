
# Qdrant client import
# + payload update karne ke liye

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import random


# Qdrant connection
# Local Qdrant instance se connect

client = QdrantClient(url="http://localhost:6333")

print("Connected to Qdrant")

# memory fields
# Har disaster ke saath response, outcome, confidence,
# + failure-related memory attach karna

print("Updating disasters with memory fields...")

DISASTER_TYPES = ["flood", "wildfire", "cyclone"]

for disaster_type in DISASTER_TYPES:

    # current disaster type ke points nikaalne ka filter
    disaster_filter = Filter(
        must=[FieldCondition(
            key="disaster_type",
            match=MatchValue(value=disaster_type)
        )]
    )

    # Qdrant se matching disasters scroll
    # scroll is used kyunki multiple points update karne hain
    results = client.scroll(
        collection_name="disasters",
        scroll_filter=disaster_filter,
        limit=100
    )[0]

    # Har disaster memory ko update

    for point in results:

        # Disaster-type specific response randomly assign
        # (Simulation purpose ke liye)
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

        # Outcome simulate
        outcome = random.choice([
            "reduced casualties",
            "moderate damage",
            "response delayed"
        ])

        # Outcome ke basis pe confidence assign
        confidence = {
            "reduced casualties": 0.9,
            "moderate damage": 0.7,
            "response delayed": 0.4
        }[outcome]

        # Existing payload ko copy
        payload = point.payload.copy()

        # Default: koi failure nahi
        failed_response = None
        failure_reason = None

        # Agar response delayed hua → negative memory mark
        if outcome == "response delayed":
            failed_response = response_used
            failure_reason = "delayed or insufficient response"

        # Payload me memory-related fields add/update
        payload.update({
            "response_used": response_used,
            "outcome": outcome,
            "confidence": confidence,
            "response_failed": failed_response,
            "failure_reason": failure_reason
        })

        # Qdrant me payload update kar rahe hain
        client.set_payload(
            collection_name="disasters",
            payload=payload,
            points=[point.id]
        )

# (legacy block)
# Flood-type disasters ke liye ek update pass
# Ye block essentially reinforcement simulation karta hai
# ----------------------------------------
results = client.scroll(
    collection_name="disasters",
    scroll_filter=disaster_filter,
    limit=100
)[0]

for point in results:

    # Response dubara simulate kar rahe hain
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

    # Existing payload update
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
