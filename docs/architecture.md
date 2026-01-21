# System Architecture

## Overview

The Disaster Response Memory Agent is designed as a long-term institutional memory system rather than a conventional question-answering AI. It retrieves and reasons over historical disaster events using multimodal embeddings and explicit memory updates.

## High-Level Flow

User Scenario (Text or Image)
↓
Embedding Models
(Text → MiniLM | Image → CLIP)
↓
Qdrant Vector Database
(Text Vectors + Image Vectors + Metadata)
↓
Retriever
(Semantic Similarity + Metadata Filtering)
↓
Memory & Reasoning Layer
(Outcome Reinforcement, Failure Penalties, Time Decay)
↓
Historical Response Summary
(Trade-offs, Reliability Scores)
↓
Evidence Trace
(Referenced Past Disasters)


## Key Design Decisions

### Multimodal Separation
Text and image embeddings are stored in separate vector fields within Qdrant. This prevents semantic interference and allows modality-specific queries.

### Disaster as Memory Entity
Each disaster is treated as a memory that evolves over time. Payload updates record:
- Response strategies used
- Observed outcomes
- Confidence and reliability scores
- Explicit failure cases

### Explainability by Design
All recommendations are grounded in retrieved historical events. The system exposes similarity scores and payload metadata to ensure traceability and auditability.

### Extensibility
The architecture uses a single reasoning pipeline parameterized by disaster type, allowing extension to new hazards without redesign or retraining.