# Roadmap

This file describes the current maturity state and next system-level milestones. Historical implementation details live in [`CHANGELOG.md`](CHANGELOG.md); capability ownership lives in [`CAPABILITY-REGISTRY.md`](CAPABILITY-REGISTRY.md).

Last reconciled: **2026-09-18**.

## Current state — Governed full-stack Marketing OS

The repository currently has **31 governed skills** in [`.agents/skills/`](.agents/skills/) with one canonical ownership model, shared evidence/governance contracts, behavioral evaluations, and CI validation.

Completed capability areas include:

- marketing routing, intake, shared Marketing Context, and growth strategy
- customer research, ICP/JTBD, competitive intelligence, offer strategy, and pricing/monetization
- Google Ads, Meta Ads, YouTube Ads, TikTok Ads, LinkedIn Ads, programmatic, influencer, affiliate, organic social, PR, and SEO
- creative strategy, copywriting, CRO, static DTC creative direction, and governed 4:5 → centered 1:1 cross-crop safety
- activation, retention strategy, retention economics, and lifecycle marketing
- tracking/measurement, experiment learning, performance diagnostics, marketing reporting, marketing operations, and optimization/scaling
- generated self-contained Agent Skills distribution for Codex, Claude Code, Cursor, Windsurf, GitHub Copilot, OpenCode, and other compatible runtimes from one canonical skill source
- public GitHub onboarding and truth-governed worked-example standards

The capability registry remains authoritative. Marketing analytics engineering is now governed end to end by `$marketing-analytics`, including data contracts, warehouse/pipeline design, metric layers, data quality, BI/dashboard implementation, refresh/backfill governance, and reconciliation. Tracking validity, diagnostic interpretation, reporting narrative, and marketing decisions retain their specialist owners.

## Completed maturity milestones

### Evidence and terminology governance

- Canonical glossary and knowledge taxonomy.
- Observed / calculated / inferred / assumed / unknown evidence separation.
- Platform-currency registry and freshness validation for fast-changing platform claims.
- Exact implementation-state language for proposed, configured, live, observed, verified, and related states.

### Strategy and commercial system

- Growth Strategy with evidence-grounded constraint or constraint-set handling, opportunity portfolio, priorities, non-priorities, sequencing, and learning roadmap.
- Offer Strategy separated from Pricing & Monetization.
- Pricing decisions separated from competitor context, stated preference, modeled economics, and realized commercial evidence.

### Acquisition, creative, and conversion system

- Governed channel owners for the active acquisition/distribution disciplines in the capability registry.
- Creative ideation from research → insight → angle → mechanic → concept → hook → format → proof → test.
- Static creative production direction with placement/crop preflight and cross-crop resilience rules.
- CRO ownership limited to the pre-conversion boundary; Activation owns post-conversion first-value decisions.

### Activation and retention system

- Activation owns first meaningful value, path-to-value, time-to-value, and activation intervention strategy.
- Retention Strategy owns reason diagnosis and cause-matched save/recovery/repeat/renewal/win-back interventions.
- Retention Economics owns realized/predictive cohort economics, LTV, payback, and churn/retention measurement.
- Lifecycle Marketing owns communication segmentation, trigger logic, cadence, suppression, and deliverability.

### Measurement, operations, and scaling system

- Tracking & Measurement owns event integrity, attribution reconciliation, causal evidence, and experiment learning.
- Performance Diagnostics owns anomaly decomposition and competing-cause diagnosis.
- Marketing Operations owns recurring cross-skill loops, state, idempotency, approvals, verification, escalation, and retirement.
- Optimization & Scaling owns paid-media readiness, marginal economics, controlled expansion/de-scaling, pacing, and guardrails.
- Marketing Reporting owns cross-channel executive reporting and recurring stakeholder communication.
- Marketing Analytics owns marketing data contracts, warehouse/pipeline design, semantic metrics, data quality, BI/dashboard implementation, refresh/backfill behavior, lineage, and source-to-output reconciliation.

### Distribution and usability

- `.agents/skills/` remains the canonical skill source.
- `skills/` is a generated portable distribution layer with byte-exact drift checks; it is never hand-maintained.
- The public `npx skills` path is smoke-tested against actual Codex and Claude Code install targets.
- Codex and Claude Code installers generate runtime copies without creating competing skill hierarchies, protect personal files, and keep shared resources in `.marketing-os/`.
- The GPT reference pack is generated from current canonical sources and checked for drift.
- Evaluation cases have executable static validation and an opt-in model-grading harness with offline regression tests. These do not establish a live behavioral pass rate.
- `GETTING_STARTED.md`, `AGENT_GUIDE.md`, `DISTRIBUTION.md`, and root README provide public onboarding.
- Worked examples distinguish synthetic, anonymized, and verified public case studies and prohibit fabricated achieved results.
- `integrations/` defines runtime-neutral connector/MCP/API boundaries, secrets rules, mutation approval, rollback, and verification states without pretending user-specific connections are live.
- `validation/` defines the real-world evidence registry, privacy/publication rules, and validation-state progression; evidence can grow without making repository structure incomplete.

## Current cleanup — System consistency

- Normalize remaining legacy `SKILL.md` files to explicit `## Required inputs` contracts without changing ownership.
- Keep README, roadmap, architecture, capability registry, examples, and distribution docs synchronized with the actual governed system.
- Remove or replace stale compact examples when a stronger governed walkthrough exists.

## Ongoing evidence program — Real-world validation

The validation framework and registry are now implemented. Priority remains **growing trustworthy evidence, not adding skills for the sake of count**.

- Run and review a reproducible live-model benchmark using the evaluation harness. Preserve raw responses, source identity, exclusions, and grading limits; no live behavioral result is claimed by this tooling release.
- Validate high-value skills against anonymized real-world cases where permission and evidence allow.
- Preserve the difference between a worked example and a verified case study.
- Record contradictions, failed hypotheses, negative outcomes, and scope limits rather than publishing only wins.
- Use experiment-learning records to promote only replicated scoped patterns, never one-off results as universal best practices.

## Ongoing deployment program — Provider integrations

The integration contract layer is complete at repository level. Add provider-specific adapters only when a real runtime/account requires them, without moving marketing intelligence out of the skill layer.

- Extend provider-specific source contracts when real platform exports expose a new grain, key, freshness, or mutation boundary.
- Keep Skills as the decision system; treat MCP/connectors/APIs as optional data/action layers governed by `integrations/README.md`.
- Verify each runtime connection separately using documented -> configured -> authenticated -> connected -> authorized -> verified states.
- Package a marketplace-specific plugin only when distribution value justifies it and the target manifest/runtime can be verified; plugin packaging is optional, not a missing core capability.

## Next milestone — Operational maintainability

- Add automated checks that prevent stale capability counts, unsupported roadmap claims, and broken public-navigation links where practical.
- Automate scheduled platform-currency review issues only when a real runtime is configured and verified.
- Establish maintainers, migration policy, and deprecation rules before broader external contribution creates compatibility obligations.
- Continue expanding behavioral evaluations from observed failure modes rather than arbitrary coverage quotas.

## Deliberate non-goals

Do not add a new skill merely because another repository has one. External systems are idea sources only.

Do not duplicate a capability that already has an owner. Improve the existing owner when the gap belongs there.

Do not turn the Marketing OS into one giant MCP server or connector. The governed skill layer remains the marketing intelligence source of truth.

Do not claim a plugin, integration, scheduled loop, live mutation, case-study result, or platform behavior exists until its real state is verified.
