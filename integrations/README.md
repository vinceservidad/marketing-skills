# Integration Contract Layer

Full-Stack Marketing OS is runtime-neutral. Skills contain the decision logic; integrations provide optional access to external data and actions.

A dedicated all-in-one marketplace plugin is not required for system completeness. Codex, Claude Code, ChatGPT, or another host may expose connectors, MCP servers, APIs, browser/computer use, or local tools. An adapter is usable only when it satisfies this contract and its actual connection state is verified.

## Integration states

Use exact states:

documented -> configured -> authenticated -> connected -> authorized -> verified

- documented: contract exists only
- configured: adapter/tool is installed or registered
- authenticated: credentials/session are valid
- connected: a bounded read succeeds against the intended account/resource
- authorized: the requested read/write scope is explicitly permitted
- verified: the exact requested action/read has been checked against the external source

Never describe an adapter as live from documentation alone.

## Required adapter fields

Every registry entry declares:

- id and provider
- capability class
- read/write boundary
- authentication mechanism
- minimum scopes/permissions
- secrets location rule
- supported objects/actions
- mutation approval rule
- verification rule
- rollback/recovery rule for writes
- data freshness expectations
- current repository status

See registry.json. The registry describes contracts, not user-specific connection state.

## Read contract

Before using a live source:

1. identify the exact account/property/store/project/resource
2. establish the intended source of truth
3. use least-privilege read scope
4. preserve provider timestamps/time zones/currencies
5. report freshness and query window
6. reconcile a bounded sample when the data affects a material decision

## Mutation contract

External mutations require:

1. an owning Marketing OS skill
2. explicit authorization for the exact account/resource/action
3. pre-change state capture when rollback is meaningful
4. bounded write
5. provider response capture
6. post-write readback/verification
7. exact implementation state
8. rollback or escalation if verification fails

Approval for one budget, campaign, price, tracking rule, audience, page, or account does not authorize a materially different mutation.

## Secrets

- never commit credentials, API keys, refresh tokens, session cookies, private keys, or account secrets
- use the host runtime/secret manager
- do not echo secrets into logs, prompts, artifacts, or examples
- adapters should fail closed when credentials are absent

## Host-provided connectors and MCP

A host-provided connector or MCP server can satisfy the integration layer without this repository shipping provider credentials or duplicating SDKs.

The skill must still verify:

- the tool is actually available
- the intended account/resource is selected
- read/write scope matches the task
- the operation is authorized
- the resulting state is read back when material

Tool availability is runtime state, not repository state.

## Plugin packaging

A marketplace/plugin package is a distribution choice, not the source of marketing intelligence. If a future provider-specific package is created, it must:

- point to canonical skills rather than fork them
- declare permissions/resources
- store no credentials in the repository
- preserve approval and verification gates
- pass the registry validator
- be described as installable/live only after the target platform installation is actually verified

This prevents "plugin not packaged" from being treated as an incomplete marketing capability.

## Validation

Run:

python3 scripts/validate-system-boundaries.py

The validator checks registry shape and truth-state constraints. It does not authenticate user accounts or prove a provider is reachable.
