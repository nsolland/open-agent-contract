"""Tests for open-agent-contract."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from open_agent_contract.engine import ContractEngine
from open_agent_contract.models import (
    AgentContract,
    ContractClause,
    ContractClauseEntry,
    ContractEnforcement,
    ContractParty,
    ContractStatus,
    ContractViolation,
)


@pytest.fixture
def engine() -> ContractEngine:
    return ContractEngine()


@pytest.fixture
def principal() -> ContractParty:
    return ContractParty(party_id="principal-1", role="principal", public_key="pk_principal")


@pytest.fixture
def agent() -> ContractParty:
    return ContractParty(party_id="agent-1", role="agent", public_key="pk_agent")


class TestContractLifecycle:
    def test_create_contract(self, engine, principal, agent):
        contract = engine.create_contract("c1", principal, agent)
        assert contract.contract_id == "c1"
        assert contract.status == ContractStatus.DRAFT

    def test_create_duplicate(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        with pytest.raises(ValueError, match="already exists"):
            engine.create_contract("c1", principal, agent)

    def test_get_contract(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        c = engine.get_contract("c1")
        assert c is not None
        assert c.contract_id == "c1"

    def test_get_nonexistent(self, engine):
        assert engine.get_contract("nonexistent") is None

    def test_list_contracts(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        engine.create_contract("c2", principal, agent)
        assert len(engine.list_contracts()) == 2

    def test_list_contracts_filter_status(self, engine, principal, agent):
        c1 = engine.create_contract("c1", principal, agent)
        c2 = engine.create_contract("c2", principal, agent)
        c1.status = ContractStatus.ACTIVE
        active = engine.list_contracts(status=ContractStatus.ACTIVE)
        assert len(active) == 1
        assert active[0].contract_id == "c1"

    def test_full_lifecycle(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        assert engine.propose_contract("c1").status == ContractStatus.PROPOSED
        assert engine.activate_contract("c1", "sig_p", "sig_a").status == ContractStatus.ACTIVE
        assert engine.suspend_contract("c1").status == ContractStatus.SUSPENDED
        assert engine.terminate_contract("c1").status == ContractStatus.TERMINATED

    def test_activate_from_wrong_state(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        assert engine.activate_contract("c1", "s1", "s2") is None  # still DRAFT


class TestClauses:
    def test_add_clause(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        clause = ContractClauseEntry(
            clause_id="cl1",
            clause_type=ContractClause.SCOPE,
            description="Scope of work",
            normative_text="Agent MUST operate within defined scope",
            reht_requirement_id="REHT-001",
        )
        updated = engine.add_clause("c1", clause)
        assert updated is not None
        assert len(updated.clauses) == 1

    def test_add_clause_nonexistent(self, engine, principal, agent):
        clause = ContractClauseEntry(
            clause_id="cl1", clause_type=ContractClause.SCOPE,
            description="test", normative_text="test",
        )
        assert engine.add_clause("nonexistent", clause) is None

    def test_get_clauses_by_type(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        engine.add_clause("c1", ContractClauseEntry(clause_id="cl1", clause_type=ContractClause.SCOPE, description="s", normative_text="t"))
        engine.add_clause("c1", ContractClauseEntry(clause_id="cl2", clause_type=ContractClause.AUTHORITY, description="a", normative_text="t"))
        engine.add_clause("c1", ContractClauseEntry(clause_id="cl3", clause_type=ContractClause.SCOPE, description="s2", normative_text="t"))
        scopes = engine.get_clauses_by_type("c1", ContractClause.SCOPE)
        assert len(scopes) == 2


class TestEnforcement:
    def test_record_enforcement(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        enforcement = ContractEnforcement(
            enforcement_id="e1", contract_id="c1",
            clause_id="cl1", action="check_compliance",
        )
        engine.record_enforcement(enforcement)
        enforcements = engine.list_enforcements("c1")
        assert len(enforcements) == 1

    def test_record_violation(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        violation = ContractViolation(
            violation_id="v1", contract_id="c1",
            clause_id="cl1", description="Scope exceeded",
            severity="critical",
        )
        engine.record_violation(violation)
        violations = engine.list_violations(contract_id="c1")
        assert len(violations) == 1

    def test_list_violations_filter_severity(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        engine.record_violation(ContractViolation(violation_id="v1", contract_id="c1", clause_id="cl1", description="warn", severity="warning"))
        engine.record_violation(ContractViolation(violation_id="v2", contract_id="c1", clause_id="cl1", description="crit", severity="critical"))
        crits = engine.list_violations(severity="critical")
        assert len(crits) == 1


class TestVerification:
    def test_verify_integrity(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        result = engine.verify_contract_integrity("c1")
        assert result["valid"] is True
        assert result["status"] == "draft"

    def test_verify_active_missing_sig(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        engine.propose_contract("c1")
        engine.activate_contract("c1", "sig_p", "sig_a")
        result = engine.verify_contract_integrity("c1")
        assert result["valid"] is True

    def test_verify_not_found(self, engine):
        result = engine.verify_contract_integrity("nonexistent")
        assert result["valid"] is False

    def test_digest(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        contract = engine.get_contract("c1")
        digest = ContractEngine.digest_contract(contract)
        assert len(digest) == 64  # SHA-256 hex
        assert isinstance(digest, str)

    def test_digest_deterministic(self, engine, principal, agent):
        engine.create_contract("c1", principal, agent)
        contract = engine.get_contract("c1")
        d1 = ContractEngine.digest_contract(contract)
        d2 = ContractEngine.digest_contract(contract)
        assert d1 == d2
