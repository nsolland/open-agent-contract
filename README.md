# Open Agent Contract

Spesifikasjon og implementasjon av verifiserbare agentkontraktar.

Knytt til REHT standardar, RACS bindingar, og **BO#42**.

## Features

- **Contract Lifecycle** — DRAFT → PROPOSED → ACTIVE → SUSPENDED → TERMINATED
- **Clause Management** — scope, authority, constraint, obligation, prohibition, permission clauses
- **Enforcement Tracking** — record enforcements and violations per contract
- **Integrity Verification** — verify contract state and REHT requirement compliance
- **Contract Digest** — SHA-256 digest for signing and verification

## Quick Start

```bash
pip install -e .
pytest --tb=short
```

## Contract Lifecycle

```
DRAFT → PROPOSED → ACTIVE → SUSPENDED → TERMINATED
         ↓
       (signatures required)
         ↓
      ACTIVE → EXPIRED (if expires_at set)
```

## REHT Integration

Each clause can reference a REHT requirement ID, enabling traceability between agent contracts and governance requirements.
