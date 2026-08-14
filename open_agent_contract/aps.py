"""Adapter from verified APS authority facts into Governed Contract v1.

The adapter is intentionally not an APS cryptographic verifier. It accepts a
snapshot produced by a conforming/trusted APS verifier, preserves the evidence
boundary, and projects only explicitly mapped authority into a portable
Governed Contract. Contract conformance remains distinct from execution
authorization.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator

from .governed import AuthorityGrant, GovernedContract, PartyRef

APS_DRAFT = "draft-pidlisnyi-aps-03"
APS_DRAFT_URL = "https://www.ietf.org/archive/id/draft-pidlisnyi-aps-03.html"


class APSVerificationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    INDETERMINATE = "indeterminate"
    UNSUPPORTED = "unsupported"


class APSVerifiedAuthoritySnapshot(BaseModel):
    """Normalized output from an external APS verifier.

    The four status fields are kept separate so callers cannot accidentally
    turn cryptographic integrity, principal binding, delegation validity or
    revocation freshness into one undifferentiated trust bit.
    """

    agent_id: str = Field(min_length=1)
    principal_id: str = Field(min_length=1)
    principal_binding_id: str = Field(min_length=1)
    leaf_issuer: str = Field(min_length=1)
    leaf_delegation_id: str = Field(min_length=1)
    authority_chain: list[str] = Field(min_length=1)

    agent_identity_status: APSVerificationStatus
    principal_binding_status: APSVerificationStatus
    delegation_chain_status: APSVerificationStatus
    revocation_status: APSVerificationStatus

    effective_scope_grants: list[str] = Field(min_length=1)
    effective_not_before: datetime
    effective_not_after: datetime

    spend: dict[str, Any]
    depth_remaining: int = Field(ge=0, le=255)
    reputation_ceiling: int = Field(ge=0, le=100)
    values_required: list[str] = Field(default_factory=list)
    reversibility_ceiling: str = Field(min_length=1)

    authority_profiles: list[str] = Field(default_factory=list)
    receipt_context: str | None = None
    source_draft: str = APS_DRAFT

    @model_validator(mode="after")
    def validate_window(self) -> "APSVerifiedAuthoritySnapshot":
        if self.effective_not_after <= self.effective_not_before:
            raise ValueError("effective_not_after must be after effective_not_before")
        if self.authority_chain[-1] != self.leaf_delegation_id:
            raise ValueError("authority_chain must end at leaf_delegation_id")
        return self


class APSContractProjection(BaseModel):
    """Deployment-owned semantic mapping from APS scopes into contract fields."""

    contract_id: str = Field(min_length=1)
    required_scope_grants: list[str] = Field(min_length=1)
    allowed_actions: list[str] = Field(min_length=1)
    allowed_resources: list[str] = Field(min_length=1)
    allowed_purposes: list[str] = Field(min_length=1)
    principal_kind: str = "organization"
    constraints: dict[str, Any] = Field(default_factory=dict)
    require_receipt: bool = True


def _scope_covers(parent: str, child: str) -> bool:
    """Implement APS hierarchical scope coverage for exact and terminal wildcards."""
    if parent == "*":
        return True
    if parent == child:
        return True
    if parent.endswith(":*"):
        prefix = parent[:-2]
        return child == prefix or child.startswith(prefix + ":")
    return False


def _require_valid(label: str, status: APSVerificationStatus) -> None:
    if status != APSVerificationStatus.VALID:
        raise ValueError(f"APS {label} is {status.value}; refusing authority projection")


def project_verified_aps_authority(
    snapshot: APSVerifiedAuthoritySnapshot,
    projection: APSContractProjection,
) -> GovernedContract:
    """Project verified APS authority into a Governed Contract, fail closed.

    This function does not verify APS signatures, JCS canonicalization, DID key
    authority, revocation records, spend ledgers or receipt chains. Those facts
    must be resolved before this boundary and represented by ``snapshot``.
    """

    _require_valid("agent identity", snapshot.agent_identity_status)
    _require_valid("principal binding", snapshot.principal_binding_status)
    _require_valid("delegation chain", snapshot.delegation_chain_status)
    _require_valid("revocation state", snapshot.revocation_status)

    uncovered = [
        required
        for required in projection.required_scope_grants
        if not any(
            _scope_covers(granted, required)
            for granted in snapshot.effective_scope_grants
        )
    ]
    if uncovered:
        raise ValueError(
            "APS authority does not cover required scope grants: "
            + ", ".join(sorted(uncovered))
        )

    aps_constraints = {
        "source_draft": snapshot.source_draft,
        "required_scope_grants": projection.required_scope_grants,
        "effective_scope_grants": snapshot.effective_scope_grants,
        "spend": snapshot.spend,
        "depth_remaining": snapshot.depth_remaining,
        "reputation_ceiling": snapshot.reputation_ceiling,
        "values_required": snapshot.values_required,
        "reversibility_ceiling": snapshot.reversibility_ceiling,
    }

    constraints = dict(projection.constraints)
    constraints["aps"] = aps_constraints

    extensions: dict[str, Any] = {
        "aps": {
            "source_draft": snapshot.source_draft,
            "principal_binding_id": snapshot.principal_binding_id,
            "leaf_delegation_id": snapshot.leaf_delegation_id,
            "authority_chain": snapshot.authority_chain,
            "authority_profiles": snapshot.authority_profiles,
            "verification": {
                "agent_identity": snapshot.agent_identity_status.value,
                "principal_binding": snapshot.principal_binding_status.value,
                "delegation_chain": snapshot.delegation_chain_status.value,
                "revocation": snapshot.revocation_status.value,
            },
            "receipt_context": snapshot.receipt_context,
            "authorization_required": True,
        }
    }

    return GovernedContract(
        contract_id=projection.contract_id,
        issuer=PartyRef(
            party_id=snapshot.principal_id,
            kind=projection.principal_kind,
            identity_scheme="aps-principal-binding",
            identity_ref=snapshot.principal_binding_id,
        ),
        subject=PartyRef(
            party_id=snapshot.agent_id,
            kind="agent",
            identity_scheme="did",
            identity_ref=snapshot.agent_id,
        ),
        authority=[
            AuthorityGrant(
                grant_id=snapshot.leaf_delegation_id,
                granted_by=snapshot.leaf_issuer,
                granted_to=snapshot.agent_id,
                actions=projection.allowed_actions,
                resources=projection.allowed_resources,
                purposes=projection.allowed_purposes,
                not_before=snapshot.effective_not_before,
                not_after=snapshot.effective_not_after,
                delegation_chain=snapshot.authority_chain,
            )
        ],
        allowed_actions=projection.allowed_actions,
        allowed_resources=projection.allowed_resources,
        allowed_purposes=projection.allowed_purposes,
        constraints=constraints,
        valid_from=snapshot.effective_not_before,
        valid_until=snapshot.effective_not_after,
        require_receipt=projection.require_receipt,
        extensions=extensions,
    )
