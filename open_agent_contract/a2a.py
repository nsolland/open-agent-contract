"""A2A Governed Contract extension profile.

This adapter binds an A2A task/message to a portable Governed Contract and
returns deterministic contract conformance. It never authorizes execution.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from pydantic import BaseModel, Field

from .governed import (
    ActionIntent,
    ConformanceIssue,
    ConformanceOutcome,
    ConformanceResult,
    GovernedContract,
    check_conformance,
)

A2A_GOVERNED_CONTRACT_EXTENSION_URI = (
    "https://openagentcontract.org/extensions/governed-contract/v1"
)


class A2AGovernedContractExtension(BaseModel):
    """Portable metadata carried with an A2A interaction."""

    uri: str = A2A_GOVERNED_CONTRACT_EXTENSION_URI
    required: bool = True
    contract_id: str
    contract_digest: str
    intent_id: str
    outcome: ConformanceOutcome
    issues: list[ConformanceIssue] = Field(default_factory=list)
    checked_at: datetime
    authorization_required: bool = True


def evaluate_a2a_consequence(
    contract: GovernedContract,
    intent: ActionIntent,
    *,
    checked_at: datetime | None = None,
) -> ConformanceResult:
    """Evaluate contract conformance plus portable transaction constraints.

    Recognised v1 constraint keys:
      * ``max_amount`` — numeric ceiling against ``intent.attributes.amount``
      * ``currency`` — exact match against ``intent.attributes.currency``

    Unknown constraints are left to extension namespaces or downstream policy.
    A conformant result remains non-authoritative for execution.
    """

    result = check_conformance(contract, intent, checked_at=checked_at)
    if not result.conformant:
        return result

    issues: list[ConformanceIssue] = []
    constraints = contract.constraints

    if "max_amount" in constraints:
        raw_amount = intent.attributes.get("amount")
        if raw_amount is None:
            issues.append(
                ConformanceIssue(
                    code="amount_missing",
                    message="transaction amount required by max_amount constraint",
                )
            )
        else:
            try:
                amount = Decimal(str(raw_amount))
                maximum = Decimal(str(constraints["max_amount"]))
            except (InvalidOperation, ValueError):
                issues.append(
                    ConformanceIssue(
                        code="amount_invalid",
                        message="transaction amount or max_amount is not numeric",
                    )
                )
            else:
                if amount > maximum:
                    issues.append(
                        ConformanceIssue(
                            code="amount_exceeds_mandate",
                            message=f"amount {amount} exceeds contract ceiling {maximum}",
                        )
                    )

    if "currency" in constraints:
        currency = intent.attributes.get("currency")
        if currency is None:
            issues.append(
                ConformanceIssue(
                    code="currency_missing",
                    message="transaction currency required by contract",
                )
            )
        elif str(currency).upper() != str(constraints["currency"]).upper():
            issues.append(
                ConformanceIssue(
                    code="currency_mismatch",
                    message="transaction currency does not match contract currency",
                )
            )

    if not issues:
        return result

    now = checked_at or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    else:
        now = now.astimezone(timezone.utc)

    return ConformanceResult(
        outcome=ConformanceOutcome.NON_CONFORMANT,
        contract_id=contract.contract_id,
        intent_id=intent.intent_id,
        contract_digest=contract.digest(),
        checked_at=now,
        issues=issues,
    )


def to_a2a_extension(result: ConformanceResult) -> dict[str, Any]:
    """Return transport-neutral A2A extension metadata."""

    return A2AGovernedContractExtension(
        contract_id=result.contract_id,
        contract_digest=result.contract_digest,
        intent_id=result.intent_id,
        outcome=result.outcome,
        issues=result.issues,
        checked_at=result.checked_at,
    ).model_dump(mode="json")
