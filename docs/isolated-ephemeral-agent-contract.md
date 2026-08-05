# Isolated Ephemeral Agent Contract

## Status

Canonical composition contract for short-lived agents created under VALO Need to Ask / Need to Acquire.

The contract is strict enough to preserve the silo boundary and practical enough to retrieve evidence that is genuinely required for legitimate execution.

## Canonical rule

A requesting agent never receives broader access because it lacks information.

It may submit a bounded Need to Ask request. If the need is valid, necessary, proportionate and minimal, a separate acquisition agent may be created inside an isolated silo.

The acquisition agent receives only the cleared mandate. The requesting agent receives only the cleared evidence output.

## Ownership

`open-agent-contract` owns the composition contract and lifecycle invariants.

It does not take authority from the existing VALO layers:

- MAL admits models, sources and evidence classes.
- Delegation Graph proves origin and monotone delegation.
- Session Authority binds identity, scope, resources and expiry.
- REHT clears each concrete acquisition or delivery action.
- RACS expresses the deterministic decision contract. It does not evaluate or authorize.
- Gateway enforces tools, resources, fields, egress and single-use permits.
- Veritas records activation, execution, delivery, revocation, expiration, termination and deletion.
- Memory Governance and Zero-Mem govern operating-memory admission, retention and deletion.

## Existing controls composed

The contract binds existing controls rather than reimplementing them:

- `valo-platform/src/valo_platform/session_authority_service.py`
  - immutable scoped tokens
  - expiry and revocation
  - short-lived step-up grants
- `valo-platform/src/valo_platform/delegation_graph.py`
  - origin and parent delegation
  - agent-to-agent delegation
  - monotone authority
  - expiry, revocation and chain receipts
- `valo-platform/docs/model-independent-memory-governance.md`
  - ownership, provenance, access policy, retention and deletion
  - minimum context exposure
  - separate memory decisions for durable writeback
- `Racs/reference/python/racs_permit.py`
  - bounded execution permits
  - shorter-lived single-use commit tokens
  - expiry inherited from upstream authorization
- `open_agent_contract/ephemeral.py`
  - one immutable composition object
  - cross-layer binding and lifecycle verification

## Contract contents

The canonical contract contains:

1. Origin
   - principal
   - requesting agent
   - Need to Ask request
   - parent contract
   - delegation chain and digest

2. Need to Ask / Need to Acquire binding
   - reason for the request
   - acquisition decision
   - isolated acquisition agent identity
   - REHT clearance
   - RACS decision reference
   - gateway policy
   - Veritas stream

3. Bounded mandate
   - purpose
   - explicit task scope
   - explicit sources, tools and resources
   - prohibited actions
   - maximum actions
   - no further delegation

4. Isolation boundary
   - silo identity and isolation class
   - gateway enforcement
   - credential broker lease
   - explicit network egress
   - no cross-silo access
   - no raw credentials

5. Operating-memory lease
   - owner and provenance
   - explicit readers and writers
   - memory classes and size limit
   - retention deadline
   - deletion on closure
   - no automatic writeback to canonical memory
   - mandatory Zero-Mem deletion receipt

6. Evidence delivery
   - requesting agent as recipient
   - explicit allowed fields
   - redaction profile
   - item limit
   - no credentials
   - no raw-source delivery without separate authorization

7. Lifecycle
   - creation and activation deadline
   - hard expiry
   - revocation
   - termination
   - deletion deadline and proof

## Lifecycle

```text
Need to Ask request
        -> need evaluation
        -> Need to Acquire decision
        -> DRAFT contract
        -> ACTIVE with Veritas activation receipt
        -> per-action REHT clearance
        -> RACS decision contract
        -> gateway enforcement
        -> minimal evidence delivery
        -> REVOKED | EXPIRED | TERMINATED
        -> operating-memory deletion
        -> DELETED with Zero-Mem / Veritas receipt
```

The contract registry verifies lifecycle and bindings only. A valid active contract is necessary but never sufficient for execution. Every action still requires the normal REHT, RACS and gateway chain.

## Hard invariants

The implementation rejects:

- wildcard sources, tools, resources, fields or egress
- cross-silo access
- raw credential exposure
- further delegation
- operating memory that survives its deletion deadline
- durable memory writeback without a separate memory-governance decision
- raw-source or credential delivery
- lifetimes longer than the contract maximum
- active or closed states without the required Veritas receipt and timestamp
- evidence delivery to anyone other than the requesting agent

## Relationship to Operating Memory

Operating memory is not agent-owned memory. It is a leased governed object.

The agent may use only the memory classes and bytes explicitly admitted by the contract. At closure, the lease ends. Any knowledge proposed for durable retention must enter Memory Governance as a new candidate with its own owner, provenance, access, retention and evidence decision.

## Relationship to Zero-Mem and LastSeen

Zero-Mem provides the deletion discipline and proof pattern.

LastSeen provides a concrete edge use case: local observations may be retained under explicit ownership and retention policy, while temporary inference or acquisition workers remain isolated and disposable. Durable object history and temporary agent working memory are separate governed objects.

## Canonical formulations

Strict enough to protect the boundary. Practical enough to retrieve what is actually necessary.

Ask is a proposal. Acquire is a separately authorized action.

The requesting agent never crosses the silo boundary. A bounded acquisition agent retrieves only the cleared evidence.

An active contract proves bounded mandate and lifecycle. It does not itself authorize execution.
