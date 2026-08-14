"""30-second A2A governed consequence demo.

Communication succeeds. Identity is assumed valid. The purchase still cannot
proceed because the requested amount exceeds the buyer agent's mandate.
"""

from datetime import datetime, timedelta, timezone

from open_agent_contract.a2a import evaluate_a2a_consequence, to_a2a_extension
from open_agent_contract.governed import ActionIntent, AuthorityGrant, GovernedContract, PartyRef

now = datetime.now(timezone.utc)
org = PartyRef(party_id="org:buyer-co", kind="organization")
buyer = PartyRef(party_id="agent:buyer", kind="agent")

contract = GovernedContract(
    contract_id="gc-purchase-001",
    issuer=org,
    subject=buyer,
    authority=[
        AuthorityGrant(
            grant_id="grant-purchase-001",
            granted_by=org.party_id,
            granted_to=buyer.party_id,
            actions=["purchase"],
            resources=["catalog:item-42"],
            purposes=["restock"],
        )
    ],
    allowed_actions=["purchase"],
    allowed_resources=["catalog:item-42"],
    allowed_purposes=["restock"],
    constraints={"max_amount": "1000.00", "currency": "EUR"},
    valid_from=now - timedelta(minutes=1),
    valid_until=now + timedelta(hours=1),
)

intent = ActionIntent(
    intent_id="a2a-task-purchase-001",
    actor=buyer,
    action="purchase",
    resource="catalog:item-42",
    purpose="restock",
    requested_at=now,
    attributes={"amount": "1200.00", "currency": "EUR"},
)

result = evaluate_a2a_consequence(contract, intent, checked_at=now)
extension = to_a2a_extension(result)

print("A2A transport: SUCCESS")
print("Identity/authentication: SUCCESS")
print(f"Governed Contract: {result.outcome.value.upper()}")
print(f"Reason: {result.issues[0].code if result.issues else 'none'}")
print("Execution authorization eligible:", result.conformant)
print("Economic consequence occurred: NO")
print("A2A extension:", extension)
