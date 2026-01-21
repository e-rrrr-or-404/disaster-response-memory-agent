\# Disaster Response Memory Agent



A multimodal disaster response decision-support system designed for \*\*district-level disaster response planners (DDMA)\*\*.  

The system retrieves, remembers, and reasons over historical disasters using \*\*Qdrant\*\* as a long-term vector memory.



---



\## Problem Context



District Disaster Management Authorities (DDMAs) must make rapid decisions during the early hours of a disaster using incomplete and fragmented historical information. This system supports those decisions by surfacing historically similar disasters, response strategies, and observed outcomes with explicit evidence.



---



\## Key Capabilities



\- Multimodal retrieval over \*\*text reports and satellite imagery\*\*

\- Long-term disaster memory with:

&nbsp; - Outcome reinforcement

&nbsp; - Time-based decay

&nbsp; - Explicit failure tracking

\- Disagreement-aware recommendations

\- Evidence-based reasoning with traceable historical context



---



\## System Architecture



User Scenario

↓

Embedding Models (MiniLM + CLIP)

↓

Qdrant Vector Database

(Text + Image Vectors + Metadata)

↓

Retriever

↓

Memory \& Reasoning Layer

↓

Historical Response Summary + Evidence Trace





---



\## Tech Stack



\- Vector Database: \*\*Qdrant\*\*

\- Text Embeddings: sentence-transformers (MiniLM)

\- Image Embeddings: CLIP (ViT-B/32)

\- Language: Python 3.9+



---



\## Setup Instructions



\### 1. Install dependencies

```bash

pip install -r requirements.txt



2\. Start Qdrant (Docker)



docker run -p 6333:6333 qdrant/qdrant



3\. Ingest disaster data



python ingest\_all.py



4\. Run recommendation demo



python recommend.py



Visualizations



Use the Qdrant dashboard at:



http://localhost:6333/dashboard



Recommended visualization:



&nbsp;   UMAP projection of text\_vector



&nbsp;   Colored by disaster\_type



Ethics \& Limitations



This system is designed strictly for decision support. It does not automate authority or replace human judgment.

See docs/ethics\_and\_limitations.md for details.



Documentation



Detailed documentation is available in the docs/ folder:



&nbsp;   Architecture



&nbsp;   Memory logic



&nbsp;   Demo script



&nbsp;   Ethics \& limitations





