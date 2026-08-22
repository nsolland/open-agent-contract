# Inferred Person-Model Clause v0

Status: draft standard clause for human-AI contracts.

This clause governs person-specific representations inferred by an agent or service from a human principal's traces. It is model-, provider- and implementation-neutral.

## Core rule

The ability to infer a model of the principal does not grant the agent authority to retain, share, simulate, influence or act as the principal.

Predicted preference is not consent.

## Clause type

Use `ContractClause.PERSON_MODEL`.

A conformant clause SHOULD carry parameters equivalent to:

```json
{
  "subject_party_id": "principal-1",
  "derivation_allowed": false,
  "retention_allowed": false,
  "permitted_use_classes": [],
  "prohibited_use_classes": ["political_influence"],
  "permitted_recipients": [],
  "retention_until": null,
  "revocable": true,
  "evidence_required": true,
  "derivative_restrictions_follow": true
}
```

## Standard use classes

- `assist_subject` — use for work requested by the principal.
- `predict_subject` — predict or simulate the principal's likely response or choice.
- `personalize_content` — adapt ranking, content or presentation to the principal.
- `influence_subject` — optimize information, argument, timing, channel or context to alter judgement or behaviour.
- `political_influence` — individualized political persuasion, demobilization, trust manipulation or voting-behaviour optimization.
- `share_person_model` — disclose or transfer the model or a materially equivalent representation.

Authority for one use class MUST NOT imply authority for another.

## Mandatory semantics

1. `derivation_allowed=false` means the agent MUST NOT intentionally build or persist a person-specific model beyond transient inference strictly necessary for otherwise authorized execution.
2. `retention_allowed=false` means a person-specific representation MUST NOT be persisted after the authorized task boundary.
3. `predict_subject`, `personalize_content`, `influence_subject` and `share_person_model` require explicit inclusion in `permitted_use_classes` when used as persistent person-model operations.
4. `political_influence` MUST remain prohibited in this profile and MUST NOT be enabled by generic consent, terms-of-service acceptance or an inferred preference.
5. A person-model or its output MUST NOT serve as consent, delegation, authorization or authority evidence merely because it predicts that the principal would approve.
6. Restrictions MUST follow materially person-specific descendants across embedding, compression, transformation, transfer, clone, fork, merge or model swap.
7. Revocation MUST make the representation non-operative for revoked uses even when technical copies remain.
8. The agent MUST NOT claim identity, ownership or principal authority from predictive fidelity.

## Recommended normative text

`The Agent MUST treat any materially person-specific cognitive, behavioural, preference, response-prediction or simulation model inferred from the Principal as subject-linked governed state. Derivation does not create authority. Predicted approval does not constitute consent or delegation. The Agent MUST NOT retain, disclose, simulate, personalize against, or use such a model to influence the Principal except for use classes explicitly authorized by this Contract and current governing policy. Individualized political influence is prohibited. Restrictions and revocation follow materially equivalent derived representations.`

## Enforcement

A consequence gate SHOULD evaluate the requested person-model use class separately from the business action itself.

Examples:

- `send_email` may be authorized while `influence_subject` is denied;
- `recommend_product` may be authorized while persistent `predict_subject` is denied;
- `summarize_preferences_for_user` may be authorized while `share_person_model` is denied.

This prevents ordinary task authorization from silently becoming authorization to construct or exploit a behavioural digital twin.
