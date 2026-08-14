# APS draft-03 adapter

Status: experimental adapter pinned to `draft-pidlisnyi-aps-03`.

Reference: https://www.ietf.org/archive/id/draft-pidlisnyi-aps-03.html

The Agent Passport System (APS) Internet-Draft defines cryptographic agent identity, separately signed principal bindings, monotonically attenuated authority delegations, revocation, action references and signed action/decision/result receipts.

This repository does not reimplement or claim conformance with the APS verifier. The adapter consumes a normalized snapshot produced by an external APS verifier and projects only explicitly mapped, already-verified authority facts into a Governed Contract.

```text
APS passport / principal binding / delegation chain
                    |
                    v
          external APS verifier
                    |
        verified authority snapshot
                    |
                    v
         Open Agent Contract adapter
                    |
          Governed Contract v1
                    |
                    v
     separate authorization boundary
```

## Hard boundary

A projected contract is not permission to execute.

```text
APS verification != Governed Contract conformance != execution authorization
```

The adapter therefore keeps these APS results separate and requires each to be `valid` before projection:

- agent identity;
- principal binding;
- delegation chain;
- revocation state.

`invalid`, `indeterminate`, or `unsupported` fails closed.

The deployment also owns the semantic projection from APS scope grants to contract actions, resources and purposes. The adapter checks APS hierarchical scope coverage, including terminal `:*` wildcards, but does not invent business semantics from scope strings.

## Preserved APS facts

The projected contract carries the selected authority chain and the effective APS facets needed downstream:

- scope grants;
- spend limits;
- remaining delegation depth;
- temporal validity;
- reputation ceiling;
- values requirements;
- reversibility ceiling;
- principal-binding and leaf-delegation references;
- verification statuses and optional receipt context.

These are provenance and constraint inputs. Mutable execution-time facts such as revocation freshness and live cumulative spend still belong at the enforcement/authorization boundary and must be revalidated there.

## Deliberate exclusions

This adapter does not:

- verify Ed25519 signatures or DID key authority;
- implement RFC 8785/JCS canonicalization;
- verify APS receipt chains or compute native APS `action_ref` values;
- maintain the APS spend ledger;
- resolve revocation evidence;
- imply an APS A2A binding. Draft-03 specifies MCP and OAuth bindings but explicitly does not specify A2A.

## Draft status

`draft-pidlisnyi-aps-03` is an individual IETF Internet-Draft published 18 July 2026 with intended status Informational. It is work in progress, not an IETF standard. Adapter behavior is pinned to this draft identifier so future revisions can be reviewed explicitly rather than silently changing the trust boundary.
