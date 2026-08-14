# Governed Contract v1.1

Governed Contract is a vendor-neutral machine-readable contract for agent-to-agent consequence.

It defines identity, delegated authority, purpose, scope, resources, constraints, evidence, validity, completion conditions and receipt requirements.

A conformant intent is eligible for a separate organization-controlled decision boundary. Conformance does not itself execute anything.

Outcomes are `conformant`, `non_conformant`, `insufficient_evidence`, `not_yet_valid`, and `expired`.

Missing or stale required evidence must never be inferred as present.

The format is transport-, model-, identity-provider-, and vendor-neutral.

## Contract continuity

Every newly produced `ConformanceResult` carries the exact `contract_id`, `contract_spec_version` and deterministic `contract_digest` used for the check.

A prior conformant result is not durable permission. Before relying on it in a later continuation, the consumer can call `verify_contract_continuity()` against the current Governed Contract.

If the contract has been amended, replaced or otherwise changed, the result is `contract_changed` with `requires_fresh_conformance=true`. The old result must not be rebound under the changed contract.

Legacy conformance results without a recorded contract spec version remain readable, but continuity fails closed and requires fresh conformance because the original contract semantics cannot be proven.

A `current` continuation result proves only contract identity/digest continuity. It is not execution authorization and does not replace fresh authority, evidence, state or policy checks at the organization-controlled consequence boundary.

## Persistent material

Files, memory, configuration, instructions, handoffs or cached artifacts that survive between agents/sessions do not acquire contract standing merely by persistence.

If such material is required evidence, it must be supplied through the contract's evidence surface with the provenance/freshness required by the relevant profile. Worker-produced material cannot silently self-promote into a contract, authority grant or required evidence.

## Versioning

Governed Contract wire semantics are `1.1.0` for this additive continuity revision. The Python package is independently versioned as `0.4.0` because the package remains pre-1.0.
