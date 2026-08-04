"""Canonical contract for isolated, short-lived acquisition agents.

This module composes existing VALO controls. It does not authorize execution.
REHT clears actions, RACS expresses the deterministic decision contract, the
gateway enforces it, and Veritas records the outcome.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _require_aware(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include a timezone")
    return value


def _explicit_values(values: list[str], field_name: str) -> list[str]:
    cleaned = [value.strip() for value in values]
    if any(not value for value in cleaned):
        raise ValueError(f"{field_name} cannot contain empty values")
    if any(value == "*" or value.endswith(":*") for value in cleaned):
        raise ValueError(f"{field_name} must be explicit; wildcards are forbidden")
    if len(cleaned) != len(set(cleaned)):
        raise ValueError(f"{field_name} cannot contain duplicates")
    return cleaned


class EphemeralAgentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    DELETED = "deleted"


class IsolationClass(str, Enum):
    PROCESS = "process"
    CONTAINER = "container"
    VM = "vm"
    HARDWARE = "hardware"


class DeliveryMode(str, Enum):
    MINIMAL_EVIDENCE = "minimal_evidence"
    AGGREGATED_ANSWER = "aggregated_answer"
    REDACTED_ARTIFACT = "redacted_artifact"


class AgentOrigin(BaseModel):
    model_config = ConfigDict(frozen=True)

    principal_id: str
    requesting_agent_id: str
    request_id: str
    parent_contract_id: str | None = None
    delegation_chain_id: str
    delegation_chain_digest: str


class NeedToAskAcquireBinding(BaseModel):
    """Proof that the need was separately evaluated, cleared and bound."""

    model_config = ConfigDict(frozen=True)

    ask_request_id: str
    ask_reason: str
    acquire_decision_id: str
    acquisition_agent_id: str
    reht_clearance_id: str
    racs_decision_id: str
    gateway_policy_id: str
    veritas_stream_id: str


class BoundedMandate(BaseModel):
    model_config = ConfigDict(frozen=True)

    purpose: str
    task_scope: list[str] = Field(min_length=1)
    allowed_sources: list[str] = Field(min_length=1)
    allowed_tools: list[str] = Field(default_factory=list)
    allowed_resources: list[str] = Field(default_factory=list)
    prohibited_actions: list[str] = Field(default_factory=list)
    max_actions: int = Field(default=1, gt=0, le=10_000)
    allow_further_delegation: bool = False

    @field_validator(
        "task_scope",
        "allowed_sources",
        "allowed_tools",
        "allowed_resources",
        "prohibited_actions",
    )
    @classmethod
    def explicit_scope(cls, values: list[str], info: Any) -> list[str]:
        return _explicit_values(values, info.field_name)

    @model_validator(mode="after")
    def forbid_redelegation(self) -> "BoundedMandate":
        if self.allow_further_delegation:
            raise ValueError("isolated ephemeral agents cannot further delegate")
        return self


class IsolationBoundary(BaseModel):
    model_config = ConfigDict(frozen=True)

    silo_id: str
    isolation_class: IsolationClass = IsolationClass.CONTAINER
    gateway_enforcement_id: str
    credential_broker_ref: str | None = None
    network_egress_allowlist: list[str] = Field(default_factory=list)
    cross_silo_access: bool = False
    raw_credentials_exposed: bool = False

    @field_validator("network_egress_allowlist")
    @classmethod
    def explicit_egress(cls, values: list[str], info: Any) -> list[str]:
        return _explicit_values(values, info.field_name)

    @model_validator(mode="after")
    def enforce_boundary(self) -> "IsolationBoundary":
        if self.cross_silo_access:
            raise ValueError("cross-silo access is forbidden")
        if self.raw_credentials_exposed:
            raise ValueError("raw credentials cannot be exposed to the agent")
        return self


class OperatingMemoryLease(BaseModel):
    model_config = ConfigDict(frozen=True)

    owner_id: str
    provenance_refs: list[str] = Field(min_length=1)
    allowed_readers: list[str] = Field(min_length=1)
    allowed_writers: list[str] = Field(default_factory=list)
    memory_classes: list[str] = Field(default_factory=list)
    max_bytes: int = Field(gt=0)
    retention_until: datetime
    delete_on_termination: bool = True
    writeback_to_canonical_memory: bool = False
    zero_mem_receipt_required: bool = True

    @field_validator(
        "provenance_refs", "allowed_readers", "allowed_writers", "memory_classes"
    )
    @classmethod
    def explicit_memory_scope(cls, values: list[str], info: Any) -> list[str]:
        return _explicit_values(values, info.field_name)

    @field_validator("retention_until")
    @classmethod
    def aware_retention(cls, value: datetime) -> datetime:
        return _require_aware(value, "retention_until")

    @model_validator(mode="after")
    def enforce_disposal(self) -> "OperatingMemoryLease":
        if not self.delete_on_termination:
            raise ValueError("ephemeral operating memory must be deleted on termination")
        if self.writeback_to_canonical_memory:
            raise ValueError(
                "operating memory cannot write back without a separate memory decision"
            )
        if not self.zero_mem_receipt_required:
            raise ValueError("a deletion receipt is required")
        return self


class EvidenceDeliveryPolicy(BaseModel):
    model_config = ConfigDict(frozen=True)

    recipient_agent_id: str
    mode: DeliveryMode = DeliveryMode.MINIMAL_EVIDENCE
    allowed_fields: list[str] = Field(min_length=1)
    redaction_profile_id: str
    max_items: int = Field(default=1, gt=0, le=10_000)
    raw_source_delivery: bool = False
    credential_delivery: bool = False

    @field_validator("allowed_fields")
    @classmethod
    def explicit_fields(cls, values: list[str], info: Any) -> list[str]:
        return _explicit_values(values, info.field_name)

    @model_validator(mode="after")
    def enforce_minimization(self) -> "EvidenceDeliveryPolicy":
        if self.raw_source_delivery:
            raise ValueError("raw source delivery requires a separate authorization")
        if self.credential_delivery:
            raise ValueError("credentials can never be delivered")
        return self


class LifecycleWindow(BaseModel):
    model_config = ConfigDict(frozen=True)

    created_at: datetime = Field(default_factory=utcnow)
    activate_by: datetime
    expires_at: datetime
    deletion_due_at: datetime
    activated_at: datetime | None = None
    revoked_at: datetime | None = None
    expired_at: datetime | None = None
    terminated_at: datetime | None = None
    deleted_at: datetime | None = None

    @field_validator(
        "created_at",
        "activate_by",
        "expires_at",
        "deletion_due_at",
        "activated_at",
        "revoked_at",
        "expired_at",
        "terminated_at",
        "deleted_at",
    )
    @classmethod
    def aware_timestamps(cls, value: datetime | None, info: Any) -> datetime | None:
        if value is None:
            return None
        return _require_aware(value, info.field_name)

    @model_validator(mode="after")
    def ordered_window(self) -> "LifecycleWindow":
        if not self.created_at < self.activate_by <= self.expires_at:
            raise ValueError("lifecycle must satisfy created_at < activate_by <= expires_at")
        if self.deletion_due_at < self.expires_at:
            raise ValueError("deletion_due_at cannot precede expires_at")
        if self.activated_at is not None and not (
            self.created_at <= self.activated_at <= self.activate_by
        ):
            raise ValueError("activated_at is outside the activation window")
        return self


class IsolatedEphemeralAgentContract(BaseModel):
    """One bounded contract binding origin, authority, silo, memory and disposal."""

    model_config = ConfigDict(frozen=True)

    contract_id: str
    schema_version: str = "1.0.0"
    status: EphemeralAgentStatus = EphemeralAgentStatus.DRAFT
    agent_id: str
    origin: AgentOrigin
    need_binding: NeedToAskAcquireBinding
    mandate: BoundedMandate
    isolation: IsolationBoundary
    memory: OperatingMemoryLease
    delivery: EvidenceDeliveryPolicy
    lifecycle: LifecycleWindow
    max_lifetime_seconds: int = Field(default=900, gt=0, le=86_400)
    receipt_ids: dict[str, str] = Field(default_factory=dict)
    termination_reason: str | None = None

    @model_validator(mode="after")
    def cross_object_invariants(self) -> "IsolatedEphemeralAgentContract":
        lifetime = (self.lifecycle.expires_at - self.lifecycle.created_at).total_seconds()
        if lifetime > self.max_lifetime_seconds:
            raise ValueError("contract lifetime exceeds max_lifetime_seconds")
        if self.need_binding.acquisition_agent_id != self.agent_id:
            raise ValueError("need binding must target this acquisition agent")
        if self.delivery.recipient_agent_id != self.origin.requesting_agent_id:
            raise ValueError("evidence may only return to the requesting agent")
        if self.agent_id not in self.memory.allowed_readers:
            raise ValueError("acquisition agent must be an explicit memory reader")
        if self.memory.retention_until > self.lifecycle.deletion_due_at:
            raise ValueError("memory retention cannot outlive deletion_due_at")
        if self.origin.principal_id == self.agent_id:
            raise ValueError("the agent cannot be its own principal")

        requirements = {
            EphemeralAgentStatus.ACTIVE: ("activation", self.lifecycle.activated_at),
            EphemeralAgentStatus.REVOKED: ("revocation", self.lifecycle.revoked_at),
            EphemeralAgentStatus.EXPIRED: ("expiration", self.lifecycle.expired_at),
            EphemeralAgentStatus.TERMINATED: (
                "termination",
                self.lifecycle.terminated_at,
            ),
            EphemeralAgentStatus.DELETED: ("deletion", self.lifecycle.deleted_at),
        }
        if self.status in requirements:
            receipt_name, timestamp = requirements[self.status]
            if receipt_name not in self.receipt_ids:
                raise ValueError(f"{self.status.value} status requires {receipt_name} receipt")
            if timestamp is None:
                raise ValueError(f"{self.status.value} status requires lifecycle timestamp")

        if self.status == EphemeralAgentStatus.DELETED:
            closure_receipts = {"revocation", "expiration", "termination"}
            if not closure_receipts.intersection(self.receipt_ids):
                raise ValueError("deleted status requires a prior closure receipt")
            if not any(
                (
                    self.lifecycle.revoked_at,
                    self.lifecycle.expired_at,
                    self.lifecycle.terminated_at,
                )
            ):
                raise ValueError("deleted status requires a prior closure timestamp")
        return self

    def digest(self) -> str:
        canonical = json.dumps(
            self.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
        )
        return sha256(canonical.encode("utf-8")).hexdigest()


class EphemeralContractRegistry:
    """Lifecycle registry and verifier; never an execution authorizer."""

    def __init__(self) -> None:
        self._contracts: dict[str, IsolatedEphemeralAgentContract] = {}

    def register(
        self, contract: IsolatedEphemeralAgentContract
    ) -> IsolatedEphemeralAgentContract:
        if contract.contract_id in self._contracts:
            raise ValueError(f"Contract {contract.contract_id} already exists")
        self._contracts[contract.contract_id] = contract
        return contract

    def get(self, contract_id: str) -> IsolatedEphemeralAgentContract | None:
        return self._contracts.get(contract_id)

    def activate(
        self, contract_id: str, receipt_id: str, now: datetime | None = None
    ) -> IsolatedEphemeralAgentContract:
        now = _require_aware(now or utcnow(), "now")
        contract = self._require(contract_id)
        if contract.status != EphemeralAgentStatus.DRAFT:
            raise ValueError("only draft contracts can be activated")
        if now < contract.lifecycle.created_at or now > contract.lifecycle.activate_by:
            raise ValueError("activation is outside the allowed window")
        lifecycle = contract.lifecycle.model_copy(update={"activated_at": now})
        return self._replace(
            contract,
            status=EphemeralAgentStatus.ACTIVE,
            lifecycle=lifecycle,
            receipt_ids={**contract.receipt_ids, "activation": receipt_id},
        )

    def verify_execution_binding(
        self,
        contract_id: str,
        *,
        agent_id: str,
        tool: str | None = None,
        resource: str | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Check bindings only. REHT/RACS must still authorize each action."""
        now = _require_aware(now or utcnow(), "now")
        contract = self._require(contract_id)
        issues: list[str] = []
        if contract.status != EphemeralAgentStatus.ACTIVE:
            issues.append("contract_not_active")
        if now >= contract.lifecycle.expires_at:
            issues.append("contract_expired")
        if agent_id != contract.agent_id:
            issues.append("agent_mismatch")
        if tool and tool not in contract.mandate.allowed_tools:
            issues.append("tool_out_of_scope")
        if resource and resource not in contract.mandate.allowed_resources:
            issues.append("resource_out_of_scope")
        return {
            "valid": not issues,
            "issues": issues,
            "contract_digest": contract.digest(),
            "reht_clearance_id": contract.need_binding.reht_clearance_id,
            "racs_decision_id": contract.need_binding.racs_decision_id,
            "gateway_enforcement_id": contract.isolation.gateway_enforcement_id,
            "requires_per_action_authorization": True,
        }

    def revoke(
        self,
        contract_id: str,
        *,
        reason: str,
        receipt_id: str,
        now: datetime | None = None,
    ) -> IsolatedEphemeralAgentContract:
        now = _require_aware(now or utcnow(), "now")
        contract = self._require(contract_id)
        if contract.status in {
            EphemeralAgentStatus.REVOKED,
            EphemeralAgentStatus.TERMINATED,
            EphemeralAgentStatus.DELETED,
        }:
            raise ValueError("contract is already closed")
        lifecycle = contract.lifecycle.model_copy(update={"revoked_at": now})
        return self._replace(
            contract,
            status=EphemeralAgentStatus.REVOKED,
            lifecycle=lifecycle,
            termination_reason=reason,
            receipt_ids={**contract.receipt_ids, "revocation": receipt_id},
        )

    def expire(
        self, contract_id: str, receipt_id: str, now: datetime | None = None
    ) -> IsolatedEphemeralAgentContract:
        now = _require_aware(now or utcnow(), "now")
        contract = self._require(contract_id)
        if contract.status != EphemeralAgentStatus.ACTIVE:
            raise ValueError("only active contracts can expire")
        if now < contract.lifecycle.expires_at:
            raise ValueError("contract has not reached expires_at")
        lifecycle = contract.lifecycle.model_copy(update={"expired_at": now})
        return self._replace(
            contract,
            status=EphemeralAgentStatus.EXPIRED,
            lifecycle=lifecycle,
            receipt_ids={**contract.receipt_ids, "expiration": receipt_id},
        )

    def terminate(
        self,
        contract_id: str,
        *,
        reason: str,
        receipt_id: str,
        now: datetime | None = None,
    ) -> IsolatedEphemeralAgentContract:
        now = _require_aware(now or utcnow(), "now")
        contract = self._require(contract_id)
        if contract.status not in {
            EphemeralAgentStatus.ACTIVE,
            EphemeralAgentStatus.EXPIRED,
        }:
            raise ValueError("contract cannot be terminated from its current state")
        lifecycle = contract.lifecycle.model_copy(update={"terminated_at": now})
        return self._replace(
            contract,
            status=EphemeralAgentStatus.TERMINATED,
            lifecycle=lifecycle,
            termination_reason=reason,
            receipt_ids={**contract.receipt_ids, "termination": receipt_id},
        )

    def mark_deleted(
        self, contract_id: str, receipt_id: str, now: datetime | None = None
    ) -> IsolatedEphemeralAgentContract:
        now = _require_aware(now or utcnow(), "now")
        contract = self._require(contract_id)
        if contract.status not in {
            EphemeralAgentStatus.REVOKED,
            EphemeralAgentStatus.TERMINATED,
            EphemeralAgentStatus.EXPIRED,
        }:
            raise ValueError("memory can only be marked deleted after closure")
        lifecycle = contract.lifecycle.model_copy(update={"deleted_at": now})
        return self._replace(
            contract,
            status=EphemeralAgentStatus.DELETED,
            lifecycle=lifecycle,
            receipt_ids={**contract.receipt_ids, "deletion": receipt_id},
        )

    def _replace(
        self, contract: IsolatedEphemeralAgentContract, **updates: Any
    ) -> IsolatedEphemeralAgentContract:
        payload = contract.model_dump()
        payload.update(updates)
        updated = IsolatedEphemeralAgentContract.model_validate(payload)
        self._contracts[contract.contract_id] = updated
        return updated

    def _require(self, contract_id: str) -> IsolatedEphemeralAgentContract:
        contract = self._contracts.get(contract_id)
        if contract is None:
            raise KeyError(f"Contract {contract_id} not found")
        return contract
