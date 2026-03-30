# CLAUDE.md — medinovai-connector-framework

> This file is read by every Claude agent at the start of each session.
> Keep it accurate. It is the agent's primary source of truth about this repo.

## Purpose

Phase E integration service that hosts pluggable connectors to eight external health-data platforms (AWS HealthLake, Datavant, TriNetX, N3C, PCORnet, Mayo Clinic Platform, Azure Health Data Services, NIH All of Us). It exposes a uniform FastAPI surface for authentication probes, per-connector health, ingestion hooks, and registration metadata. Upstream callers include **medinovai-integration-gateway** (canonical ingest routing) and platform automation; credentials are expected from **medinovai-secrets-manager-bridge**, not from repo config.

## Compliance Tier

Tier **2** (platform / integration — security layer, no direct PHI persistence in this scaffold).

Applicable regulations: HIPAA and GDPR apply to **downstream** deployments when handling PHI; this repo must enforce audit-safe logging (IDs only), TLS for egress, and secrets externalization.

## Tech Stack

- Backend: Python 3.11, FastAPI, Uvicorn
- Frontend: None
- Database: None (connectors call external systems)
- Cache: None (optional Redis in later phases)
- Messaging: Optional CloudEvents to integration gateway / stream bus (stubs)
- Infrastructure: Docker, Kubernetes-ready probes
- Monitoring: Structured JSON logs (structlog), health/readiness endpoints

## How to Start the Dev Server

```bash
bash init.sh
```

Dev server runs at: `http://localhost:8000`  
Health endpoint: `GET /health` → 200 OK  
Readiness: `GET /ready` → 200 OK  
Per-connector paths (slug in URL): `GET /health/aws`, `GET /health/datavant`, `GET /health/trinetx`, `GET /health/n3c`, `GET /health/pcornet`, `GET /health/mayo`, `GET /health/azure`, `GET /health/all_of_us`  
Aggregate: `GET /health/summary`  
Registry: `GET /connectors`  
Ingest: `POST /ingest/{slug}`, batch `POST /ingest/batch/{slug}`

## How to Run Unit Tests

```bash
# After test suite is added
pytest tests/unit/ -q
```

Minimum coverage: 80% (target for production hardening).

## How to Run End-to-End Tests

```bash
# After Playwright or integration tests exist
pytest tests/integration/ -q
```

## Coding Conventions (MedinovAI Standard)

- Constants: `E_VARIABLE` (uppercase, `E_` prefix)
- Variables: `mos_variableName` (lowerCamelCase, `mos_` prefix)
- Methods: max 40 lines; split into private helpers if longer
- Docstrings: Google style on public functions and classes
- Error handling: never swallow exceptions; log with correlation ID
- Secrets: AWS Secrets Manager / secrets-manager-bridge only — no literals in code or committed config
- Orchestration: Claude Agent SDK / ActiveMQ / Step Functions patterns for platform workflows — no n8n

## API Standards

- REST JSON; OpenAPI auto-docs at `/docs`
- Protected routes should validate JWT via **medinovai-security-service** (MSS) when deployed — not implemented in this scaffold
- Rate limiting: per-connector quotas per `specs/active/medinovai-2in-connector-framework/specification.yaml`

## Tier 1 Compliance Requirements (N/A for Tier 2 scaffold)

Skip PHI-at-rest in this service until connected to regulated data paths; still **never log PHI** — use resource IDs and correlation IDs only.

## Git Branch Strategy

- `main`: production-ready only — no direct commits
- `develop`: integration branch (if used)
- Feature branches: `feature/F###-short-description`
- Agent commits to feature branch, then opens PR

## Known Issues / Current State

- Connectors are **stubs**: `authenticate`, `health_check`, and `ingest` return structured placeholders until platform SDKs and secrets wiring land.
- Register with **medinovai-registry** in a future feature.

## Last Updated

2026-03-30 — Harness 2.1 initializer scaffold (Tier 2)
