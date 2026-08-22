# Rights-Lineage Clause v0

Status: draft standard clause for governed human↔AI and AI↔AI contracts.

This clause carries declared or otherwise applicable rights, restrictions and provenance obligations across transformations of source material. It does not determine whether a legal right exists and does not create copyright, trade-secret, confidentiality or other statutory rights by itself.

## Core invariants

> **Applicable rights follow lineage while they remain applicable.**

> **Before a rights-sensitive use, establish a valid basis for that exact use.**

Transformation, summarization, embedding, compression, distillation, fine-tuning, model transfer, synthesis, clone, fork, merge, regeneration, replication or format conversion MUST NOT by themselves be treated as extinguishing rights, restrictions or provenance obligations that still apply to materially derived representations.

The rule is direction-neutral: it applies to human→AI, AI→human and AI→AI exchanges.

A valid basis is broader than ownership or express licence. Depending on governing law, contract and policy it MAY include ownership, licence, mandate, statutory permission, exception, limitation or another admitted lawful basis.

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
7. **DERIVATIVE_RESTRICTIONS_FOLLOW** — where the governing rights or contract require it, applicable restrictions MUST follow materially derived descendants even when the original bytes are absent.
8. **PROVENANCE_PERSISTS** — a system claiming compliance MUST preserve enough lineage to evaluate whether a proposed downstream use remains within the declared rights boundary.
9. **NO_RIGHTS_LAUNDERING_BY_AGENT_CHAIN** — routing material through additional agents or models MUST NOT be used to erase or broaden restrictions.
10. **NO_ASSUMED_OWNERSHIP_OF_OUTPUT** — receipt of an AI-generated output MUST NOT by itself be treated as proof that all upstream rights have been cleared.
11. **PROOF_BEFORE_USE** — where clearance is required, the proposed user MUST establish an admitted valid basis for the exact use before that use is permitted.
12. **SELF_ASSERTION_NE_PROOF** — self-asserted ownership, licence, mandate or permission MUST NOT by itself establish clearance.
13. **SIMILARITY_NE_DERIVATION** — similarity, stylistic resemblance or functional equivalence alone MUST NOT establish material derivation.
14. **INDEPENDENT_CREATION_ADMISSIBLE** — independent creation and alternative provenance MUST remain admissible evidence where derivation is disputed.
15. **PROVENANCE_NE_TRUTH** — provenance integrity MUST remain distinct from legal standing, rights applicability and external truth.
16. **PROVE_RIGHT_NE_DISCLOSE_ALL** — proof mechanisms SHOULD permit selective disclosure and avoid unnecessary disclosure of source material, identities, contract terms, trade secrets or complete upstream lineage.
17. **TRAINING_NE_OUTPUT_RIGHTS** — input/access/training rights, the status of a particular descendant, and rights to redistribute/commercialize that descendant MUST remain separately evaluable where relevant.
18. **JURISDICTION_BOUND** — contract conformance MUST NOT be represented as a universal copyrightability, ownership or infringement determination.
19. **NO_RIGHTS_ANTICOMMONS** — only rights materially operative for the exact requested use SHOULD require resolution; irrelevant ancestry MUST NOT become a veto merely because it exists.
20. **SCALABLE_CLEARANCE** — implementations SHOULD support machine-readable grants, aggregation, attestations and cached admitted rights state so lawful machine use does not require per-item or per-token human adjudication.

## Material derivation

This contract deliberately defines no universal material-derivation threshold.

No fixed byte count, token count, similarity score, embedding distance, information contribution or economic threshold is normative in v0.

Provisional evidence guidance is in `docs/material-derivation-evidence-guidance.md`. It is explicitly revisable and MUST NOT be treated as a settled legal test.

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

`Applicable rights, restrictions and provenance obligations attached to Source Material MUST remain evaluable across materially derived representations while those rights remain applicable. Transformation, compression, distillation, transfer, replication, model incorporation or regeneration MUST NOT by themselves be treated as extinguishing or broadening those rights. Technical capability does not constitute permission or license. Before a rights-sensitive downstream use, the proposed user MUST establish an admitted valid basis covering the exact requested use. Similarity alone does not establish derivation, self-assertion does not establish rights, and unresolved required rights state does not become permission.`

## Enforcement

A consequence boundary SHOULD evaluate the requested rights use class separately from the technical action.

Examples:

- `read_document` may be permitted while `train_persistent_model` is denied;
- `summarize_document` may be permitted while `redistribute_derivative` is denied;
- `generate_code` may be permitted while `commercialize_derivative` remains unresolved;
- `share_with_agent` may be permitted only if the downstream agent receives and honors the same lineage obligations;
- an admitted statutory exception may establish a valid basis for one use without granting unrelated commercialization rights.

Failing to resolve required rights or provenance before a consequence-bearing use SHOULD produce deny, defer or escalation according to governing policy.
