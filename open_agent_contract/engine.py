"""Contract lifecycle management and enforcement engine."""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
from typing import Any

from .models import (
    AgentContract,
    ContractClauseEntry,
    ContractClause,
    ContractEnforcement,
    ContractParty,
    ContractStatus,
    ContractViolation,
)


class ContractEngine:
    """Manages the lifecycle and enforcement of agent contracts."""

    def __init__(self) -> None:
        self._contracts: dict[str, AgentContract] = {}
        self._enforcements: list[ContractEnforcement] = []
        self._violations: list[ContractViolation] = []

    # -- Lifecycle --

    def create_contract(
        self,
        contract_id: str,
        principal: ContractParty,
        agent: ContractParty,
        clauses: list[ContractClauseEntry] | None = None,
        expires_at: datetime | None = None,
    ) -> AgentContract:
        if contract_id in self._contracts:
            raise ValueError(f"Contract {contract_id} already exists")
        contract = AgentContract(
            contract_id=contract_id,
            principal=principal,
            agent=agent,
            clauses=clauses or [],
            expires_at=expires_at,
        )
        self._contracts[contract_id] = contract
        return contract

    def get_contract(self, contract_id: str) -> AgentContract | None:
        return self._contracts.get(contract_id)

    def list_contracts(self, status: ContractStatus | None = None) -> list[AgentContract]:
        contracts = list(self._contracts.values())
        if status:
            contracts = [c for c in contracts if c.status == status]
        return sorted(contracts, key=lambda c: c.created_at, reverse=True)

    def propose_contract(self, contract_id: str) -> AgentContract | None:
        contract = self._contracts.get(contract_id)
        if contract is None or contract.status != ContractStatus.DRAFT:
            return None
        contract.status = ContractStatus.PROPOSED
        return contract

    def activate_contract(
        self,
        contract_id: str,
        sig_principal: str,
        sig_agent: str,
    ) -> AgentContract | None:
        contract = self._contracts.get(contract_id)
        if contract is None or contract.status != ContractStatus.PROPOSED:
            return None
        contract.status = ContractStatus.ACTIVE
        contract.activated_at = datetime.utcnow()
        contract.signature_principal = sig_principal
        contract.signature_agent = sig_agent
        return contract

    def suspend_contract(self, contract_id: str) -> AgentContract | None:
        contract = self._contracts.get(contract_id)
        if contract is None or contract.status != ContractStatus.ACTIVE:
            return None
        contract.status = ContractStatus.SUSPENDED
        return contract

    def terminate_contract(self, contract_id: str) -> AgentContract | None:
        contract = self._contracts.get(contract_id)
        if contract is None:
            return None
        contract.status = ContractStatus.TERMINATED
        return contract

    # -- Clauses --

    def add_clause(self, contract_id: str, clause: ContractClauseEntry) -> AgentContract | None:
        contract = self._contracts.get(contract_id)
        if contract is None:
            return None
        contract.clauses.append(clause)
        return contract

    def get_clauses_by_type(self, contract_id: str, clause_type: ContractClause) -> list[ContractClauseEntry]:
        contract = self._contracts.get(contract_id)
        if contract is None:
            return []
        return [c for c in contract.clauses if c.clause_type == clause_type]

    # -- Enforcement --

    def record_enforcement(self, enforcement: ContractEnforcement) -> ContractEnforcement:
        self._enforcements.append(enforcement)
        return enforcement

    def list_enforcements(self, contract_id: str) -> list[ContractEnforcement]:
        return [e for e in self._enforcements if e.contract_id == contract_id]

    # -- Violations --

    def record_violation(self, violation: ContractViolation) -> ContractViolation:
        self._violations.append(violation)
        return violation

    def list_violations(
        self, contract_id: str | None = None, severity: str | None = None
    ) -> list[ContractViolation]:
        results = list(self._violations)
        if contract_id:
            results = [v for v in results if v.contract_id == contract_id]
        if severity:
            results = [v for v in results if v.severity == severity]
        return results

    # -- Verification --

    def verify_contract_integrity(self, contract_id: str) -> dict[str, Any]:
        """Verify the integrity of a contract."""
        contract = self._contracts.get(contract_id)
        if contract is None:
            return {"valid": False, "reason": "Contract not found"}
        issues = []
        if contract.status == ContractStatus.ACTIVE:
            if not contract.signature_principal or not contract.signature_agent:
                issues.append("Active contract missing signatures")
            if contract.expires_at and contract.expires_at < datetime.utcnow():
                issues.append("Contract has expired")
        # Check for REHT requirement references
        req_ids = []
        for clause in contract.clauses:
            if clause.reht_requirement_id:
                req_ids.append(clause.reht_requirement_id)
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "clause_count": len(contract.clauses),
            "reht_requirements": req_ids,
            "status": contract.status.value,
        }

    @staticmethod
    def digest_contract(contract: AgentContract) -> str:
        """Compute a SHA-256 digest of the contract for signing."""
        canonical = (
            f"{contract.contract_id}:{contract.version}:"
            f"{contract.principal.party_id}:{contract.agent.party_id}:"
            f"{'|'.join(c.clause_id for c in sorted(contract.clauses, key=lambda x: x.clause_id))}"
        )
        return sha256(canonical.encode()).hexdigest()
