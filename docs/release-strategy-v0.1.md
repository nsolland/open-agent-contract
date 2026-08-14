# Governed Contract v0.1 — Release Strategy

## Position

Governed Contract is an open, vendor-neutral contract for governing consequence across autonomous systems.

A2A provides inter-agent communication and leaves authorization logic implementation-specific. Governed Contract does not replace A2A authentication or authorization. It provides a portable, machine-readable statement of authority, purpose, scope, resources, constraints, evidence, validity and completion that independent systems can evaluate before consequence.

Core distinction:

- communication answers: can these systems interact?
- authentication answers: who is this?
- local authorization answers: may this caller make this request here?
- Governed Contract answers: does this proposed consequence conform to the portable mandate shared across the interaction?
- execution authorization remains organization-controlled.

A conformant contract is never itself permission to execute.

## GTM principle

Open the contract. Compete on enforcement.

The open project contains only what another vendor must be able to implement independently:

- normative contract specification
- portable schema/model
- deterministic conformance semantics
- conformance tests
- reference validator
- protocol bindings and examples

VALO/reht, proprietary policy/evaluation logic, enterprise enforcement, internal governance methods and operational infrastructure are outside the standard.

## Release sequence

### Preview 0 — private design review

Do not publish the repository yet.

Send a compact package to a small set of protocol maintainers, enterprise architects and agent-platform builders. The package contains:

1. one-page problem statement
2. Governed Contract v0.1 specification
3. one A2A consequence demo
4. conformance test vectors
5. one question: `What interoperable contract should survive across organizational boundaries when an agent action is about to create consequence?`

The goal is not endorsement. The goal is to find semantic collisions, missing fields and existing work before public namespace is committed.

Exit criteria:

- no discovered protocol already provides equivalent portable consequence semantics
- at least two independent reviewers can implement or evaluate the contract without VALO knowledge
- A2A binding does not alter core A2A semantics
- no proprietary VALO/reht material is required to conform

### Preview 1 — public v0.1

Publish only after Preview 0 exit criteria pass.

Release assets:

- repository under an open license
- immutable `v0.1.0` tag
- normative specification
- JSON-compatible contract schema/model
- deterministic validator
- conformance suite
- A2A extension example
- purchase-limit demo
- security and non-goals document
- contribution and governance documents

Public message:

`An open contract for governing consequence across autonomous systems.`

Do not launch as a VALO product. VALO Research is the initial contributor/reference implementer.

### Preview 2 — interoperability

Target independent implementations rather than stars or downloads.

Success means:

- two implementations that do not share the reference validator
- one A2A integration
- one MCP/tool-execution integration
- one cross-organization enterprise design partner
- published conformance vectors pass across implementations

Only after this should the project seek formal ecosystem hosting or standardization.

## Canonical demo

Scenario: purchasing agents.

Principal grants Buyer Agent authority to purchase inventory up to EUR 1,000 for purpose `restock` during a bounded validity window.

Buyer Agent and Seller Agent discover and communicate successfully. Authentication succeeds. A purchase of EUR 1,200 is proposed.

Expected result:

```text
A2A communication: OK
identity/authentication: OK
request accepted by protocol: OK
Governed Contract conformance: NON_CONFORMANT
execution authorization: NOT REACHED
financial consequence: NONE
receipt: contract rejection evidence
```

Then repeat with EUR 900:

```text
A2A communication: OK
identity/authentication: OK
Governed Contract conformance: CONFORMANT
execution authorization: REQUIRED SEPARATELY
```

This demonstrates the boundary without claiming that the contract itself authorizes execution.

## A2A path

Implement Governed Contract first as an independent specification with an experimental A2A extension profile.

The extension should carry or reference:

- contract identifier and version
- immutable contract digest
- intent identifier
- subject/actor reference
- purpose
- requested consequence/action
- resource reference
- evidence references
- conformance result reference

Do not put credentials or proprietary policy internals into the extension.

Treat all received contract and evidence material as untrusted until validated.

If ecosystem feedback is positive and independent implementations exist, propose the extension through A2A's extension governance rather than modifying A2A core.

## Licensing

Before formal A2A submission, reassess MIT versus Apache-2.0. A2A's official extension governance requires Apache-2.0 for extensions hosted by the A2A organization. Do not create an avoidable relicensing barrier.

## Naming

Working project: Open Agent Contract.

Normative artifact: Governed Contract.

Avoid naming the standard `VALO Contract` or `reht Contract`. Vendor neutrality is part of the architecture, not marketing.

## What we measure

Do not optimize the first release for GitHub attention.

Measure:

- independent implementability
- protocol compatibility
- conformance agreement
- number of external implementations
- design partners
- issues that improve the normative model
- whether external teams use the contract without the VALO runtime

## Release gate

The repository remains private until:

- IP/proprietary dependency review is clean
- package history is safe to expose
- A2A example and conformance vectors are present
- security/non-goals are explicit
- license decision is final
- Preview 0 feedback has been incorporated

Public visibility is the final release action, not the first.