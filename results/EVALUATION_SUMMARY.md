# AdvSOC Evaluation Summary — v0.5

## Evaluation Set
24 curated SOC alert cases:

- 4 benign/informational
- 4 suspicious authentication
- 4 malicious network/C2
- 3 phishing
- 3 malware
- 3 reconnaissance
- 3 unknown/ambiguous

## Degraded-Mode Baseline

| Metric | Result |
|---|---:|
| Category accuracy | 83.3% |
| Severity accuracy | 41.7% |
| Policy accuracy | 70.8% |
| Slack-routing accuracy | 66.7% |
| Full-case pass rate | 33.3% |

The AI classifier was unavailable during this baseline because of a prompt configuration issue, so this primarily represents deterministic/fallback behavior.

## Hybrid Baseline

After restoring the AI classifier:

| Metric | Result |
|---|---:|
| Category accuracy | 91.7% |
| Severity accuracy | 41.7% |
| Policy accuracy | 75.0% |
| Slack-routing accuracy | 66.7% |
| Full-case pass rate | 37.5% |

## Post-Fix Evaluation

After improving authentication evidence extraction, negation handling, malware evidence distinction, evidence-based severity floors, and unknown-event handling:

| Metric | Result |
|---|---:|
| Category accuracy | 100% |
| Severity accuracy | 100% |
| Policy accuracy | 100% |
| Slack-routing accuracy | 100% |
| Full-case pass rate | 100% |

## Interpretation

The final result represents performance on this 24-case curated development/evaluation set. It should not be interpreted as evidence of universal or production-level accuracy.

Future evaluation should include larger held-out datasets, adversarial alerts, service failures, malformed inputs, and broader threat-intelligence conditions.
