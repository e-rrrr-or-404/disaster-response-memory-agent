import os
import uuid
import json

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition, MatchValue

from sentence_transformers import SentenceTransformer
import torch
import clip
from PIL import Image

# -----------------------
# Load models
# -----------------------
print("Loading models...")

text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

print("Models loaded")

# -----------------------
# Embedding functions
# -----------------------
def get_text_embedding(text: str):
    return text_model.encode(text).tolist()

def get_image_embedding(image_path: str):
    image = Image.open(image_path).convert("RGB")
    image_input = clip_preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()[0].tolist()

# -----------------------
# Connect to Qdrant
# -----------------------
client = QdrantClient(url="http://localhost:6333")
print("Connected to Qdrant")

# -----------------------
# Create collection (clean)
# -----------------------
if client.collection_exists("disasters"):
    client.delete_collection("disasters")

client.create_collection(
    collection_name="disasters",
    vectors_config={
        "text_vector": VectorParams(size=384, distance=Distance.COSINE),
        "image_vector": VectorParams(size=512, distance=Distance.COSINE),
    }
)

print("Collection created")

# -----------------------
# Batch ingest all disasters
# -----------------------
BASE_DIR = "data"
folders = ["floods", "fires", "cyclones"]

points = []

for folder in folders:
    folder_path = os.path.join(BASE_DIR, folder)

    for file in os.listdir(folder_path):
        if not file.endswith(".txt"):
            continue

        base_name = file.replace(".txt", "")

        text_path = os.path.join(folder_path, base_name + ".txt")
        image_path = os.path.join(folder_path, base_name + ".jpg")
        json_path = os.path.join(folder_path, base_name + ".json")

        if not (os.path.exists(image_path) and os.path.exists(json_path)):
            continue

        with open(text_path, "r") as f:
            report_text = f.read()

        with open(json_path, "r") as f:
            metadata = json.load(f)

        text_vector = get_text_embedding(report_text)
        image_vector = get_image_embedding(image_path)

        points.append({
            "id": str(uuid.uuid4()),
            "vector": {
                "text_vector": text_vector,
                "image_vector": image_vector
            },
            "payload": metadata
        })

client.upsert(collection_name="disasters", points=points)
print(f"Ingested {len(points)} disaster events")

# -----------------------
# TEXT SEARCH TEST
# -----------------------
print("\nTEXT SEARCH TEST")

text_hits = client.query_points(
    collection_name="disasters",
    query=get_text_embedding("severe flooding and evacuations"),
    using="text_vector",
    limit=3
)

for p in text_hits.points:
    print(p.payload, p.score)

# -----------------------
# IMAGE SEARCH TEST
# -----------------------
print("\nIMAGE SEARCH TEST")

test_image = "data/floods/flood_01.jpg"
image_query = get_image_embedding(test_image)

image_hits = client.query_points(
    collection_name="disasters",
    query=image_query,
    using="image_vector",
    limit=3
)

for p in image_hits.points:
    print(p.payload, p.score)

# -----------------------
# METADATA FILTER TEST
# -----------------------
print("\nMETADATA FILTER TEST (floods only)")

flood_filter = Filter(
    must=[
        FieldCondition(
            key="disaster_type",
            match=MatchValue(value="flood")
        )
    ]
)

filtered_hits = client.query_points(
    collection_name="disasters",
    query=get_text_embedding("river overflow"),
    using="text_vector",
    query_filter=flood_filter,
    limit=5
)

for p in filtered_hits.points:
    print(p.payload, p.score)
