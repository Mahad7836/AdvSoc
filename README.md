# AdvSOC

**Policy-Governed AI SOC Analyst for Automated Threat Triage and Secure Incident Response using n8n**

AdvSOC is a security automation workflow that combines deterministic detection logic, threat-intelligence enrichment, LLM-assisted SOC analysis, risk scoring, policy enforcement, human-approval controls, structured logging, and Slack alerting.

The project explores a central security question:

> How can an AI-assisted SOC workflow gain useful reasoning capability without allowing the AI model itself to authorize sensitive security actions?

AdvSOC addresses this by separating **AI analysis** from **deterministic authorization**.

---

## Core Design Principle

The LLM may:

- classify alerts;
- summarize evidence;
- explain likely security implications;
- suggest MITRE ATT&CK mappings;
- recommend response actions.

The LLM may **not**:

- authorize high-impact remediation;
- bypass the deterministic policy layer;
- disable human approval;
- directly execute destructive actions.

Final action authorization is controlled by deterministic policy logic.

High-impact response actions are simulated in the current project version.

---

## Architecture

AdvSOC processes alerts through the following stages:

1. Alert ingestion
2. Input normalization
3. Schema validation
4. IoC extraction
5. Deterministic security-rule evaluation
6. Primary IoC selection
7. VirusTotal enrichment
8. AI-assisted SOC classification
9. Risk scoring
10. Deterministic response-policy evaluation
11. Structured result logging
12. Severity-based routing
13. Slack notification for high/critical alerts
14. Webhook response

The architecture intentionally maintains deterministic control around security-sensitive decisions.

---

## Supported Alert Inputs

Required fields:

- `alert_id`
- `timestamp`
- `source`
- `alert_type`
- `description`

Optional fields include:

- `source_ip`
- `destination_ip`
- `domain`
- `url`
- `file_hash`
- `username`
- `hostname`
- `original_severity`
- `metadata`

---

## IoC Support

AdvSOC currently extracts and processes:

- IPv4 addresses
- domains
- URLs
- MD5 hashes
- SHA-1 hashes
- SHA-256 hashes

When several IoCs exist, the enrichment priority is:

`file hash > URL > domain > IP`

The current implementation performs one primary VirusTotal lookup per alert.

---

## Threat-Intelligence Enrichment

VirusTotal is used as the primary threat-intelligence provider.

Threat-intelligence results contribute to the final risk assessment but do not independently determine response authorization.

The workflow also supports degraded operation when enrichment is unavailable.

Synthetic and reserved test indicators are prevented from artificially influencing evaluation scores.

---

## AI-Assisted SOC Analysis

The AI classifier receives normalized alert evidence, deterministic-rule results, and available threat-intelligence findings.

The model returns structured output containing:

- security category;
- confidence;
- summary;
- explanation;
- recommended action;
- MITRE ATT&CK mappings.

Supported categories:

- `benign_informational`
- `suspicious_authentication`
- `malicious_network_activity`
- `phishing_malicious_url`
- `malware_malicious_file`
- `reconnaissance_scanning`
- `other_unknown`

Alert fields are explicitly treated as **untrusted data**.

Instructions embedded inside alert descriptions, URLs, usernames, metadata, or other fields are not intended to control the SOC workflow.

---

## Risk Scoring

AdvSOC combines three evidence sources:

| Component | Maximum contribution |
|---|---:|
| Deterministic security rules | 60 |
| Threat intelligence | 25 |
| AI assessment | 15 |
| **Maximum risk score** | **100** |

Severity levels:

| Risk score | Severity |
|---:|---|
| 0–24 | Low |
| 25–49 | Medium |
| 50–74 | High |
| 75–100 | Critical |

Evidence-based floors are also used for strongly supported scenarios such as critical malware, privileged-account compromise, and C2/exfiltration activity.

---

## Policy-Governed Response

Examples of response actions include:

