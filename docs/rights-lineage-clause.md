# Rights-Lineage Clause v0

Status: draft standard clause for governed human↔AI and AI↔AI contracts.

This clause carries declared or otherwise applicable rights, restrictions and provenance obligations across transformations of source material. It does not determine whether a legal right exists and does not create copyright, trade-secret, confidentiality or other statutory rights by itself.

## Core invariant

> **Derivation does not extinguish applicable rights.**

Transformation, summarization, embedding, compression, distillation, fine-tuning, model transfer, synthesis, clone, fork, merge, regeneration, replication or format conversion MUST NOT by themselves be treated as extinguishing rights, restrictions or provenance obligations that still apply to materially derived representations.

The rule is directional-neutral: it applies to human→AI, AI→human and AI→AI exchanges.

## Clause type

Use `ContractClause.RIGHTS_LINEAGE`.

A conformant clause SHOULD carry parameters equivalent to:

```json
{
  "source_ref": "artifact:example",
  "rights_holder_party_ids": ["party-1"],
  "asserted_rights_bases": ["copyright", "contract"],
  "permitted_use_classes": ["analyze_for_task"],
  "prohibited_use_classes": ["train_persistent_model", "redistribute_derivative"],
  "permitted_recipients": ["agent-1"],
  "provenance_required": true,
  "derivative_restrictions_follow": true,
  "multiplication_requires_permission": true,
  "commercialization_requires_permission": true,
  "revocable_where_applicable": true
}
```

## Mandatory semantics

1. **TRANSFORMATION_NE_RIGHTS_EXTINCTION** — a technical transformation MUST NOT be treated as proof that applicable rights or restrictions disappeared.
2. **COMPRESSION_NE_RIGHTS_EXTINCTION** — reducing a source to an embedding, latent state, distilled representation, compact model or other compressed form MUST NOT by itself clear lineage obligations.
3. **TRANSFER_NE_RIGHTS_EXTINCTION** — transfer to another agent, model, provider, runtime or human recipient MUST NOT by itself broaden rights.
4. **REGENERATION_NE_RIGHTS_EXTINCTION** — reconstructing function or content from a derived representation MUST NOT reset provenance or permissions.
5. **MULTIPLICATION_NE_PERMISSION** — the ability to copy, replicate, fork or scale a representation MUST NOT create permission to do so.
6. **CAPABILITY_NE_LICENSE** — technical capability to access, infer, reproduce or transform material MUST NOT be interpreted as a license.
7. **DERIVATIVE_RESTRICTIONS_FOLLOW** — where the governing rights or contract require it, restrictions MUST follow materially derived descendants even when the original bytes are absent.
8. **PROVENANCE_PERSISTS** — a system claiming compliance MUST preserve enough lineage to evaluate whether a proposed downstream use remains within the declared rights boundary.
9. **NO_RIGHTS_LAUNDERING_BY_AGENT_CHAIN** — routing material through additional agents or models MUST NOT be used to erase or broaden restrictions.
10. **NO_ASSUMED_OWNERSHIP_OF_OUTPUT** — receipt of an AI-generated output MUST NOT by itself be treated as proof that all upstream rights have been cleared.

## Standard use classes

Examples include:

- `analyze_for_task`
- `transform_for_task`
- `generate_derivative`
- `train_persistent_model`
- `distill_into_model`
- `build_person_model`
- `redistribute_source`
- `redistribute_derivative`
- `share_with_agent`
- `commercialize_derivative`
- `replicate_at_scale`

Permission for one use class MUST NOT imply permission for another.

## Relationship to person-model governance

A person-specific cognitive or behavioural model can simultaneously be governed by `PERSON_MODEL` and `RIGHTS_LINEAGE` clauses.

Example: a contract may permit transient assistance using a person's writings while denying persistent person-model construction, model training, redistribution and commercial reuse. The fact that the writings were transformed into embeddings or distilled into a model does not by itself remove either restriction.

## Recommended normative text

`Applicable rights, restrictions and provenance obligations attached to Source Material MUST remain evaluable across materially derived representations. Transformation, compression, distillation, transfer, replication, model incorporation or regeneration MUST NOT by themselves be treated as extinguishing or broadening those rights. Technical capability does not constitute permission or license. Downstream use MUST remain within the current authorized rights scope, and agent-to-agent transfer MUST preserve the relevant rights lineage.`

## Enforcement

A consequence boundary SHOULD evaluate the requested rights use class separately from the technical action.

Examples:

- `read_document` may be permitted while `train_persistent_model` is denied;
- `summarize_document` may be permitted while `redistribute_derivative` is denied;
- `generate_code` may be permitted while `commercialize_derivative` remains unresolved;
- `share_with_agent` may be permitted only if the downstream agent receives and honors the same lineage obligations.

Failing to resolve required rights or provenance before a consequence-bearing use SHOULD produce deny, defer or escalation according to governing policy.
