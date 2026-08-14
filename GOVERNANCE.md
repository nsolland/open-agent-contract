# Open Agent Contract Governance

Status: 2026-08-14

Open Agent Contract is an independently usable public contract and reference implementation.

## Change authority

Issues, discussions, papers and external review are proposal inputs. They do not change the contract by themselves.

A normative/public-API change requires a pull request that records:

- rationale;
- contract/API compatibility impact;
- security impact;
- test/conformance impact;
- migration impact;
- target wire-spec and package versions.

## Version surfaces

Two version surfaces are intentionally independent:

- Governed Contract `spec_version`: compatibility of the portable contract semantics/wire representation;
- Python package version: compatibility of this reference implementation/API.

For Governed Contract semantics:

- major = incompatible contract semantics;
- minor = substantive additive semantics/fields/continuation behavior;
- patch = clarification/correction with no behavioral compatibility change.

The Python package remains pre-1.0 and follows its own semantic-version signal.

Historical release tags are immutable. Corrections move forward through new versions rather than retargeting prior tags.

## External review and standardization

Publisher, journal, conference, foundation, standards-body or consortium feedback is proposal/evidence input until incorporated through a versioned accepted change.

If an external standards body or other venue later becomes canonical for the portable contract:

1. record the transfer explicitly here and in the README;
2. tag/freeze the last locally canonical contract version;
3. identify the external canonical source/version and effective date;
4. make this repository a reference implementation/profile/mirror as appropriate;
5. map local package releases to the external contract version;
6. never claim simultaneous competing canonical sources for the same contract.

Discussion may continue locally after transfer, but local experimental changes are non-normative until accepted by the external authority.

## Decision rule

Discussion proposes. Evidence informs. An accepted versioned contract/API change decides.
