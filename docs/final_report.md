# Disaster Response Memory Agent using Qdrant

## 1. Problem Statement
Disaster response requires learning from past events across diverse data modalities such as satellite imagery and textual reports. However, many existing AI systems focus on generating responses rather than maintaining long-term, evolving memory. This limits their ability to support evidence-based decision-making in high-stakes societal contexts.

This system is designed for district-level disaster response planners (DDMA), who must make rapid decisions using incomplete and fragmented historical information during the early hours of a disaster.

## 2. System Design
We present a Disaster Response Memory Agent that uses Qdrant as a multimodal vector database to store and retrieve historical disaster events. Each disaster is modeled as a memory entity with independent text and image embeddings and an evolving payload capturing response outcomes and reliability.

## 3. Multimodal Strategy
Textual disaster reports are embedded using MiniLM, while satellite images are embedded using CLIP. These embeddings are stored in separate vector fields to preserve modality integrity. Queries can be text-based or image-based and are combined with metadata filtering to ensure contextual relevance.

## 4. Memory Logic
Unlike static retrieval systems, disaster memories evolve over time. Payload updates record which responses were used, which failed, and how effective they were. Confidence scores are reinforced or weakened based on observed outcomes, and older events are downweighted using time-based decay. The system also surfaces disagreement between historical responses rather than collapsing them into a single answer. All retrieved disasters, similarity scores, and outcome reliabilities can be logged and reviewed post-incident to support institutional learning and after-action audits.

### Memory Absence Handling

If no sufficiently similar historical disasters exist above a similarity threshold, the system explicitly reports low memory confidence instead of extrapolating recommendations. In such cases, it defers to human judgment and highlights the lack of precedent.

Example output:

No strong historical precedent found.  
Outcome reliability is low.  
Human judgment required.


## 5. Ethics and Limitations
The system is designed as a decision-support tool and does not automate authority. It avoids personal data, exposes uncertainty, and provides transparent evidence traces. Limitations include dependence on historical data coverage and the need for human oversight in real-world deployments.

## Conclusion
By combining multimodal retrieval, long-term memory evolution, and evidence-grounded reasoning, this system demonstrates how vector databases like Qdrant can support responsible, transparent AI for societal impact.
