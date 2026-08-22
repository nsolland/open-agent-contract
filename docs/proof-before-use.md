# Proof-Before-Use v0

Status: normative companion to `RIGHTS_LINEAGE`.

This rule makes rights-lineage operational. It does not determine legal ownership, copyrightability, validity of a licence, or the existence of a statutory exception. It defines which party bears the burden inside a governed AI/agent contract before a rights-sensitive use is permitted.

## Core invariant

> **Before use, prove the right to use.**

Equivalent negative rules:

```text
access             != licence
exposure           != derivation right
possession         != permission
unknown provenance != free use
self-assertion     != admitted proof
capability         != rights clearance
```

The party proposing to derive, train, distill, retain, replicate, transfer, redistribute, commercialize or otherwise exploit a representation MUST provide admitted evidence of a valid basis for the exact requested use when rights clearance is required.

## Burden rule

The burden rests on the party requesting the use. A creator or upstream rights holder MUST NOT be required by the contract surface to prove infringement before the system asks whether the proposed user can prove authorization.

A conformant governed flow therefore evaluates:

```text
proposed use
  -> source / lineage reference
  -> claimed rights basis
  -> evidence supporting that basis
  -> evidence admission status
  -> exact permitted use scope
  -> ALLOW | DENY | DENY_OR_DEFER
```

## Accepted basis classes

Examples may include:

- ownership;
- licence;
- mandate or delegation;
- contractual grant;
- statutory exception or limitation;
- public-domain status;
- another admitted authorized basis.

A label is not proof. The basis must be supported by evidence admitted through the governing evidence process.

## Mandatory semantics

1. **PROOF_BEFORE_USE** — a rights-sensitive use requiring clearance MUST NOT proceed before the relevant right-to-use has been evidenced and admitted.
2. **BURDEN_ON_PROPOSED_USER** — the party requesting the use bears the burden of supplying the evidence required for clearance.
3. **UNKNOWN_PROVENANCE_NE_PERMISSION** — missing or unknown lineage MUST NOT be interpreted as unencumbered material.
4. **SELF_ASSERTION_NE_PROOF** — a party's own claim of ownership, licence or permission MUST NOT by itself establish clearance.
5. **EXACT_USE_SCOPE_REQUIRED** — proof for one use class MUST NOT authorize a different use class.
6. **REJECTED_BASIS_DENIES** — rejected evidence or a rejected rights basis MUST produce `DENY` for the covered use.
7. **UNRESOLVED_BASIS_FAILS_CLOSED** — missing, stale, conflicting or unresolved evidence MUST produce `DENY_OR_DEFER` rather than implied permission.
8. **PROOF_FOLLOWS_LINEAGE** — downstream agents receiving materially derived representations inherit the obligation to establish their own right for the proposed downstream use; upstream technical transfer is not clearance.

## Reference implementation

`open_agent_contract.rights.evaluate_rights_use()` provides a deterministic reference evaluator.

It returns `ALLOW` only when:

- a rights basis is declared;
- supporting evidence references are present;
- the evidence status is `admitted`; and
- the exact requested use is inside the admitted scope.

The `admitted` state is a governance/admission result, not a claimant self-declaration and not a legal judgment by the library.

## Relationship to rights-lineage

`RIGHTS_LINEAGE` answers: **do applicable rights survive transformation?**

`PROOF_BEFORE_USE` answers: **who must demonstrate permission before the next use?**

Together:

> **Exposure does not grant derivation rights. Derivation does not extinguish applicable rights. Rights follow lineage. Before use, prove the right to use.**
