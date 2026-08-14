# Work anchor — Governed Contract continuity

- Active delivery: make contract-digest continuity explicit for portable Governed Contract handoff and document public change governance.
- Repository: `nsolland/open-agent-contract`
- Canonical base: `66bd0b9f419f3ee856910fda5efad6e7c7d09bb4`
- Branch: `feat/v1.1-continuity`
- Draft PR: `#10`
- Owner/claim: ChatGPT on behalf of Njål; portable contract/reference implementation.
- Owned files: `open_agent_contract/governed.py`, `open_agent_contract/a2a.py`, `open_agent_contract/__init__.py`, `tests/test_governed.py`, `docs/governed-contract-v1.md`, `README.md`, `PUBLICATION_STATUS.md`, `pyproject.toml`, `CHANGELOG.md`, `GOVERNANCE.md`, `.github/ISSUE_TEMPLATE/normative_contract_change.md`, this anchor.
- Dependencies: public `0.3.0` package line; no VALO runtime dependency.
- Version decision: Governed Contract wire semantics `1.1.0`; package `0.4.0` because the public package is still pre-1.0.
