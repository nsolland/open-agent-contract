# A2A Governed Contract Extension Profile v0.1

Status: private design preview.

## Purpose

A2A enables interoperable agent interaction. This profile adds portable semantics for the conditions under which a resulting action is contract-conformant before it is submitted to an organization-controlled execution-authorization boundary.

It does not replace A2A authentication or authorization. It does not authorize execution.

## Extension URI

`https://openagentcontract.org/extensions/governed-contract/v1`

## Required metadata

- `contract_id`
- `contract_digest`
- `intent_id`
- `outcome`
- `issues`
- `checked_at`
- `authorization_required: true`

## Processing rule

1. A2A transport/discovery/authentication completes normally.
2. The action is represented as an `ActionIntent`.
3. The intent is evaluated against the referenced Governed Contract.
4. `non_conformant`, `insufficient_evidence`, `not_yet_valid`, and `expired` MUST NOT be treated as eligible for consequence.
5. `conformant` means only that contract conformance succeeded. A separate authorization/enforcement boundary MUST still decide whether execution may occur.
6. The downstream system SHOULD produce a receipt binding the action to the contract digest and authorization decision.

## v0.1 portable transaction constraints

The reference profile recognizes:

- `max_amount`: numeric ceiling for `ActionIntent.attributes.amount`.
- `currency`: required transaction currency.

Missing or malformed required transaction attributes fail closed as `non_conformant`.

## Canonical demo

A buyer agent has a valid identity and an active mandate to purchase `catalog:item-42` for restocking. The contract ceiling is EUR 1,000. The seller proposes EUR 1,200.

```text
A2A transport                 SUCCESS
Identity/authentication       SUCCESS
Task understood               SUCCESS
Governed Contract             NON_CONFORMANT
Reason                        amount_exceeds_mandate
Execution authorization       NOT ELIGIBLE
Economic consequence          NO
```

The same interaction at EUR 900 is `conformant`, but still carries `authorization_required: true`. Contract conformance is deliberately separated from execution authorization.

## Interoperability boundary

The profile is vendor-neutral. Implementers may use any identity system, model, agent framework, policy engine, execution boundary, settlement system, or receipt store. Product-specific integrations belong behind adapters rather than in the portable contract.
