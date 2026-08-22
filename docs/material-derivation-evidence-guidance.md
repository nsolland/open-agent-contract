# Material Derivation Evidence Guidance v0

Status: provisional guidance, not a fixed legal or conformance test.

This guidance exists because rights-lineage can become either ineffective or overbroad if `materially derived` is treated as self-evident.

## Stable rules

```text
similarity != derivation
access != derivation
chronology != derivation
provenance != legal truth
self-assertion != proof
unknown provenance != free use where clearance is required
```

A rights-sensitive use SHOULD rely on an admitted evidentiary decision rather than a single similarity score.

A provisional prima-facie case MAY consider, together:

1. prior existence of the asserted source;
2. plausible access/exposure before the challenged descendant;
3. source-specific correspondence beyond topic/style/common-knowledge/common-function baselines;
4. materiality to the relevant downstream use.

No single factor is sufficient by itself.

If a prima-facie case is admitted, governing policy MAY place the next evidentiary burden on the proposed user to establish a lawful basis for the exact use, independent creation, alternative provenance, convincing non-derivation evidence, or another applicable rebuttal.

No universal numeric threshold is defined by this contract. Thresholds for bytes, tokens, similarity, embedding distance, information contribution or economic materiality require empirical and jurisdiction-specific calibration.

## Required blindspot protections

- **LAWFUL_BASIS_NE_OWNERSHIP_ONLY** — lawful use may rest on ownership, licence, mandate, statutory permission/exception/limitation or another admitted basis.
- **SIMILARITY_NE_DERIVATION** — similarity alone MUST NOT establish derivation.
- **INDEPENDENT_CREATION_ADMISSIBLE** — independent creation and alternative provenance MUST remain admissible rebuttals.
- **APPLICABLE_RIGHTS_FOLLOW_LINEAGE** — only rights/restrictions that remain applicable follow lineage; expiry, waiver, transfer, lawful exception or superseding agreement may change state.
- **SELF_ASSERTION_NE_PROOF** — bare rights claims MUST NOT establish standing or clearance.
- **PROVENANCE_NE_TRUTH** — provenance integrity and legal/factual truth are distinct.
- **PROVE_RIGHT_NE_DISCLOSE_ALL** — proof SHOULD support selective disclosure and avoid unnecessary exposure of source material, identity, contracts, trade secrets or full upstream lineage.
- **TRAINING_NE_OUTPUT_RIGHTS** — input/training rights, a particular output's status, and downstream redistribution/commercialization rights MUST be evaluated separately where relevant.
- **JURISDICTION_BOUND** — the contract MUST NOT make universal copyrightability, infringement or ownership determinations.
- **NO_RIGHTS_ANTICOMMONS** — only materially operative rights for the requested use SHOULD require resolution; unrelated ancestry MUST NOT require consent merely because it exists.
- **SCALABLE_CLEARANCE** — implementations SHOULD support machine-readable grants, aggregation, attestations, cached admitted rights state and escalation only for materially unresolved cases.

## Experimental status

The prima-facie factors and burden-shift model MUST be treated as revisable. They SHOULD be tested against exact copies, paraphrase, structural reconstruction, independent same-function creation, topic/style negatives, common-knowledge controls, multi-source composition, very small exposures, long transformation chains, provenance stripping and adversarial false claims.

False positives, false negatives, calibration, dispute quality and clearance cost are first-class evaluation metrics.
