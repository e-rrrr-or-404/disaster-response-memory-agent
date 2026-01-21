import uuid
import json

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from sentence_transformers import SentenceTransformer
import torch
import clip
from PIL import Image
# ---- Load text model ----
print("Loading text model...")
text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---- Load image model ----
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
print("Models loaded")

def get_text_embedding(text: str):
    return text_model.encode(text).tolist()


def get_image_embedding(image_path: str):
    image = Image.open(image_path).convert("RGB")
    image_input = clip_preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()[0].tolist()

print("Connecting to Qdrant...")
client = QdrantClient(url="http://localhost:6333")
print("Connected")

print("Creating collection...")

client.recreate_collection(
    collection_name="disasters",
    vectors_config={
        "text_vector": VectorParams(
            size=384,
            distance=Distance.COSINE
        ),
        "image_vector": VectorParams(
            size=512,
            distance=Distance.COSINE
        )
    }
)

print("Collection created")

text_path = "data/floods/flood_01.txt"
image_path = "data/floods/flood_01.jpg"
json_path = "data/floods/flood_01.json"

with open(text_path, "r") as f:
    report_text = f.read()

with open(json_path, "r") as f:
    metadata = json.load(f)

print("Creating embeddings...")
text_embedding = get_text_embedding(report_text)
image_embedding = get_image_embedding(image_path)

print("Uploading point...")

client.upsert(
    collection_name="disasters",
    points=[
        {
            "id": str(uuid.uuid4()),
            "vector": {
                "text_vector": text_embedding,
                "image_vector": image_embedding
            },
            "payload": metadata
        }
    ]
)

print("Upload complete")

print("Running sanity search...")

hits = client.query_points(
    collection_name="disasters",
    query=get_text_embedding("severe flooding and evacuations"),
    using="text_vector",
    limit=3
)

for point in hits.points:
    print(point.payload, point.score)