- `log_only`
- `investigate`
- `escalate`
- `block_indicator`
- `isolate_host`
- `disable_account`
- `contain_and_escalate`

Low-impact actions may be allowed automatically.

High-impact actions require deterministic policy review and may require human approval.

Destructive or unsafe actions are not executed automatically.

Response execution in this project is simulated.

---

## Slack Alerting

High and critical alerts are routed to Slack with structured information including:

- run ID;
- alert ID;
- severity;
- risk score;
- category;
- summary;
- recommended action;
- policy decision;
- action code;
- human-approval requirement;
- execution mode.

Low and medium events are logged without unnecessary high-priority Slack notifications.

---

## Evaluation

AdvSOC was evaluated using a curated 24-case SOC alert development/evaluation set:

- 4 benign/informational cases
- 4 authentication cases
- 4 malicious network/C2 cases
- 3 phishing cases
- 3 malware cases
- 3 reconnaissance cases
- 3 unknown/ambiguous cases

### Degraded-Mode Baseline

| Metric | Result |
|---|---:|
| Category accuracy | 83.3% |
| Severity accuracy | 41.7% |
| Policy accuracy | 70.8% |
| Slack-routing accuracy | 66.7% |
| Full-case pass rate | 33.3% |

The AI classifier was unavailable during this baseline because of a prompt-configuration issue, so this primarily represents deterministic/fallback operation.

### Hybrid Baseline

After restoring the AI path:

| Metric | Result |
|---|---:|
| Category accuracy | 91.7% |
| Severity accuracy | 41.7% |
| Policy accuracy | 75.0% |
| Slack-routing accuracy | 66.7% |
| Full-case pass rate | 37.5% |

### Post-Fix Evaluation

Following improvements to evidence extraction, scoring, ambiguity handling, malware distinction, and evidence-based severity floors:

| Metric | Result |
|---|---:|
| Category accuracy | 100% |
| Severity accuracy | 100% |
| Policy accuracy | 100% |
| Slack-routing accuracy | 100% |
| Full-case pass rate | 100% |

**Important:** this represents a **100% full-case pass rate on the final 24-case curated development/evaluation set**. It is not a claim of universal or production-level accuracy.

Detailed evaluation artifacts are available in [`results/`](results/).

---

## Security Hardening

A separate 8-case security-hardening suite tested behavior outside the primary evaluation set.

It covered:

- missing required fields;
- malformed timestamps;
- alerts without IoCs;
- multiple IoCs;
- prompt injection inside alert descriptions;
- attempts to override deterministic policy;
- ambiguous/unknown alerts;
- attempts to suppress critical Slack notifications through untrusted input.

Final result:

**8/8 security-hardening cases passed.**

Manual verification also confirmed:

- multi-IoC selection prioritized the file hash;
- an injected instruction attempting to suppress Slack did not prevent the critical alert from being routed.

---

## Resilience and Degraded Operation

AdvSOC includes failure handling for external dependencies and invalid input:

- VirusTotal retries and fallback;
- rate-limit handling;
- AI retries;
- deterministic AI fallback;
- bounded external-service failures;
- webhook validation;
- structured HTTP 400 responses for malformed requests.

The workflow is designed to preserve deterministic analysis and policy enforcement when external AI or threat-intelligence services are unavailable.

---

## Repository Structure

```text
AdvSoc/
├── docs/
├── results/
├── screenshots/
├── test-data/
├── workflows/
├── .env.example
├── .gitignore
└── README.md
```

### `workflows/`

Exported n8n workflow versions.

### `test-data/`

Curated evaluation and security-hardening datasets.

### `results/`

Baseline, hybrid, post-fix, failure-analysis, metrics, and security-hardening artifacts.

### `docs/`

Additional architecture, security, and evaluation documentation.

### `screenshots/`

Selected visual evidence of the working system.

---

## Running AdvSOC

AdvSOC was developed and tested using a local Docker-based n8n instance.

Example:

