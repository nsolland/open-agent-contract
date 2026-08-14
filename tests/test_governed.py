from datetime import datetime, timedelta, timezone

from open_agent_contract.governed import (
    ActionIntent,
    AuthorityGrant,
    ConformanceOutcome,
    ConformanceResult,
    ContinuationOutcome,
    EvidenceRequirement,
    GovernedContract,
    PartyRef,
    check_conformance,
    verify_contract_continuity,
)


def _contract(now: datetime) -> GovernedContract:
    issuer = PartyRef(party_id="org:buyer", kind="organization")
    agent = PartyRef(party_id="agent:procurement-7", kind="agent")
    return GovernedContract(
        contract_id="gc-1",
        issuer=issuer,
        subject=agent,
        authority=[AuthorityGrant(
            grant_id="grant-1",
            granted_by=issuer.party_id,
            granted_to=agent.party_id,
            actions=["purchase"],
            resources=["catalog:item-42"],
            purposes=["approved_restock"],
        )],
        allowed_actions=["purchase"],
        allowed_resources=["catalog:item-42"],
        allowed_purposes=["approved_restock"],
        prohibited_actions=["wire_funds"],
        evidence_requirements=[EvidenceRequirement(
            requirement_id="inventory",
            evidence_type="inventory_snapshot",
            max_age_seconds=300,
        )],
        valid_from=now - timedelta(minutes=1),
        valid_until=now + timedelta(hours=1),
    )


def _intent(now: datetime) -> ActionIntent:
    return ActionIntent(
        intent_id="intent-1",
        actor=PartyRef(party_id="agent:procurement-7", kind="agent"),
        action="purchase",
        resource="catalog:item-42",
        purpose="approved_restock",
        requested_at=now,
        evidence={
            "inventory": {
                "type": "inventory_snapshot",
                "observed_at": now.isoformat(),
                "value": {"on_hand": 2},
            }
        },
    )


def test_conformant_intent():
    now = datetime.now(timezone.utc)
    contract = _contract(now)
    result = check_conformance(contract, _intent(now), checked_at=now)
    assert result.outcome == ConformanceOutcome.CONFORMANT
    assert result.conformant is True
    assert result.contract_spec_version == "1.1.0"
    assert len(result.contract_digest) == 64


def test_wrong_purpose_is_non_conformant():
    now = datetime.now(timezone.utc)
    intent = _intent(now)
    intent.purpose = "personal_use"
    result = check_conformance(_contract(now), intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.NON_CONFORMANT
    assert {i.code for i in result.issues} >= {"purpose_mismatch", "authority_missing"}


def test_missing_evidence_defers_without_guessing():
    now = datetime.now(timezone.utc)
    intent = _intent(now)
    intent.evidence = {}
    result = check_conformance(_contract(now), intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.INSUFFICIENT_EVIDENCE
    assert result.issues[0].code == "evidence_missing"


def test_stale_evidence_is_insufficient():
    now = datetime.now(timezone.utc)
    intent = _intent(now)
    intent.evidence["inventory"]["observed_at"] = (now - timedelta(minutes=10)).isoformat()
    result = check_conformance(_contract(now), intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.INSUFFICIENT_EVIDENCE
    assert result.issues[0].code == "evidence_stale"


def test_expired_contract_is_not_usable():
    now = datetime.now(timezone.utc)
    contract = _contract(now)
    contract.valid_until = now - timedelta(seconds=1)
    contract.valid_from = now - timedelta(hours=1)
    result = check_conformance(contract, _intent(now), checked_at=now)
    assert result.outcome == ConformanceOutcome.EXPIRED


def test_actor_must_match_subject_and_grant():
    now = datetime.now(timezone.utc)
    intent = _intent(now)
    intent.actor = PartyRef(party_id="agent:other", kind="agent")
    result = check_conformance(_contract(now), intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.NON_CONFORMANT
    assert {i.code for i in result.issues} >= {"actor_mismatch", "authority_missing"}


def test_prohibited_action_fails_even_if_present_elsewhere():
    now = datetime.now(timezone.utc)
    contract = _contract(now)
    contract.allowed_actions.append("wire_funds")
    contract.authority[0].actions.append("wire_funds")
    intent = _intent(now)
    intent.action = "wire_funds"
    result = check_conformance(contract, intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.NON_CONFORMANT
    assert "prohibited_action" in {i.code for i in result.issues}


def test_digest_is_deterministic():
    now = datetime(2026, 8, 13, 18, 0, tzinfo=timezone.utc)
    a = _contract(now)
    b = GovernedContract.model_validate(a.model_dump())
    assert a.digest() == b.digest()


def test_unchanged_contract_continuation_is_current():
    now = datetime.now(timezone.utc)
    contract = _contract(now)
    prior = check_conformance(contract, _intent(now), checked_at=now)
    result = verify_contract_continuity(prior, contract)
    assert result.outcome == ContinuationOutcome.CURRENT
    assert result.current is True
    assert result.requires_fresh_conformance is False


def test_changed_contract_invalidates_prior_continuation():
    now = datetime.now(timezone.utc)
    original = _contract(now)
    prior = check_conformance(original, _intent(now), checked_at=now)
    amended = GovernedContract.model_validate(original.model_dump())
    amended.allowed_resources.append("catalog:item-99")
    result = verify_contract_continuity(prior, amended)
    assert result.outcome == ContinuationOutcome.CONTRACT_CHANGED
    assert result.current is False
    assert result.requires_fresh_conformance is True
    assert result.expected_contract_digest != result.current_contract_digest


def test_contract_id_replacement_invalidates_prior_continuation():
    now = datetime.now(timezone.utc)
    original = _contract(now)
    prior = check_conformance(original, _intent(now), checked_at=now)
    replacement = GovernedContract.model_validate(original.model_dump())
    replacement.contract_id = "gc-2"
    result = verify_contract_continuity(prior, replacement)
    assert result.outcome == ContinuationOutcome.CONTRACT_CHANGED
    assert result.requires_fresh_conformance is True


def test_legacy_result_without_spec_version_requires_fresh_conformance():
    now = datetime.now(timezone.utc)
    contract = _contract(now)
    current = check_conformance(contract, _intent(now), checked_at=now)
    legacy_payload = current.model_dump()
    legacy_payload.pop("contract_spec_version")
    legacy = ConformanceResult.model_validate(legacy_payload)
    result = verify_contract_continuity(legacy, contract)
    assert legacy.contract_spec_version is None
    assert result.outcome == ContinuationOutcome.CONTRACT_CHANGED
    assert result.requires_fresh_conformance is True
