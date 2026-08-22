"""Conformance tests for the rights-lineage contract surface."""

from open_agent_contract.models import ContractClause, ContractClauseEntry
from open_agent_contract.rights import (
    RightsEvidenceStatus,
    RightsUseDecision,
    RightsUseProof,
    evaluate_rights_use,
)


def test_rights_lineage_is_distinct_clause_type():
    clause = ContractClauseEntry(
        clause_id="rights-1",
        clause_type=ContractClause.RIGHTS_LINEAGE,
        description="Preserve applicable rights across derivation",
        normative_text=(
            "Transformation, compression, distillation, transfer, replication or "
            "regeneration MUST NOT by themselves extinguish or broaden applicable rights."
        ),
        parameters={
            "source_ref": "artifact:source-1",
            "rights_holder_party_ids": ["party-1"],
            "permitted_use_classes": ["analyze_for_task"],
            "prohibited_use_classes": ["train_persistent_model"],
            "provenance_required": True,
            "derivative_restrictions_follow": True,
            "proof_before_use_required": True,
        },
    )

    assert clause.clause_type is ContractClause.RIGHTS_LINEAGE
    assert clause.parameters["provenance_required"] is True
    assert clause.parameters["derivative_restrictions_follow"] is True
    assert clause.parameters["proof_before_use_required"] is True


def test_technical_capability_does_not_imply_rights_permission():
    permitted = {"analyze_for_task"}
    requested = "train_persistent_model"

    assert requested not in permitted
    assert ContractClause.RIGHTS_LINEAGE.value == "rights_lineage"


def test_unknown_or_unresolved_rights_fail_closed():
    result = evaluate_rights_use(
        RightsUseProof(
            source_ref="artifact:source-1",
            claimant_party_id="agent-1",
            requested_use_class="train_persistent_model",
        )
    )
    assert result.decision is RightsUseDecision.DENY_OR_DEFER
    assert result.reason == "PROOF_REQUIRED_BEFORE_USE"


def test_self_asserted_basis_without_admitted_evidence_is_not_enough():
    result = evaluate_rights_use(
        RightsUseProof(
            source_ref="artifact:source-1",
            claimant_party_id="agent-1",
            requested_use_class="commercialize_derivative",
            rights_basis="license",
            evidence_refs=["claim:self-attested"],
            evidence_status=RightsEvidenceStatus.UNRESOLVED,
            permitted_use_classes=["commercialize_derivative"],
        )
    )
    assert result.decision is RightsUseDecision.DENY_OR_DEFER


def test_admitted_right_must_cover_exact_requested_use():
    result = evaluate_rights_use(
        RightsUseProof(
            source_ref="artifact:source-1",
            claimant_party_id="agent-1",
            requested_use_class="commercialize_derivative",
            rights_basis="license",
            evidence_refs=["license:123"],
            evidence_status=RightsEvidenceStatus.ADMITTED,
            permitted_use_classes=["analyze_for_task"],
        )
    )
    assert result.decision is RightsUseDecision.DENY
    assert result.reason == "REQUESTED_USE_OUTSIDE_PROVEN_SCOPE"


def test_admitted_right_for_exact_use_allows():
    result = evaluate_rights_use(
        RightsUseProof(
            source_ref="artifact:source-1",
            claimant_party_id="agent-1",
            requested_use_class="commercialize_derivative",
            rights_basis="license",
            evidence_refs=["license:123"],
            evidence_status=RightsEvidenceStatus.ADMITTED,
            permitted_use_classes=["commercialize_derivative"],
        )
    )
    assert result.decision is RightsUseDecision.ALLOW
    assert result.reason == "PROVEN_RIGHT_FOR_REQUESTED_USE"


def test_rejected_rights_basis_denies():
    result = evaluate_rights_use(
        RightsUseProof(
            source_ref="artifact:source-1",
            claimant_party_id="agent-1",
            requested_use_class="analyze_for_task",
            rights_basis="ownership",
            evidence_refs=["claim:rejected"],
            evidence_status=RightsEvidenceStatus.REJECTED,
            permitted_use_classes=["analyze_for_task"],
        )
    )
    assert result.decision is RightsUseDecision.DENY
    assert result.reason == "RIGHTS_BASIS_REJECTED"
