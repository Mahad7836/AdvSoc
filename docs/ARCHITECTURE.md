# AdvSOC Architecture

## Overview

AdvSOC is a policy-governed AI-assisted SOC workflow implemented in n8n.

Its core architectural principle is separation of responsibilities:

- deterministic components validate, score, enforce policy, and route actions;
- threat intelligence contributes external evidence;
- the LLM assists with interpretation and classification;
- the LLM does not authorize sensitive response actions.

## Processing Pipeline

```text
Security Alert
      |
      v
Normalization
      |
      v
Validation
      |
      +---- invalid ----> HTTP 400 rejection
      |
      v
IoC Extraction
      |
      v
Deterministic Rule Engine
      |
      v
Primary IoC Selection
      |
      v
VirusTotal Enrichment
      |
      v
AI Context Preparation
      |
      v
LLM SOC Classifier
      |
      +---- failure ----> Deterministic AI Fallback
      |
      v
Final Risk Scoring
      |
      v
Deterministic Policy Gate
      |
      v
Structured Result Storage
      |
      v
Severity Routing
      |
      +---- Low / Medium ---> Complete
      |
      +---- High / Critical ---> Slack Alert
      |
      v
Webhook Response
Input Layer

Required alert fields:

alert_id
timestamp
source
alert_type
description

Optional context may contain IoCs, usernames, hostnames, source severity, and metadata.

All incoming values are normalized before validation.

Malformed requests are rejected before security analysis.

Deterministic Detection

The rule engine identifies evidence such as:

repeated authentication failures;
brute-force indicators;
successful login after failures;
privileged identities;
malware indicators;
phishing indicators;
reconnaissance activity;
command-and-control or exfiltration evidence;
source-provided severity.

Natural-language quantities such as seven and thirty-five are supported for authentication-event analysis.

Threat Intelligence

AdvSOC selects one primary IoC using:

file hash > URL > domain > IP

VirusTotal enrichment contributes up to 25 points to the final risk score.

Reserved and synthetic test indicators do not contribute threat-intelligence risk during evaluation.

AI Classification

The LLM receives:

normalized alert evidence;
extracted IoCs;
deterministic rule results;
available threat-intelligence findings.

It returns structured fields including:

category;
confidence;
summary;
explanation;
recommended action;
MITRE ATT&CK mappings.

If the classifier fails, AdvSOC continues using deterministic fallback analysis.

Risk Model

Final risk combines:

Deterministic rules : max 60
Threat intelligence : max 25
AI assessment       : max 15
--------------------------------
Total                : max 100

Severity thresholds:

0-24   Low
25-49  Medium
50-74  High
75-100 Critical

Evidence-based severity floors prevent strongly supported incidents from being unintentionally downgraded when enrichment is weak or unavailable.

Policy Layer

The policy engine operates after classification and scoring.

Examples:

Low      -> log_only
Medium   -> investigate
High     -> review / simulated containment
Critical -> review / simulated high-impact response

Sensitive actions can require human approval.

The LLM does not directly set the authoritative policy decision.

Storage and Notification

Final structured results are stored through n8n Data Tables.

High and critical events are routed to Slack.

Low and medium alerts remain logged without unnecessary high-priority notification.

Failure Modes

AdvSOC includes degraded paths for:

no IoC;
unavailable VirusTotal;
rate limits;
AI service failure;
malformed user input.

These paths preserve deterministic policy enforcement wherever possible.

Scope

AdvSOC is a security-automation prototype.

It is not intended to replace:

a production SIEM;
a production SOAR;
enterprise IAM;
human SOC analysts;
production incident-response governance.
