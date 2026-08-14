# Changelog

All notable changes to Open Agent Contract are recorded here.

## 0.4.0 — Governed Contract 1.1.0

Added:

- `contract_spec_version` in newly produced `ConformanceResult` objects;
- `verify_contract_continuity()` and deterministic `ContinuationResult`;
- `contract_changed` refusal when the current contract ID/spec/digest differs from the contract used for prior conformance;
- explicit rule that contract continuity is not execution authorization;
- documentation that persisted files/memory/config/instructions/handoffs do not acquire contract standing merely through persistence;
- public governance/versioning rules and normative-change issue template.

Changed:

- default Governed Contract wire semantics from `1.0.0` to additive `1.1.0`;
- Python package from `0.3.0` to `0.4.0` because the pre-1.0 public API gains continuation behavior;
- A2A-derived conformance results now preserve the exact contract spec version.

Migration:

Existing `GovernedContract` fields remain compatible. Legacy persisted `ConformanceResult` objects without `contract_spec_version` remain deserializable, but contract continuity fails closed and requires fresh conformance because the original spec version cannot be proven.

## 0.3.0 — 2026-08-14

Added:

- portable Governed Contract v1 and deterministic conformance behavior;
- A2A reference profile and examples;
- APS draft-03 authority adapter;
- public release metadata and publication-state documentation.

Clarified:

- `conformance != execution authorization`;
- organization-controlled authorization and enforcement remain separate;
- optional adapters do not become core dependencies;
- the relationship to VALO GCoP remains unresolved until explicitly decided.

## 0.2.0

Added the governed-contract model and reference implementation while retaining the original contract lifecycle modules.

## 0.1.0

Initial agent-contract implementation.
