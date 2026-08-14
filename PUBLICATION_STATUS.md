# Publication Status

Status date: 2026-08-14

## Current fact

`nsolland/open-agent-contract` is a **public GitHub repository**.

The Governed Contract format and reference implementation are available for open, vendor-neutral use under the MIT License. The current package line is `0.3.0`.

## Public repository contents

The public repository contains:

- Governed Contract v1;
- deterministic conformance behavior;
- A2A reference profile/examples;
- general/ephemeral agent-contract lifecycle support;
- tests and package metadata;
- MIT license;
- security and contribution guidance.

The format is intended to remain usable independently of VALO, REHT, any model vendor, agent framework, transport, identity provider, policy engine or execution-governance product.

## Architecture boundary

A conformant Governed Contract is not permission to execute.

The repository defines portable contract/conformance semantics. Organization-controlled authorization and enforcement remain separate.

The exact canonical relationship between Open Agent Contract and VALO GCoP is currently unresolved. Public material MUST NOT describe them as aliases, replacements or parent/child profiles until that relationship is explicitly resolved.

## Release state

The package metadata is `0.3.0`. The canonical next public release is therefore `v0.3.0` on an exact green release head.

An existing historical `v0.1.0` tag predates the current release discipline. It MUST NOT be moved, deleted or retargeted. The corrective action is a new `v0.3.0` release, not rewriting Git history.

A release is considered published only when the tag, package version and exact commit are aligned and CI is green on that commit.

## Release gate

Before publishing a release, verify:

1. no credentials, customer data, private keys or private collaboration material are tracked;
2. all bundled examples/data are safe to publish;
3. package metadata and version match the intended release;
4. tests are green on the exact release head;
5. README and docs preserve `conformance != authorization`;
6. A2A examples do not imply protocol identity/access creates authority;
7. the GCoP relationship remains explicitly unresolved unless separately decided;
8. MIT license and attribution material are complete;
9. the exact release tag/version/hash is recorded.

## Release-state vocabulary

- **public repository** — GitHub metadata reports visibility `public`;
- **release candidate** — repository content is prepared for an identified version but the exact release artifact has not yet been published;
- **published open-source release** — public repository plus an identified tag/version/hash on a validated release head.
