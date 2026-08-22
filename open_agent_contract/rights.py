"""Deterministic proof-before-use evaluation for rights-lineage contracts.

This module does not determine legal ownership or copyrightability. It evaluates
whether a governed contract has admitted evidence of a right to perform the
specific requested use.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class RightsEvidenceStatus(str, Enum):
    """Admission status of the evidence supporting a claimed right to use."""

    ADMITTED = "admitted"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"


class RightsUseDecision(str, Enum):
    """Deterministic contract decision for a proposed rights-sensitive use."""

    ALLOW = "allow"
    DENY = "deny"
    DENY_OR_DEFER = "deny_or_defer"


class RightsUseProof(BaseModel):
    """Evidence-bound claim that a party may perform one or more use classes."""

    source_ref: str
    claimant_party_id: str
    requested_use_class: str
    rights_basis: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    evidence_status: RightsEvidenceStatus = RightsEvidenceStatus.UNRESOLVED
    permitted_use_classes: list[str] = Field(default_factory=list)
    lineage_ref: str | None = None


class RightsUseEvaluation(BaseModel):
    """Result of proof-before-use evaluation."""

    decision: RightsUseDecision
    reason: str


def evaluate_rights_use(proof: RightsUseProof) -> RightsUseEvaluation:
    """Fail closed unless admitted evidence proves the exact requested use.

    `ADMITTED` means admitted by the governing evidence/admission process. It is
    not a declaration by the claimant and is not itself a legal judgment.
    """

    if proof.evidence_status is RightsEvidenceStatus.REJECTED:
        return RightsUseEvaluation(
            decision=RightsUseDecision.DENY,
            reason="RIGHTS_BASIS_REJECTED",
        )

    if (
        proof.evidence_status is not RightsEvidenceStatus.ADMITTED
        or not proof.rights_basis
        or not proof.evidence_refs
    ):
        return RightsUseEvaluation(
            decision=RightsUseDecision.DENY_OR_DEFER,
            reason="PROOF_REQUIRED_BEFORE_USE",
        )

    if proof.requested_use_class not in proof.permitted_use_classes:
        return RightsUseEvaluation(
            decision=RightsUseDecision.DENY,
            reason="REQUESTED_USE_OUTSIDE_PROVEN_SCOPE",
        )

    return RightsUseEvaluation(
        decision=RightsUseDecision.ALLOW,
        reason="PROVEN_RIGHT_FOR_REQUESTED_USE",
    )
