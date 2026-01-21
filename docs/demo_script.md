# Demo Script

This demo is structured as a realistic decision-support walkthrough rather than a technical showcase.

---

## Demo 1: Flood Scenario (Text-Based)

**Scenario**
A report arrives indicating heavy rainfall and rising river levels in Assam.

**Query**
"Heavy flooding reported in Assam. What should responders do?"

**What the System Shows**
- Retrieval of historically similar flood events
- Display of response strategies and outcome reliability
- Penalization of historically failed responses
- Time-aware weighting of recent disasters

**Key Output**
- Early warning and evacuation emerges as the most historically reliable response

**Evidence Trace**
- Flood Assam 2022
- Flood Bihar 2021
- Flood Kerala 2019

---

## Demo 2: Wildfire Scenario

**Scenario**
A wildfire is spreading near forested regions under dry and windy conditions.

**Query**
"A wildfire is spreading near forested regions. What should responders do?"

**What the System Shows**
- Retrieval of wildfire-specific historical events
- Comparison between firebreaks, aerial suppression, and evacuation
- Display of disagreement and trade-offs between strategies

**Key Insight**
- Firebreaks show higher reliability, while aerial suppression has mixed outcomes

- In this wildfire scenario, textual situation reports were sparse and delayed, but satellite imagery alone was sufficient to retrieve historically similar wildfire events.


---

## Demo 3: Cyclone Scenario (Location-Aware)

**Scenario**
A cyclone is approaching a populated coastline.

**Query**
"A cyclone is approaching the coastline. What should responders do?"

**What the System Shows**
- Retrieval of past cyclone events
- Emphasis on early warning and shelter activation
- Clear evidence linking outcomes to prior evacuations

---

## Closing Message to Judges

"This system does not generate advice from scratch. It remembers how past responses actually performed and summarizes that institutional knowledge with evidence."