```powershell
docker run -d `
  --name n8n `
  -p 5678:5678 `
  -e GENERIC_TIMEZONE="Asia/Riyadh" `
  -e TZ="Asia/Riyadh" `
  -v n8n_data:/home/node/.n8n `
  docker.n8n.io/n8nio/n8n
```

Open:

```text
http://localhost:5678
```

The production webhook endpoint used during development is:

```text
POST /webhook/advsoc/alert
```

Example payload:

```json
{
  "alert_id": "EXAMPLE-001",
  "timestamp": "2026-08-27T10:00:00+03:00",
  "source": "example-siem",
  "alert_type": "phishing",
  "description": "Email contained a suspicious credential-harvesting link.",
  "url": "https://example.invalid/login",
  "original_severity": "high"
}
```

External-service credentials should be configured using the appropriate n8n credential mechanisms.

**Never commit real API keys or tokens.**

See `.env.example` for placeholder configuration examples.

---

## Security Boundaries

AdvSOC assumes alert fields may contain attacker-controlled content.

Therefore:

- alert descriptions are treated as untrusted data;
- embedded instructions are not authoritative workflow commands;
- LLM output is advisory rather than authorization;
- deterministic logic determines response policy;
- selected high-impact actions require human approval;
- destructive actions are not automatically executed.

The hardening suite specifically tested attempts to:

- force benign classification;
- force `policy_decision=allow`;
- disable human approval;
- suppress Slack notification;
- lower severity through attacker-controlled text.

Those attempts did not override the deterministic controls in the final tested configuration.

---

## Current Limitations

AdvSOC is a portfolio and security-automation prototype rather than a production SIEM/SOAR platform.

Current limitations include:

- relatively small curated evaluation set;
- no independent held-out benchmark yet;
- no claim of universal prompt-injection resistance;
- one primary threat-intelligence lookup per alert;
- dependence on external LLM and threat-intelligence services;
- simulated high-impact response actions;
- limited enterprise identity and asset context;
- limited historical alert correlation;
- no production-grade RBAC or multi-tenant architecture;
- no replacement for human SOC analysts.

The 24/24 result should therefore be interpreted only within the scope of the documented curated evaluation set.

---

## Future Work

Potential extensions include:

- larger held-out SOC datasets;
- adaptive and adversarial prompt-injection evaluation;
- additional threat-intelligence providers;
- richer MITRE ATT&CK correlation;
- asset-criticality and identity-risk context;
- historical alert correlation;
- analyst-feedback loops;
- production-grade approval workflows;
- SIEM/SOAR integrations;
- expanded observability and performance metrics.

---

## Evaluation Artifacts

Useful result files include:

- `results/EVALUATION_SUMMARY.md`
- `results/advsoc-baseline-metrics.json`
- `results/advsoc-baseline-failure-analysis.json`
- `results/advsoc-eval-baseline-24.json`
- `results/advsoc-eval-hybrid-24.json`
- `results/advsoc-eval-postfix-24.json`
- `results/advsoc-postfix-metrics.json`
- `results/advsoc-security-hardening-results.json`

Corresponding CSV files are included where useful for manual analysis.

---

## Workflow Versions

`workflows/advsoc-core-v0.5.json` is the evaluated pre-release workflow checkpoint.

`workflows/advsoc-core-v1.0.json` is the final hardened release workflow.

---

## Responsible Use

AdvSOC is intended for defensive cybersecurity learning, experimentation, and security-automation research.

All high-impact actions in this project are simulated.

This prototype should not be treated as a production-ready autonomous incident-response system without substantially broader testing, governance, authentication, authorization, monitoring, deployment hardening, and human oversight.

---

## Project Status

**AdvSOC v1.0 released**

- Core workflow: complete
- 24-case evaluation: complete
- Evaluation-driven corrections: complete
- 8-case security-hardening suite: complete
- Repository security review: complete
- Final documentation: complete
- Final v1.0 export and release: complete

