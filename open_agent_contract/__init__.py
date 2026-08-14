"""Open Agent Contract public API."""

from .a2a import (
    A2A_GOVERNED_CONTRACT_EXTENSION_URI,
    A2AGovernedContractExtension,
    evaluate_a2a_consequence,
    to_a2a_extension,
)
from .aps import (
    APS_DRAFT,
    APS_DRAFT_URL,
    APSContractProjection,
    APSVerificationStatus,
    APSVerifiedAuthoritySnapshot,
    project_verified_aps_authority,
)
from .governed import (
    ActionIntent,
    AuthorityGrant,
    CompletionCondition,
    ConformanceIssue,
    ConformanceOutcome,
    ConformanceResult,
    ContinuationOutcome,
    ContinuationResult,
    EvidenceRequirement,
    GovernedContract,
    PartyRef,
    check_conformance,
    verify_contract_continuity,
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

__version__ = "0.4.0"

__all__ = [
    "A2A_GOVERNED_CONTRACT_EXTENSION_URI", "A2AGovernedContractExtension",
    "evaluate_a2a_consequence", "to_a2a_extension",
    "APS_DRAFT", "APS_DRAFT_URL", "APSContractProjection",
    "APSVerificationStatus", "APSVerifiedAuthoritySnapshot",
    "project_verified_aps_authority",
    "ActionIntent", "AuthorityGrant", "CompletionCondition",
    "ConformanceIssue", "ConformanceOutcome", "ConformanceResult",
    "ContinuationOutcome", "ContinuationResult", "EvidenceRequirement",
    "GovernedContract", "PartyRef", "check_conformance",
    "verify_contract_continuity",
    "AgentOrigin", "BoundedMandate", "DeliveryMode", "EphemeralAgentStatus",
    "EphemeralContractRegistry", "EvidenceDeliveryPolicy",
    "IsolatedEphemeralAgentContract", "IsolationBoundary", "IsolationClass",
    "LifecycleWindow", "NeedToAskAcquireBinding", "OperatingMemoryLease",
]
