"""Canonical data models for verifiable agent contracts."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ContractStatus(str, Enum):
    """Lifecycle status of an agent contract."""
    DRAFT = "draft"
    PROPOSED = "proposed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    EXPIRED = "expired"


class ContractClause(str, Enum):
    """Standard clause types."""
    SCOPE = "scope"
    AUTHORITY = "authority"
    CONSTRAINT = "constraint"
    OBLIGATION = "obligation"
    PROHIBITION = "prohibition"
    PERMISSION = "permission"
    ESCALATION = "escalation"
    TERMINATION = "termination"
    PERSON_MODEL = "person_model"
    RIGHTS_LINEAGE = "rights_lineage"


class ContractParty(BaseModel):
    """A party to the contract — principal or agent."""
    party_id: str
    role: str  # "principal" | "agent" | "third_party"
    public_key: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContractClauseEntry(BaseModel):
    """A single clause in the contract."""
    clause_id: str
    clause_type: ContractClause
    description: str
    normative_text: str
    reht_requirement_id: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class AgentContract(BaseModel):
    """A verifiable contract between a principal and an agent."""
    contract_id: str
    version: str = "1.0.0"
    status: ContractStatus = ContractStatus.DRAFT
    principal: ContractParty
    agent: ContractParty
    clauses: list[ContractClauseEntry] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    activated_at: datetime | None = None
    expires_at: datetime | None = None
    signature_principal: str | None = None
    signature_agent: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContractEnforcement(BaseModel):
    """An enforcement action on a contract."""
    enforcement_id: str
    contract_id: str
    clause_id: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    evidence: dict[str, Any] = Field(default_factory=dict)
    receipt_id: str | None = None


class ContractViolation(BaseModel):
    """A recorded violation of a contract."""
    violation_id: str
    contract_id: str
    clause_id: str
    description: str
    severity: str = "warning"  # "info", "warning", "critical"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    evidence: dict[str, Any] = Field(default_factory=dict)
    remediated: bool = False
