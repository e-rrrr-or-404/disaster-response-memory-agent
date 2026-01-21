from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient(url="http://localhost:6333")

print("Connected to Qdrant")

flood_filter = Filter(
    must=[FieldCondition(key="disaster_type", match=MatchValue(value="flood"))]
)

points = client.scroll(
    collection_name="disasters",
    scroll_filter=flood_filter,
    limit=100
)[0]

for p in points:
    payload = p.payload

    if payload.get("outcome") == "reduced casualties":
        payload["confidence"] = min(payload["confidence"] + 0.05, 1.0)

    elif payload.get("outcome") == "response delayed":
        payload["confidence"] = max(payload["confidence"] - 0.1, 0.1)

    client.set_payload(
        collection_name="disasters",
        payload=payload,
        points=[p.id]
    )

print("Memory reinforcement complete")
