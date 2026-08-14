from datetime import datetime, timedelta, timezone

from open_agent_contract.a2a import A2A_GOVERNED_CONTRACT_EXTENSION_URI, evaluate_a2a_consequence, to_a2a_extension
from open_agent_contract.governed import ActionIntent, AuthorityGrant, ConformanceOutcome, GovernedContract, PartyRef


def _fixture(amount="1200.00", currency="EUR"):
    now = datetime(2026, 8, 14, 6, 0, tzinfo=timezone.utc)
    org = PartyRef(party_id="org:buyer-co", kind="organization")
    buyer = PartyRef(party_id="agent:buyer", kind="agent")
    contract = GovernedContract(
        contract_id="gc-1", issuer=org, subject=buyer,
        authority=[AuthorityGrant(grant_id="g-1", granted_by=org.party_id, granted_to=buyer.party_id, actions=["purchase"], resources=["catalog:item-42"], purposes=["restock"])],
        allowed_actions=["purchase"], allowed_resources=["catalog:item-42"], allowed_purposes=["restock"],
        constraints={"max_amount": "1000.00", "currency": "EUR"},
        valid_from=now - timedelta(minutes=1), valid_until=now + timedelta(hours=1),
    )
    intent = ActionIntent(intent_id="i-1", actor=buyer, action="purchase", resource="catalog:item-42", purpose="restock", requested_at=now, attributes={"amount": amount, "currency": currency})
    return now, contract, intent


def test_1200_purchase_exceeds_1000_mandate():
    now, contract, intent = _fixture()
    result = evaluate_a2a_consequence(contract, intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.NON_CONFORMANT
    assert result.issues[0].code == "amount_exceeds_mandate"


def test_900_purchase_is_contract_conformant_but_not_authorized():
    now, contract, intent = _fixture(amount="900.00")
    result = evaluate_a2a_consequence(contract, intent, checked_at=now)
    extension = to_a2a_extension(result)
    assert result.outcome == ConformanceOutcome.CONFORMANT
    assert extension["authorization_required"] is True
    assert extension["uri"] == A2A_GOVERNED_CONTRACT_EXTENSION_URI


def test_currency_mismatch_fails_closed():
    now, contract, intent = _fixture(amount="900.00", currency="USD")
    result = evaluate_a2a_consequence(contract, intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.NON_CONFORMANT
    assert any(issue.code == "currency_mismatch" for issue in result.issues)


def test_missing_amount_fails_closed():
    now, contract, intent = _fixture(amount="900.00")
    intent.attributes.pop("amount")
    result = evaluate_a2a_consequence(contract, intent, checked_at=now)
    assert result.outcome == ConformanceOutcome.NON_CONFORMANT
    assert any(issue.code == "amount_missing" for issue in result.issues)
