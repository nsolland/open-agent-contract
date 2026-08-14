"""Open Agent Contract public API."""

from .governed import (
    ActionIntent,
    AuthorityGrant,
    CompletionCondition,
    ConformanceIssue,
    ConformanceOutcome,
    ConformanceResult,
    EvidenceRequirement,
    GovernedContract,
    PartyRef,
    check_conformance,
)
from .ephemeral import (
    AgentOrigin,
    BoundedMandate,
    DeliveryMode,
    EphemeralAgentStatus,
    EphemeralContractRegistry,
    EvidenceDeliveryPolicy,
    IsolatedEphemeralAgentContract,
    IsolationBoundary,
    IsolationClass,
    LifecycleWindow,
    NeedToAskAcquireBinding,
    OperatingMemoryLease,
)

__version__ = "0.3.0"

__all__ = [
    "ActionIntent", "AuthorityGrant", "CompletionCondition",
    "ConformanceIssue", "ConformanceOutcome", "ConformanceResult",
    "EvidenceRequirement", "GovernedContract", "PartyRef", "check_conformance",
    "AgentOrigin", "BoundedMandate", "DeliveryMode", "EphemeralAgentStatus",
    "EphemeralContractRegistry", "EvidenceDeliveryPolicy",
    "IsolatedEphemeralAgentContract", "IsolationBoundary", "IsolationClass",
    "LifecycleWindow", "NeedToAskAcquireBinding", "OperatingMemoryLease",
]
