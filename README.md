# Open Agent Contract

Vendor-neutral contracts for governed agent consequence.

[![CI](https://github.com/nsolland/open-agent-contract/actions/workflows/ci.yml/badge.svg)](https://github.com/nsolland/open-agent-contract/actions/workflows/ci.yml)
[![status](https://img.shields.io/badge/status-public%20release%20candidate-1f2937)](PUBLICATION_STATUS.md)
[![version](https://img.shields.io/badge/version-0.4.0-1f2937)](CHANGELOG.md)
[![contract](https://img.shields.io/badge/Governed%20Contract-1.1.0-1f2937)](docs/governed-contract-v1.md)
[![license](https://img.shields.io/badge/license-MIT-1f2937)](LICENSE)

> **Publication status — 2026-08-14:** this repository is public. The current target package line is `0.4.0`; Governed Contract semantics are `1.1.0`. See [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md) for exact release state.

The project defines a portable Governed Contract for describing who may attempt what action, on which resource, for which purpose, under which authority, evidence, constraints and validity window.

It is designed for A2A and human-to-agent interoperability. It does not require a specific model, agent framework, identity provider, transport, policy engine or execution-governance product.

## Governed Contract v1.1

Core fields:

- issuer and subject identity references
- explicit authority grants and delegation chain
- allowed actions, resources and purposes
- explicit prohibitions and constraints
- evidence requirements with freshness bounds
- validity window
- completion conditions
- downstream receipt requirement
- vendor/domain extension namespace

Deterministic conformance outcomes:

- `conformant`
- `non_conformant`
- `insufficient_evidence`
- `not_yet_valid`
- `expired`

A `conformant` result is not permission to execute. It means the intent satisfies the portable contract and may be submitted to a separate organization-controlled authorization/enforcement boundary.

Every newly produced conformance result binds the exact contract ID, spec version and digest used for evaluation. `verify_contract_continuity()` detects amendment/replacement before a prior result is reused. `contract_changed` requires fresh conformance.

Legacy results without a contract spec version remain readable, but continuity fails closed to fresh conformance.

Persistence also creates no standing: files, memory, config, instructions, handoffs or cached artifacts do not become contract authority or evidence merely because they survived into another agent/session.

See `docs/governed-contract-v1.md` and `open_agent_contract.governed`.

## Reference flow

```text
agent discovery / transport
        |
        v
Governed Contract
        |
        v
contract conformance + exact contract digest
        |
        v
continuation check if reused later
        |
        v
organization-controlled authorization boundary
        |
        v
execution / settlement
        |
        v
receipt / evidence
```

## Relationship to other governed-contract work

This repository remains an independently usable portable contract/reference implementation.

The exact canonical relationship between Open Agent Contract and VALO GCoP is **unresolved** as of 2026-08-14. They MUST NOT be described as aliases, replacements or parent/child profiles until that relationship is explicitly resolved.

This uncertainty does not weaken the local contract invariants:

```text
conformance != execution authorization
persistence != standing
contract drift -> fresh conformance
```

## Existing contract lifecycle

The package also retains the original general and isolated ephemeral agent-contract implementation:

- DRAFT → PROPOSED → ACTIVE → SUSPENDED → TERMINATED / EXPIRED
- scope, authority, constraints, obligations, prohibitions and permissions
- enforcement and violation records
- integrity verification and deterministic digests
- isolated ephemeral contracts for bounded acquisition work

These modules remain backward compatible. Product-specific integrations are optional adapters, not requirements of the open Governed Contract.

## Quick start

```bash
pip install -e '.[test]'
pytest --tb=short
```

```python
from datetime import datetime, timedelta, timezone
from open_agent_contract import (
    ActionIntent,
    AuthorityGrant,
    GovernedContract,
    PartyRef,
    check_conformance,
    verify_contract_continuity,
)

now = datetime.now(timezone.utc)
org = PartyRef(party_id="org:example", kind="organization")
agent = PartyRef(party_id="agent:buyer", kind="agent")

contract = GovernedContract(
    contract_id="gc-1",
    issuer=org,
    subject=agent,
    authority=[AuthorityGrant(
        grant_id="g-1",
        granted_by=org.party_id,
        granted_to=agent.party_id,
        actions=["purchase"],
        resources=["catalog:item-42"],
        purposes=["restock"],
    )],
    allowed_actions=["purchase"],
    allowed_resources=["catalog:item-42"],
    allowed_purposes=["restock"],
    valid_from=now,
    valid_until=now + timedelta(hours=1),
)

intent = ActionIntent(
    intent_id="i-1",
    actor=agent,
    action="purchase",
    resource="catalog:item-42",
    purpose="restock",
    requested_at=now,
)

result = check_conformance(contract, intent, checked_at=now)
continuity = verify_contract_continuity(result, contract)
print(result.outcome, continuity.outcome)
```

## Project governance

- [`CHANGELOG.md`](CHANGELOG.md) — version history
- [`GOVERNANCE.md`](GOVERNANCE.md) — normative/public-API change authority and external standardization transfer
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules
- [`SECURITY.md`](SECURITY.md) — vulnerability reporting
- [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md) — exact publication and release state

Wire-format/spec versions and Python package versions are intentionally independent. Substantive additive contract semantics increment the Governed Contract minor version. The pre-1.0 Python package increments its own minor version when its public API/behavior expands materially.

Discussion, issues, publisher review and external standards work are proposal/evidence surfaces. They do not silently change the contract; accepted versioned contract/API state is normative for this repository until an explicit canonical transfer.

## Publication

This repository is public and open source. A formal release is identified only by an exact version, tag and commit hash; repository visibility by itself is not a release claim. Historical tags are immutable and corrections move forward through new versions.

## License

MIT. The contract format and reference implementation are intended to be usable independently of any single vendor.
