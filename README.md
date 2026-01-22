# Disaster Response Memory Agent

A multimodal disaster response decision-support system designed for **district-level disaster response planners (DDMA)**.  
The system retrieves, remembers, and reasons over historical disasters using **Qdrant** as a long-term vector memory.

---

## Problem Context

District Disaster Management Authorities (DDMAs) must make rapid decisions during the early hours of a disaster using incomplete and fragmented historical information. This system supports those decisions by surfacing historically similar disasters, response strategies, and observed outcomes with explicit evidence.

---

## Key Capabilities

- Multimodal retrieval over **text reports and satellite imagery**
- Long-term disaster memory with:
  - Outcome reinforcement
  - Time-based decay
  - Explicit failure tracking
- Disagreement-aware recommendations
- Evidence-based reasoning with traceable historical context

---

## System Architecture

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/c42cf797-05f6-4ee2-9ff9-9a5c3b634694" />

---

## Tech Stack

- Vector Database: **Qdrant**
- Text Embeddings: sentence-transformers (MiniLM)
- Image Embeddings: CLIP (ViT-B/32)
- Language: Python 3.9+

---

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Qdrant (Docker)

keep terminal running 

```bash
docker run -p 6333:6333 qdrant/qdrant
```
OPEN NEW TERMINAL

### 3. Ingest disaster data
```bash
python ingest_all.py
```

### 4. Run memory update
```bash
python memory_update.py
```

### 5. Run memory reinforcement
```bash
python memory_reinforce.py
```

### 6. Run recommendation demo
```bash
python recommend.py
```

## Visualizations

Use the Qdrant dashboard at:
```bash
http://localhost:6333/dashboard
```

Recommended visualization:

## UMAP projection of text_vector
Colored by disaster_type
```bash
{
  "limit": 300,
  "using": "text_vector",
  "algorithm": "UMAP",
  "color_by": {
    "payload": "disaster_type"
  }
}

```
## UMAP projection of image_vector
Colored by disaster_type
```bash
{
  "limit": 200,
  "using": "image_vector",
  "algorithm": "UMAP",
  "color_by": {
    "payload": "disaster_type"
  }
}

```


## Ethics & Limitations

This system is designed strictly for decision support. It does not automate authority or replace human judgment.

See docs/ethics_and_limitations.md for details.

## Documentation

Detailed documentation is available in the docs/ folder:

- Architecture

- Demo script

- Ethics & limitations

