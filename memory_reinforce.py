from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
# Qdrant connection
client = QdrantClient(url="http://localhost:6333")
print("Connected to Qdrant")

DISASTER_TYPES = ["flood", "wildfire", "cyclone"]

# Reinforcement rules
# Confidence ko kitna badhaana / ghataana hai

POSITIVE_OUTCOME_BOOST = 0.2     # agar outcome acha tha → confidence increase
NEGATIVE_OUTCOME_PENALTY = 0.3   # agar response delay hua → confidence decrease
MAX_CONFIDENCE = 1.0              # confidence upper bound
MIN_CONFIDENCE = 0.1              # confidence lower bound

# Har disaster type ke liye loop
# post-incident review jaisa behave

for disaster_type in DISASTER_TYPES:

    print(f"\nReinforcing memories for: {disaster_type}")

    # current disaster type ke points nikaalne ke liye filter
    disaster_filter = Filter(
        must=[
            FieldCondition(
                key="disaster_type",
                match=MatchValue(value=disaster_type)
            )
        ]
    )

    # Qdrant se matching disasters scroll
    points = client.scroll(
        collection_name="disasters",
        scroll_filter=disaster_filter,
        limit=100
    )[0]

    for point in points:
        payload = point.payload

        outcome = payload.get("outcome")
        confidence = payload.get("confidence")

        # Agar memory incomplete hai (missing fields),
        # toh usko skip kar do
        if confidence is None or outcome is None:
            continue

        
        # Positive reinforcement
        if outcome == "reduced casualties":
            payload["confidence"] = min(
                confidence + POSITIVE_OUTCOME_BOOST,
                MAX_CONFIDENCE   # confidence 1.0 se upar nahi
            )

        
        # Negative reinforcement
        elif outcome == "response delayed":
            payload["confidence"] = max(
                confidence - NEGATIVE_OUTCOME_PENALTY,
                MIN_CONFIDENCE   # confidence zero tak collapse nahi
            )

        # Moderate outcome (na bahut acha, na bahut kharab)
        # Is case me confidence change nahi karte
        else:
            continue


        # Updated confidence ko Qdrant me save karo
        # Isse disaster memory time ke saath evolve hoti hai

        client.set_payload(
            collection_name="disasters",
            payload=payload,
            points=[point.id]
        )

    print(f"Memory reinforcement complete for: {disaster_type}")

print("\nAll disaster memories updated successfully")
