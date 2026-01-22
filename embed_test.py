from sentence_transformers import SentenceTransformer

# ----------------------------------------
# Text embedding model load
# Disaster reports ke liye text embeddings
# ----------------------------------------
print("Loading text embedding model...")
text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Text model loaded")

import torch
import clip
from PIL import Image

# Device selection
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# CLIP image embedding model load
# Satellite images ke liye
print("Loading CLIP image model...")
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
print("Image model loaded")

# TEST: Embedding dimensions check

sample_text = "Severe flooding caused evacuations and infrastructure damage."

# Text → embedding
text_embedding = text_model.encode(sample_text)
print("Text embedding dimension:", len(text_embedding))

# Image → embedding
# Kisi bhi disaster image se test kar sakte ho
image = Image.open("data/floods/flood_01.jpg").convert("RGB")
image_input = clip_preprocess(image).unsqueeze(0).to(device)

with torch.no_grad():
    image_embedding = clip_model.encode_image(image_input)

print("Image embedding dimension:", image_embedding.shape[1])


# Reusable embedding helper functions

def get_text_embedding(text: str):
    # Text ko list me convert kar rahe hain
    # Qdrant ko list format chahiye
    embedding = text_model.encode(text)
    return embedding.tolist()

def get_image_embedding(image_path: str):
    # Image load + preprocess
    image = Image.open(image_path).convert("RGB")
    image_input = clip_preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)

    # Cosine similarity ke liye normalize
    image_features /= image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()[0].tolist()

# Final check
print(
    "Text embedding length:",
    len(get_text_embedding("Test flood report"))
)

print(
    "Image embedding length:",
    len(get_image_embedding("data/floods/flood_01.jpg"))
)
