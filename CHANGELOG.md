# Changelog

All notable development milestones for AdvSOC are documented here.

## v1.0.0

### Added

- End-to-end n8n SOC alert-processing workflow.
- Webhook-based alert ingestion.
- Alert normalization and required-field validation.
- Structured HTTP 400 responses for invalid alerts.
- IoC extraction for:
  - IPv4 addresses
  - domains
  - URLs
  - MD5
  - SHA-1
  - SHA-256
- Deterministic security rule engine.
- Primary-IoC selection using:
  - file hash
  - URL
  - domain
  - IP
- VirusTotal threat-intelligence enrichment.
- LLM-assisted SOC classification.
- Structured AI output validation.
- Deterministic fallback when AI classification fails.
- 0-100 hybrid risk-scoring system.
- Evidence-based severity floors.
- Low, medium, high, and critical severity routing.
- Deterministic response-policy enforcement.
- Human-approval requirements for selected high-impact actions.
- Simulated response actions.
- n8n Data Table result storage.
- Slack alerting for high and critical incidents.
- Retry and degraded-operation paths for external services.

### Security

- Treated incoming alert content as untrusted data.
- Prevented LLM output from directly authorizing sensitive response actions.
- Added prompt-injection hardening.
- Added policy-bypass resistance tests.
- Added Slack-suppression resistance testing.
- Added malformed-input handling.
- Added reserved/synthetic IoC handling for evaluation.
- Performed repository credential and secret scans.

### Evaluation

Three major evaluation stages were retained:

#### Degraded deterministic/fallback baseline

- Category accuracy: 83.3%
- Severity accuracy: 41.7%
- Policy accuracy: 70.8%
- Slack-routing accuracy: 66.7%
- Full-case pass rate: 33.3%

#### Hybrid baseline

- Category accuracy: 91.7%
- Severity accuracy: 41.7%
- Policy accuracy: 75.0%
- Slack-routing accuracy: 66.7%
- Full-case pass rate: 37.5%

#### Final post-fix evaluation

- Category: 24/24
- Severity: 24/24
- Policy: 24/24
- Slack routing: 24/24
- Full-case pass rate: 24/24

These results apply to the final 24-case curated development/evaluation set and are not claims of universal system accuracy.

### Security-hardening evaluation

A separate 8-case hardening suite tested:

- missing required fields;
- malformed timestamps;
- alerts without IoCs;
- multi-IoC selection;
- prompt injection;
- deterministic-policy bypass attempts;
- ambiguous alerts;
- attempts to suppress critical Slack notifications.

Final result:

- Passed: 8/8
- Failed: 0/8

### Documentation

Added:

- comprehensive README;
- architecture documentation;
- security-model documentation;
- evaluation summary;
- curated test data;
- evaluation artifacts;
- security-hardening artifacts;
- workflow screenshots;
- versioned workflow exports.

---

## v0.5

Pre-release evaluation checkpoint.

This version contained the main AdvSOC architecture used during the evaluation and iterative debugging phase before the final validation-response and security-hardening changes included in v1.0.

---

## v0.1

Initial detection-focused workflow prototype.

Early work included:

- alert ingestion;
- payload normalization;
- validation;
- IoC extraction;
- deterministic detection logic.

The early workflow was later superseded by the integrated AdvSOC architecture.
