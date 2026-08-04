"""Tests for the isolated ephemeral agent contract."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from open_agent_contract.ephemeral import (
    AgentOrigin,
    BoundedMandate,
    EphemeralAgentStatus,
    EphemeralContractRegistry,
    EvidenceDeliveryPolicy,
    IsolatedEphemeralAgentContract,
    IsolationBoundary,
    LifecycleWindow,
    NeedToAskAcquireBinding,
    OperatingMemoryLease,
)


BASE = datetime(2026, 8, 4, 13, 0, tzinfo=timezone.utc)


def make_contract(**overrides) -> IsolatedEphemeralAgentContract:
    values = {
        "contract_id": "iac-001",
        "agent_id": "acquirer-001",
        "origin": AgentOrigin(
            principal_id="principal-001",
            requesting_agent_id="requester-001",
            request_id="ask-001",
            parent_contract_id="parent-001",
            delegation_chain_id="chain-001",
            delegation_chain_digest="sha256:chain",
        ),
        "need_binding": NeedToAskAcquireBinding(
            ask_request_id="ask-001",
            ask_reason="Fetch the minimum evidence required for invoice validation",
            acquire_decision_id="acquire-decision-001",
            acquisition_agent_id="acquirer-001",
            reht_clearance_id="clearance-001",
            racs_decision_id="racs-001",
            gateway_policy_id="gateway-policy-001",
            veritas_stream_id="veritas-001",
        ),
        "mandate": BoundedMandate(
            purpose="Validate one invoice against its purchase order",
            task_scope=["invoice.validate"],
            allowed_sources=["erp:invoice:INV-001", "erp:purchase-order:PO-001"],
            allowed_tools=["erp.read_invoice", "erp.read_purchase_order"],
            allowed_resources=["invoice:INV-001", "purchase-order:PO-001"],
            prohibited_actions=["payment.execute", "record.update"],
            max_actions=2,
        ),
        "isolation": IsolationBoundary(
            silo_id="silo-finance-001",
            gateway_enforcement_id="gateway-enforcement-001",
            credential_broker_ref="broker-lease-001",
            network_egress_allowlist=["erp.internal"],
        ),
        "memory": OperatingMemoryLease(
            owner_id="enterprise-001",
            provenance_refs=["invoice:INV-001", "purchase-order:PO-001"],
            allowed_readers=["acquirer-001"],
            allowed_writers=["acquirer-001"],
            memory_classes=["working:evidence"],
            max_bytes=1_000_000,
            retention_until=BASE + timedelta(minutes=10),
        ),
        "delivery": EvidenceDeliveryPolicy(
            recipient_agent_id="requester-001",
            allowed_fields=["invoice_id", "purchase_order_id", "match_result"],
            redaction_profile_id="redaction-finance-minimal-v1",
        ),
        "lifecycle": LifecycleWindow(
            created_at=BASE,
            activate_by=BASE + timedelta(minutes=1),
            expires_at=BASE + timedelta(minutes=10),
            deletion_due_at=BASE + timedelta(minutes=11),
        ),
        "max_lifetime_seconds": 900,
    }
    values.update(overrides)
    return IsolatedEphemeralAgentContract(**values)


def test_contract_collects_origin_authority_silo_memory_and_disposal() -> None:
    contract = make_contract()
    assert contract.status == EphemeralAgentStatus.DRAFT
    assert contract.need_binding.reht_clearance_id == "clearance-001"
    assert contract.isolation.silo_id == "silo-finance-001"
    assert contract.memory.delete_on_termination is True
    assert len(contract.digest()) == 64


def test_digest_is_deterministic() -> None:
    contract = make_contract()
    assert contract.digest() == contract.digest()


def test_wildcards_are_forbidden() -> None:
    with pytest.raises(ValueError, match="wildcards are forbidden"):
        BoundedMandate(
            purpose="unsafe",
            task_scope=["invoice.validate"],
            allowed_sources=["erp:*"],
        )


def test_further_delegation_is_forbidden() -> None:
    with pytest.raises(ValueError, match="cannot further delegate"):
        BoundedMandate(
            purpose="unsafe",
            task_scope=["invoice.validate"],
            allowed_sources=["erp:invoice:INV-001"],
            allow_further_delegation=True,
        )


def test_raw_credentials_and_cross_silo_access_are_forbidden() -> None:
    with pytest.raises(ValueError, match="cross-silo access"):
        IsolationBoundary(
            silo_id="silo-1",
            gateway_enforcement_id="gateway-1",
            cross_silo_access=True,
        )
    with pytest.raises(ValueError, match="raw credentials"):
        IsolationBoundary(
            silo_id="silo-1",
            gateway_enforcement_id="gateway-1",
            raw_credentials_exposed=True,
        )


def test_contract_lifetime_is_bounded() -> None:
    lifecycle = LifecycleWindow(
        created_at=BASE,
        activate_by=BASE + timedelta(minutes=1),
        expires_at=BASE + timedelta(hours=2),
        deletion_due_at=BASE + timedelta(hours=2, minutes=1),
    )
    with pytest.raises(ValueError, match="lifetime exceeds"):
        make_contract(lifecycle=lifecycle, max_lifetime_seconds=900)


def test_memory_cannot_outlive_deletion_deadline() -> None:
    memory = OperatingMemoryLease(
        owner_id="enterprise-001",
        provenance_refs=["invoice:INV-001"],
        allowed_readers=["acquirer-001"],
        max_bytes=1000,
        retention_until=BASE + timedelta(minutes=12),
    )
    with pytest.raises(ValueError, match="memory retention cannot outlive"):
        make_contract(memory=memory)


def test_active_status_requires_activation_receipt() -> None:
    with pytest.raises(ValueError, match="requires activation receipt"):
        make_contract(status=EphemeralAgentStatus.ACTIVE)


def test_activation_and_execution_binding_remain_separate_from_authorization() -> None:
    registry = EphemeralContractRegistry()
    registry.register(make_contract())
    active = registry.activate("iac-001", "receipt-activation", BASE + timedelta(seconds=30))

    result = registry.verify_execution_binding(
        "iac-001",
        agent_id="acquirer-001",
        tool="erp.read_invoice",
        resource="invoice:INV-001",
        now=BASE + timedelta(minutes=2),
    )

    assert active.status == EphemeralAgentStatus.ACTIVE
    assert result["valid"] is True
    assert result["requires_per_action_authorization"] is True
    assert result["racs_decision_id"] == "racs-001"


def test_execution_binding_rejects_wrong_agent_tool_and_resource() -> None:
    registry = EphemeralContractRegistry()
    registry.register(make_contract())
    registry.activate("iac-001", "receipt-activation", BASE + timedelta(seconds=30))

    result = registry.verify_execution_binding(
        "iac-001",
        agent_id="other-agent",
        tool="erp.write_invoice",
        resource="invoice:OTHER",
        now=BASE + timedelta(minutes=2),
    )

    assert result["valid"] is False
    assert set(result["issues"]) == {
        "agent_mismatch",
        "tool_out_of_scope",
        "resource_out_of_scope",
    }


def test_revocation_closes_contract_and_requires_deletion_receipt() -> None:
    registry = EphemeralContractRegistry()
    registry.register(make_contract())
    registry.activate("iac-001", "receipt-activation", BASE + timedelta(seconds=30))
    revoked = registry.revoke(
        "iac-001",
        reason="request withdrawn",
        receipt_id="receipt-revocation",
        now=BASE + timedelta(minutes=3),
    )

    result = registry.verify_execution_binding(
        "iac-001", agent_id="acquirer-001", now=BASE + timedelta(minutes=4)
    )
    deleted = registry.mark_deleted(
        "iac-001", "receipt-zero-mem", BASE + timedelta(minutes=4)
    )

    assert revoked.status == EphemeralAgentStatus.REVOKED
    assert result["valid"] is False
    assert "contract_not_active" in result["issues"]
    assert deleted.status == EphemeralAgentStatus.DELETED
    assert deleted.receipt_ids["deletion"] == "receipt-zero-mem"


def test_expiration_requires_veritas_receipt() -> None:
    registry = EphemeralContractRegistry()
    registry.register(make_contract())
    registry.activate("iac-001", "receipt-activation", BASE + timedelta(seconds=30))

    with pytest.raises(ValueError, match="has not reached"):
        registry.expire("iac-001", "receipt-expiration", BASE + timedelta(minutes=9))

    expired = registry.expire(
        "iac-001", "receipt-expiration", BASE + timedelta(minutes=10)
    )
    assert expired.status == EphemeralAgentStatus.EXPIRED
    assert expired.lifecycle.expired_at == BASE + timedelta(minutes=10)


def test_naive_timestamps_are_rejected() -> None:
    with pytest.raises(ValueError, match="must include a timezone"):
        LifecycleWindow(
            created_at=datetime(2026, 8, 4, 13, 0),
            activate_by=BASE + timedelta(minutes=1),
            expires_at=BASE + timedelta(minutes=10),
            deletion_due_at=BASE + timedelta(minutes=11),
        )
