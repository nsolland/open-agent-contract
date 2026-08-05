# Open Agent Contract

Specification and implementation of verifiable agent contracts linked to REHT, RACS and VALO execution governance.

## Features

- Contract lifecycle: DRAFT → PROPOSED → ACTIVE → SUSPENDED → TERMINATED / EXPIRED
- Clause management: scope, authority, constraints, obligations, prohibitions and permissions
- Enforcement and violation records
- Integrity verification and deterministic SHA-256 contract digests
- Isolated Ephemeral Agent Contract for Need to Ask / Need to Acquire

## Isolated Ephemeral Agent Contract

`open_agent_contract.ephemeral` composes the existing VALO controls for a short-lived acquisition agent:

- origin and delegation chain
- validated Need to Ask / Need to Acquire binding
- explicit sources, tools, resources and prohibited actions
- isolated silo and gateway enforcement
- operating-memory ownership, provenance, retention and deletion
- minimal evidence delivery to the requesting agent
- activation, revocation, expiration, termination and deletion receipts

The registry verifies bindings and lifecycle only. It never replaces REHT authorization, the RACS decision contract, gateway enforcement or Veritas receipts.

See `docs/isolated-ephemeral-agent-contract.md`.

## Quick start

```bash
pip install -e .
pytest --tb=short
```

## General contract lifecycle

```text
DRAFT → PROPOSED → ACTIVE → SUSPENDED → TERMINATED
         ↓
       signatures
         ↓
      ACTIVE → EXPIRED
```

## REHT integration

Each general contract clause can reference a REHT requirement ID. The isolated ephemeral contract additionally binds the exact REHT clearance, RACS decision, gateway policy and Veritas stream used for the acquisition lifecycle.
