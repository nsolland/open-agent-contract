"""Contract tests for inferred person-model governance."""

from open_agent_contract.models import ContractClause, ContractClauseEntry


def test_person_model_clause_type_is_available():
    assert ContractClause.PERSON_MODEL.value == "person_model"


def test_person_model_clause_preserves_explicit_use_boundaries():
    clause = ContractClauseEntry(
        clause_id="pm-001",
        clause_type=ContractClause.PERSON_MODEL,
        description="Govern inferred person-specific models",
        normative_text="Predicted approval does not constitute consent.",
        parameters={
            "subject_party_id": "principal-1",
            "derivation_allowed": True,
            "retention_allowed": False,
            "permitted_use_classes": ["assist_subject"],
            "prohibited_use_classes": ["political_influence", "influence_subject"],
            "derivative_restrictions_follow": True,
        },
    )

    assert clause.clause_type is ContractClause.PERSON_MODEL
    assert clause.parameters["retention_allowed"] is False
    assert "political_influence" in clause.parameters["prohibited_use_classes"]
    assert "influence_subject" not in clause.parameters["permitted_use_classes"]
    assert clause.parameters["derivative_restrictions_follow"] is True
