# Publication Status

Status date: 2026-08-14

## Current fact

`nsolland/open-agent-contract` is currently hosted as a **private GitHub repository**.

The Governed Contract format and reference implementation are intended for open, vendor-neutral use under the MIT License. Open-source intent, an open license and actual repository visibility are separate facts.

Until GitHub visibility is changed to public, this repository MUST NOT be described as a publicly accessible open-source repository.

## Intended public release

The intended release contains:

- Governed Contract v1;
- deterministic conformance behavior;
- A2A reference profile/examples;
- general/ephemeral agent-contract lifecycle support;
- tests and package metadata;
- MIT license.

The format is intended to remain usable independently of VALO, REHT, any model vendor, agent framework, transport, identity provider, policy engine or execution-governance product.

## Architecture boundary

A conformant Governed Contract is not permission to execute.

The repository defines portable contract/conformance semantics. Organization-controlled authorization and enforcement remain separate.

The exact canonical relationship between Open Agent Contract and VALO GCoP is currently unresolved. Public-release material MUST NOT describe them as aliases, replacements or parent/child profiles until that relationship is explicitly resolved.

## Public-release gate

Before changing repository visibility to public, verify:

1. no credentials, customer data, private keys or private collaboration material are tracked;
2. all bundled examples/data are safe to publish;
3. package metadata and version match the intended release;
4. tests are green on the exact release head;
5. README and docs preserve `conformance != authorization`;
6. A2A examples do not imply protocol identity/access creates authority;
7. the GCoP relationship remains explicitly unresolved unless separately decided;
8. MIT license and attribution material are complete;
9. a release tag/version is selected;
10. GitHub repository visibility is explicitly changed to `public` by an authorized repository administrator.

## Release-state vocabulary

- **open-source candidate** — code is licensed/intended for open release but may still be privately hosted;
- **public repository** — GitHub metadata reports visibility `public`;
- **published open-source release** — public repository plus identified release/tag/package artifact.

## Current blocker

The remaining publication blocker recorded here is repository visibility. The connected automation used for this update does not expose a repository-visibility mutation, so the private→public switch requires a separate authorized GitHub administration action.
