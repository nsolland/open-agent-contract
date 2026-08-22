"""Conformance tests for the rights-lineage contract surface."""

from open_agent_contract.models import ContractClause, ContractClauseEntry


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
        },
    )

    assert clause.clause_type is ContractClause.RIGHTS_LINEAGE
    assert clause.parameters["provenance_required"] is True
    assert clause.parameters["derivative_restrictions_follow"] is True


def test_technical_capability_does_not_imply_rights_permission():
    permitted = {"analyze_for_task"}
    requested = "train_persistent_model"

    assert requested not in permitted
    assert ContractClause.RIGHTS_LINEAGE.value == "rights_lineage"
