# Publication Status

Status date: 2026-08-14

## Current fact

`nsolland/open-agent-contract` is a **public GitHub repository**.

The Governed Contract format and reference implementation are available for open, vendor-neutral use under the MIT License. The current target package line is `0.4.0`, with Governed Contract semantics `1.1.0`.

## Public repository contents

The public repository contains:

- Governed Contract v1.1;
- deterministic conformance behavior;
- exact contract-digest continuation checking;
- A2A reference profile/examples;
- general/ephemeral agent-contract lifecycle support;
- tests and package metadata;
- public governance/versioning rules;
- MIT license;
- security and contribution guidance.

The format is intended to remain usable independently of VALO, REHT, any model vendor, agent framework, transport, identity provider, policy engine or execution-governance product.

## Architecture boundary

A conformant Governed Contract is not permission to execute.

A `current` contract-continuity result is also not permission to execute. It establishes only that the current contract identity/spec/digest matches the contract used for the prior conformance result.

The repository defines portable contract/conformance semantics. Organization-controlled authorization and enforcement remain separate.

The exact canonical relationship between Open Agent Contract and VALO GCoP is currently unresolved. Public material MUST NOT describe them as aliases, replacements or parent/child profiles until that relationship is explicitly resolved.

## Release state

The package target is `0.4.0`; the portable Governed Contract semantics are `1.1.0`. The canonical next public package release is therefore `v0.4.0` on an exact green release head if/when that release is explicitly published.

The prior `0.3.0` line remains historical provenance. An existing historical `v0.1.0` tag predates the current release discipline and MUST NOT be moved, deleted or retargeted. Corrections move forward through new releases.

A release is considered published only when the tag, package version and exact commit are aligned and CI is green on that commit.

## Release gate

Before publishing a release, verify:

1. no credentials, customer data, private keys or private collaboration material are tracked;
2. all bundled examples/data are safe to publish;
3. package metadata, `__version__`, contract `spec_version` and changelog match the intended release;
4. tests are green on the exact release head;
5. README and docs preserve `conformance != authorization` and `contract continuity != authorization`;
6. A2A examples do not imply protocol identity/access creates authority;
7. the GCoP relationship remains explicitly unresolved unless separately decided;
8. `GOVERNANCE.md` accounts for the change/release authority;
9. MIT license and attribution material are complete;
10. the exact release tag/version/hash is recorded.

## Release-state vocabulary

- **public repository** — GitHub metadata reports visibility `public`;
- **release candidate** — repository content is prepared for an identified version but the exact release artifact has not yet been published;
- **published open-source release** — public repository plus an identified tag/version/hash on a validated release head.

## Canonical-authority transition

If a publisher, standards body, foundation or consortium later becomes the normative authority for the portable contract, the transfer is explicit under `GOVERNANCE.md`; this repository then becomes a reference implementation/profile/mirror as declared, rather than a second competing canonical source.
