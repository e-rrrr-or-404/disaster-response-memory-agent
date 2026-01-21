# Ethics, Responsibility, and Limitations

## Decision-Support, Not Automation
This system is designed strictly as a decision-support tool for disaster response planning. It does not issue commands, trigger automated actions, or replace human authority. All outputs are intended to support trained responders and policymakers, who retain full responsibility for decisions and actions.

## Privacy and Data Protection
The system does not store, process, or infer any personally identifiable information. All inputs consist of:
- Public or synthetic satellite imagery
- High-level textual disaster reports
- Aggregated metadata such as location, year, and disaster type

No individual-level data is collected or inferred.

## Uncertainty and Transparency
Disaster response involves inherent uncertainty. Rather than hiding this uncertainty, the system explicitly exposes:
- Outcome reliability scores derived from historical performance
- Multiple response strategies when historical evidence disagrees
- Evidence traces showing which past events influenced recommendations

This prevents overconfident or opaque outputs.

## Bias and Data Coverage
The system’s effectiveness depends on the diversity and representativeness of historical disaster data. Regions or disaster types with limited historical records may yield weaker or less certain recommendations. The system does not claim universal applicability and should be used alongside local expertise.

### Climate Novelty Limitation

The system may underperform for novel disaster patterns driven by climate change where historical analogs are weak, misleading, or absent. In such cases, the system prioritizes transparency over confidence and explicitly signals uncertainty.


## Temporal Relevance
Older disaster events are downweighted using time-based decay to reflect changing infrastructure, climate patterns, and response capabilities. This mitigates the risk of outdated practices dominating recommendations.

## Misuse Prevention
To reduce the risk of misuse:
- The system avoids real-time operational control
- It does not optimize for speed over safety
- It emphasizes historical evidence rather than predictive authority

In real-world deployments, additional safeguards such as human review, auditing, and continuous data validation would be required.
