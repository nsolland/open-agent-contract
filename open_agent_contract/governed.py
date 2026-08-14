"""Vendor-neutral Governed Contract v1 models and deterministic conformance.

This module defines what must be true before an action is eligible to be
submitted to an execution-authorization boundary. It does not execute actions
and does not replace an organization's policy decision or enforcement point.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Any

from pydantic import BaseModel, Field, model_validator


class ConformanceOutcome(str, Enum):
    CONFORMANT = "conformant"
    NON_CONFORMANT = "non_conformant"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    NOT_YET_VALID = "not_yet_valid"
    EXPIRED = "expired"


class PartyRef(BaseModel):
    party_id: str = Field(min_length=1)
    kind: str = Field(description="human, agent, service, organization, or other profile")
    identity_scheme: str | None = None
    identity_ref: str | None = None


class AuthorityGrant(BaseModel):
    grant_id: str = Field(min_length=1)
    granted_by: str = Field(min_length=1)
    granted_to: str = Field(min_length=1)
    actions: list[str] = Field(min_length=1)
    resources: list[str] = Field(min_length=1)
    purposes: list[str] = Field(min_length=1)
    not_before: datetime | None = None
    not_after: datetime | None = None
    delegation_chain: list[str] = Field(default_factory=list)


class EvidenceRequirement(BaseModel):
    requirement_id: str = Field(min_length=1)
    evidence_type: str = Field(min_length=1)
    required: bool = True
    max_age_seconds: int | None = Field(default=None, ge=0)


class CompletionCondition(BaseModel):
    condition_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    required: bool = True


class GovernedContract(BaseModel):
    """Portable contract describing the governed consequence boundary."""

    spec_version: str = "1.0.0"
    contract_id: str = Field(min_length=1)
    issuer: PartyRef
    subject: PartyRef
    authority: list[AuthorityGrant] = Field(min_length=1)
    allowed_actions: list[str] = Field(min_length=1)
    allowed_resources: list[str] = Field(min_length=1)
    allowed_purposes: list[str] = Field(min_length=1)
    prohibited_actions: list[str] = Field(default_factory=list)
    constraints: dict[str, Any] = Field(default_factory=dict)
    evidence_requirements: list[EvidenceRequirement] = Field(default_factory=list)
    completion_conditions: list[CompletionCondition] = Field(default_factory=list)
    valid_from: datetime
    valid_until: datetime
    require_receipt: bool = True
    extensions: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_window(self) -> "GovernedContract":
        if self.valid_until <= self.valid_from:
            raise ValueError("valid_until must be after valid_from")
        return self

    def canonical_payload(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)

    def digest(self) -> str:
        payload = json.dumps(
            self.canonical_payload(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return sha256(payload).hexdigest()


class ActionIntent(BaseModel):
    intent_id: str = Field(min_length=1)
    actor: PartyRef
    action: str = Field(min_length=1)
    resource: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    requested_at: datetime
    evidence: dict[str, dict[str, Any]] = Field(default_factory=dict)
    attributes: dict[str, Any] = Field(default_factory=dict)


class ConformanceIssue(BaseModel):
    code: str
    message: str
    requirement_id: str | None = None


class ConformanceResult(BaseModel):
    outcome: ConformanceOutcome
    contract_id: str
    intent_id: str
    contract_digest: str
    checked_at: datetime
    issues: list[ConformanceIssue] = Field(default_factory=list)

    @property
    def conformant(self) -> bool:
        return self.outcome == ConformanceOutcome.CONFORMANT


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def check_conformance(
    contract: GovernedContract,
    intent: ActionIntent,
    *,
    checked_at: datetime | None = None,
) -> ConformanceResult:
    """Deterministically check an action intent against a Governed Contract.

    A conformant result means only that the intent satisfies this contract.
    It MUST NOT be interpreted as execution authorization.
    """

    now = _utc(checked_at or datetime.now(timezone.utc))
    valid_from = _utc(contract.valid_from)
    valid_until = _utc(contract.valid_until)
    requested_at = _utc(intent.requested_at)
    issues: list[ConformanceIssue] = []

    if now < valid_from or requested_at < valid_from:
        return _result(ConformanceOutcome.NOT_YET_VALID, contract, intent, now, issues)
    if now >= valid_until or requested_at >= valid_until:
        return _result(ConformanceOutcome.EXPIRED, contract, intent, now, issues)

    if intent.actor.party_id != contract.subject.party_id:
        issues.append(ConformanceIssue(code="actor_mismatch", message="actor is not contract subject"))
    if intent.action in contract.prohibited_actions:
        issues.append(ConformanceIssue(code="prohibited_action", message="action is explicitly prohibited"))
    if intent.action not in contract.allowed_actions:
        issues.append(ConformanceIssue(code="action_out_of_scope", message="action is outside allowed actions"))
    if intent.resource not in contract.allowed_resources:
        issues.append(ConformanceIssue(code="resource_out_of_scope", message="resource is outside allowed resources"))
    if intent.purpose not in contract.allowed_purposes:
        issues.append(ConformanceIssue(code="purpose_mismatch", message="purpose is outside allowed purposes"))

    grant_ok = any(
        grant.granted_to == intent.actor.party_id
        and intent.action in grant.actions
        and intent.resource in grant.resources
        and intent.purpose in grant.purposes
        and (grant.not_before is None or requested_at >= _utc(grant.not_before))
        and (grant.not_after is None or requested_at < _utc(grant.not_after))
        for grant in contract.authority
    )
    if not grant_ok:
        issues.append(ConformanceIssue(code="authority_missing", message="no applicable authority grant"))

    if issues:
        return _result(ConformanceOutcome.NON_CONFORMANT, contract, intent, now, issues)

    evidence_issues: list[ConformanceIssue] = []
    for req in contract.evidence_requirements:
        if not req.required:
            continue
        item = intent.evidence.get(req.requirement_id)
        if item is None:
            evidence_issues.append(ConformanceIssue(
                code="evidence_missing",
                message=f"required evidence {req.requirement_id} is missing",
                requirement_id=req.requirement_id,
            ))
            continue
        if item.get("type") != req.evidence_type:
            evidence_issues.append(ConformanceIssue(
                code="evidence_type_mismatch",
                message=f"evidence {req.requirement_id} has wrong type",
                requirement_id=req.requirement_id,
            ))
        if req.max_age_seconds is not None:
            observed_at = item.get("observed_at")
            if observed_at is None:
                evidence_issues.append(ConformanceIssue(
                    code="evidence_freshness_unknown",
                    message=f"evidence {req.requirement_id} has no observed_at",
                    requirement_id=req.requirement_id,
                ))
            else:
                observed = _utc(datetime.fromisoformat(str(observed_at).replace("Z", "+00:00")))
                if (now - observed).total_seconds() > req.max_age_seconds:
                    evidence_issues.append(ConformanceIssue(
                        code="evidence_stale",
                        message=f"evidence {req.requirement_id} is stale",
                        requirement_id=req.requirement_id,
                    ))

    if evidence_issues:
        return _result(
            ConformanceOutcome.INSUFFICIENT_EVIDENCE,
            contract,
            intent,
            now,
            evidence_issues,
        )

    return _result(ConformanceOutcome.CONFORMANT, contract, intent, now, [])


def _result(
    outcome: ConformanceOutcome,
    contract: GovernedContract,
    intent: ActionIntent,
    checked_at: datetime,
    issues: list[ConformanceIssue],
) -> ConformanceResult:
    return ConformanceResult(
        outcome=outcome,
        contract_id=contract.contract_id,
        intent_id=intent.intent_id,
        contract_digest=contract.digest(),
        checked_at=checked_at,
        issues=issues,
    )
