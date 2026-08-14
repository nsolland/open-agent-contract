# Open Agent Contract

Vendor-neutral contracts for governed agent consequence.

> **Publication status — 2026-08-14:** this GitHub repository is **public**. The contract format and reference implementation are available under the MIT License. See [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md).

The project defines a portable Governed Contract for describing who may attempt what action, on which resource, for which purpose, under which authority, evidence, constraints and validity window.

It is designed for A2A and human-to-agent interoperability. It does not require a specific model, agent framework, identity provider, transport, policy engine or execution-governance product.

## Governed Contract v1

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

See `docs/governed-contract-v1.md` and `open_agent_contract.governed`.

## Reference flow

```text
agent discovery / transport
        |
        v
Governed Contract
        |
        v
contract conformance
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

This uncertainty does not weaken the local contract invariant:

```text
conformance != execution authorization
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
print(result.outcome)
```

## Publication

See [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md) for the release-state vocabulary and publication checks.

As of 2026-08-14, this repository is a **public open-source repository**. A separately identified version/tag/package is still required before describing any exact snapshot as a published release artifact.

## License

MIT. The contract format and reference implementation are intended to be usable independently of any single vendor.
