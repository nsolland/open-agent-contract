from datetime import datetime, timezone

import pytest

from open_agent_contract.aps import (
    APSContractProjection,
    APSVerificationStatus,
    APSVerifiedAuthoritySnapshot,
    project_verified_aps_authority,
)
from open_agent_contract.governed import ActionIntent, ConformanceOutcome, PartyRef, check_conformance


def _snapshot(**overrides):
    values = {
        "agent_id": "did:key:zAgent",
        "principal_id": "did:web:example.com",
        "principal_binding_id": "binding-1",
        "leaf_issuer": "did:web:example.com",
        "leaf_delegation_id": "sha256:leaf",
        "authority_chain": ["sha256:root", "sha256:leaf"],
        "agent_identity_status": APSVerificationStatus.VALID,
        "principal_binding_status": APSVerificationStatus.VALID,
        "delegation_chain_status": APSVerificationStatus.VALID,
        "revocation_status": APSVerificationStatus.VALID,
        "effective_scope_grants": ["commerce:*"],
        "effective_not_before": datetime(2026, 8, 14, 10, 0, tzinfo=timezone.utc),
        "effective_not_after": datetime(2026, 8, 14, 12, 0, tzinfo=timezone.utc),
        "spend": {"mode": "bounded", "unit": "iso4217:EUR:minor", "per_action": "5000", "cumulative": "10000"},
        "depth_remaining": 1,
        "reputation_ceiling": 80,
        "values_required": ["F-001"],
        "reversibility_ceiling": "compensable",
        "authority_profiles": ["commerce-v1"],
        "receipt_context": "aps-receipt-v1",
    }
    values.update(overrides)
    return APSVerifiedAuthoritySnapshot(**values)


def _projection():
    return APSContractProjection(
        contract_id="contract-aps-1",
        required_scope_grants=["commerce:checkout"],
        allowed_actions=["checkout"],
        allowed_resources=["merchant:42"],
        allowed_purposes=["purchase"],
    )


def test_projects_verified_aps_authority_without_authorizing_execution():
    contract = project_verified_aps_authority(_snapshot(), _projection())

    assert contract.subject.party_id == "did:key:zAgent"
    assert contract.authority[0].delegation_chain == ["sha256:root", "sha256:leaf"]
    assert contract.constraints["aps"]["reversibility_ceiling"] == "compensable"
    assert contract.extensions["aps"]["authorization_required"] is True

    intent = ActionIntent(
        intent_id="intent-1",
        actor=PartyRef(party_id="did:key:zAgent", kind="agent"),
        action="checkout",
        resource="merchant:42",
        purpose="purchase",
        requested_at=datetime(2026, 8, 14, 11, 0, tzinfo=timezone.utc),
    )
    result = check_conformance(
        contract,
        intent,
        checked_at=datetime(2026, 8, 14, 11, 0, tzinfo=timezone.utc),
    )

    assert result.outcome == ConformanceOutcome.CONFORMANT
    assert contract.extensions["aps"]["authorization_required"] is True


@pytest.mark.parametrize(
    "field,status",
    [
        ("agent_identity_status", APSVerificationStatus.INDETERMINATE),
        ("principal_binding_status", APSVerificationStatus.INVALID),
        ("delegation_chain_status", APSVerificationStatus.UNSUPPORTED),
        ("revocation_status", APSVerificationStatus.INDETERMINATE),
    ],
)
def test_fails_closed_on_non_valid_aps_verification(field, status):
    with pytest.raises(ValueError, match="refusing authority projection"):
        project_verified_aps_authority(_snapshot(**{field: status}), _projection())


def test_rejects_uncovered_scope():
    snapshot = _snapshot(effective_scope_grants=["commerce:read"])

    with pytest.raises(ValueError, match="does not cover required scope"):
        project_verified_aps_authority(snapshot, _projection())


def test_terminal_wildcard_matches_parent_and_descendants():
    projection = _projection().model_copy(update={"required_scope_grants": ["commerce", "commerce:checkout:write"]})
    contract = project_verified_aps_authority(_snapshot(), projection)

    assert contract.constraints["aps"]["required_scope_grants"] == [
        "commerce",
        "commerce:checkout:write",
    ]
