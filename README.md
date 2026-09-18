# Full-Stack Marketing OS

![GitHub](https://img.shields.io/badge/status-public-brightgreen)
![Version](https://img.shields.io/badge/version-v1.19.0-blue)
![Focus](https://img.shields.io/badge/focus-AI%20Marketing-purple)

An evidence-led full-stack marketing skill and operating system for planning, auditing, diagnosing, creating, testing, and improving full-funnel marketing.

Built to help AI agents and modern marketing teams work from governed marketing knowledge instead of isolated prompts, copied playbooks, or unsupported “best practices.”

GitHub is the versioned source of truth. The system combines governed skills, frameworks, playbooks, templates, workflows, shared context, and behavioral evaluations.

## Start here

New to the repository? Read **[`GETTING_STARTED.md`](GETTING_STARTED.md)** first.

It covers the complete path:

```text
GitHub
  ↓
Clone / download
  ↓
Install to Codex or Claude Code
  ↓
Verify
  ↓
Choose a skill or use $marketing-router
  ↓
Provide evidence
  ↓
Run the governed workflow
  ↓
Update from GitHub when the OS changes
```

For AI-agent orchestration rules after installation, see [`AGENT_GUIDE.md`](AGENT_GUIDE.md). For runtime, plugin, MCP, connector, and Custom GPT distinctions, see [`DISTRIBUTION.md`](DISTRIBUTION.md).

## What this is

Full-Stack Marketing OS is currently a **portable skill system**, not a packaged marketplace plugin.

- **OpenAI Codex:** supported as installable local skills.
- **Claude Code:** supported as installable personal skills, with `CLAUDE.md` importing the repository-wide `AGENTS.md` rules.
- **Custom GPT:** supported through the generated [`gpt-knowledge/pack/`](gpt-knowledge/pack/) reference export, with source coverage and drift checks.
- **Live tools and integrations:** supported through host-provided connectors, MCP servers, APIs, browser/computer tools, warehouses, and BI runtimes that satisfy [`integrations/README.md`](integrations/README.md). A dedicated all-in-one marketplace plugin is optional distribution, not a missing marketing capability.

See [`DISTRIBUTION.md`](DISTRIBUTION.md) for exact install paths, terminology, current support state, and plugin boundaries.

## System Map

```text
Business / Marketing Request
        ↓
Marketing Router
        ↓
Growth Strategy or Specialist Owner
        ↓
Framework / Method
        ↓
Playbook / Template / Workflow
        ↓
Measurement + Evaluation
        ↓
Decision / Deliverable / Learning
```

## Governed capabilities

Thirty-one governed skills currently live in [`.agents/skills/`](.agents/skills/), the canonical executable layer.

### Strategy, context, commercial, and customer system

- `$marketing-router` — request routing and owner appointment
- `$marketing-intake` — scope, evidence state, metric definitions, access, authorization, shared Marketing Context
- `$growth-strategy` — business-level growth priorities, constraint/constraint-set diagnosis, opportunity portfolio, sequencing, learning roadmap
- `$customer-research` — interviews, reviews, surveys, evidence synthesis
- `$icp-jtbd` — ICP, Jobs-to-be-Done, buying situations, alternatives, competitive intelligence
- `$offer-strategy` — proposition, value architecture, bundle, proof requirements, risk reversal, legitimate urgency/scarcity
- `$pricing-monetization` — price, value metric, packages/tiers, payment model, discount architecture, willingness-to-pay evidence

### Acquisition, creative, and conversion

- `$google-ads` — Search, Shopping, Performance Max
- `$meta-ads` — structure, audiences, delivery, placements
- `$youtube-ads` — paid-video format, targeting, measurement fit
- `$tiktok-ads` — native creative fit, Spark Ads vs in-feed, targeting/cadence
- `$linkedin-ads` — firmographic/account targeting, Lead Gen Forms, B2B economics
- `$programmatic` — supply-path optimization, inventory verification, fraud screening
- `$influencer-marketing` — creator vetting, compensation, rights, disclosure
- `$affiliate-marketing` — commission structure, attribution integrity, fraud/brand-bidding screening
- `$organic-social` — content strategy, cadence, distribution fit, community management
- `$public-relations` — media relations, pitch strategy, crisis communications
- `$seo` — technical health, organic visibility, content/topic strategy, ranking diagnosis
- `$creative-strategy` — angles, mechanics, hooks, concepts, visual formats, static creative direction, testing
- `$copywriting` — lifecycle, website, sales-page, long-form, and brand copy
- `$cro` — landing/product pages, forms, checkout, and pre-conversion friction

### Activation, retention, measurement, scaling, and operations

- `$activation` — first meaningful value, path-to-value, time-to-value, activation friction
- `$retention-strategy` — churn/lapse reason diagnosis, save/recovery/repeat/renewal/win-back strategy
- `$retention-economics` — LTV, payback, cohort retention/churn, lead-to-revenue maturation
- `$lifecycle-marketing` — segmentation, trigger logic, cadence, suppression, deliverability
- `$tracking-measurement` — event integrity, attribution reconciliation, causal validity, experiment learning
- `$marketing-analytics` — data contracts, warehouse/pipeline design, semantic metric layers, data quality, BI/dashboard implementation, refresh/backfill governance, source reconciliation
- `$performance-diagnostics` — metric change, anomaly, competing explanations, causal triage
- `$optimization-scaling` — paid-media readiness, marginal economics, controlled scaling/de-scaling, pacing
- `$marketing-operations` — recurring cross-skill loops, state, idempotency, approval, verification, escalation
- `$marketing-reporting` — cross-channel executive reporting, recurring reporting cadence, stakeholder scorecards


[`CAPABILITY-REGISTRY.md`](CAPABILITY-REGISTRY.md) is authoritative. A file existing in the repository does not make a capability governed.

## Cross-agent installation

### Codex

```bash
bash scripts/install-skills.sh . "$HOME/.codex"
```

This installs generated runtime copies to `~/.codex/skills/` plus the contracts and libraries needed by those skills.

### Claude Code

```bash
bash scripts/install-claude-skills.sh
```

This installs the same canonical skill set to `~/.claude/skills/`. Do not maintain a second Claude-specific skill hierarchy.

For clone, verification, updating, troubleshooting, skill selection, and concrete usage examples, use [`GETTING_STARTED.md`](GETTING_STARTED.md).

## Repository structure

`.agents/skills/` is the **canonical executable source**. Runtime copies and exports are derived.

```text
.agents/skills/        CANONICAL — governed portable operating skills
~/.codex/skills/       GENERATED — local Codex runtime install
~/.claude/skills/      GENERATED — local Claude Code personal-skill install
skills/                Index only — no competing instructions
frameworks/            Governed decision models and methods
playbooks/             Governed scenario workflows
templates/             Governed reusable deliverable structures
workflows/             Governed execution sequences
agents/                Agent-role documentation, non-executable
gpt-knowledge/pack/     Generated Custom GPT reference export, non-canonical
integrations/           Runtime-neutral connector/MCP/API contracts and truth-state registry
validation/             Real-world validation evidence registry and publication rules
evaluations/           Routing cases and reviewer checklists
tests/evaluations/     Versioned decision cases and executable suite registry
examples/              Synthetic worked demonstrations
scripts/               Safe installers, validators, export builder, evaluation harness
docs/archive/          Historical material excluded from active retrieval
```

See [`ARCHITECTURE.md`](ARCHITECTURE.md), [`ARTIFACT-OWNERSHIP.md`](ARTIFACT-OWNERSHIP.md), and [`DISTRIBUTION.md`](DISTRIBUTION.md).

## Example usage

```text
$growth-strategy Decide where the business should focus next from the evidence I provide.

$google-ads Audit current campaign performance and separate observations from assumptions.

$creative-strategy Turn verified research into testable ad concepts and production-ready static directions.

$marketing-router Decide which Marketing OS skill should own this request when I am not sure.
```

More worked prompts and a skill-selection table are in [`GETTING_STARTED.md`](GETTING_STARTED.md).

## Worked examples

Want to see the OS make a decision end-to-end? Start in [`examples/`](examples/).

Flagship walkthroughs:

- [`Ecommerce Growth Diagnosis`](examples/ecommerce-growth/) — business objective → evidence → constraint set → specialist handoffs → non-priorities → measurement
- [`Google Ads Audit`](examples/google-ads-audit/) — query/product/margin/marginal-efficiency diagnosis without blanket channel rules
- [`Meta Ads Audit & Creative Testing`](examples/meta-ads/) — attribution reconciliation → prospecting/retargeting → creative quality → frequency/audience diagnosis → controlled testing → scaling gate
- [`DTC Creative Strategy`](examples/creative-strategy/) — synthetic VOC → JTBD → angle → mechanic → concept → 4:5 production direction → centered 1:1 cross-crop validation
- [`Scaling Refusal`](examples/scaling-refusal/) — hold a budget increase when blended ROAS masks unresolved economics and an invalid before/after comparison
- [`Shopify CRO Audit`](examples/shopify-cro/) — funnel evidence → mobile checkout diagnosis → focused hypothesis instead of full-site redesign

These are **worked examples**, not performance case studies. Synthetic/anonymized examples demonstrate how the system decides; verified public case studies require real publishable evidence. See [`examples/WORKED-EXAMPLE-STANDARD.md`](examples/WORKED-EXAMPLE-STANDARD.md).

Scaling is not defined as spending more. The system requires source-of-truth business evidence, economics, marginal efficiency, readiness, constraints, capacity, guardrails, and explicit authorization before any live change. It rejects universal budget-increase percentages and does not treat platform attribution or recommendations as proof.

## Verify the exports and evaluation tooling

```bash
python3 scripts/build-gpt-knowledge.py --check
python3 scripts/eval.py --static
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check-markdown-links.py
bash scripts/validate-agent-distribution.sh .
python3 scripts/validate-system-boundaries.py
```

The GPT pack is generated from current canonical material. Rebuild it with
`python3 scripts/build-gpt-knowledge.py` after changing exported sources; follow
[`gpt-knowledge/README.md`](gpt-knowledge/README.md) for upload instructions.

Static checks validate case structure, registration, references, and selected
claim patterns. Offline regression tests validate the tooling. Neither is a
behavioral pass rate or proof of better marketing outcomes. The opt-in live
harness records model responses and grading evidence; see
[`evaluations/README.md`](evaluations/README.md) for scope, costs, and review limits.
No live model benchmark has been run as part of this reconciliation.

## Design principles

- Evidence before assumptions
- Strategy before tactics
- Business outcomes before platform metrics
- One owner per decision
- Frameworks organize thinking; they do not prove outcomes
- Reversible learning before large irreversible commitments
- Human judgment before automation
- Canonical source before runtime/export copies

## Roadmap

The detailed, reconciled roadmap is in [`ROADMAP.md`](ROADMAP.md). Current priorities are:

- run and review a reproducible live-model benchmark; distinguish grading output from human-reviewed behavior and business outcomes
- grow the real-world validation registry with anonymized or verified-public cases where permission and evidence allow; preserve nulls, failures, and scope limits
- apply the governed integration contract to provider-specific adapters only when a real runtime/account needs them; connection state remains runtime-specific
- add maintainability checks that prevent stale capability counts, roadmap claims, and public-navigation drift
- expand behavioral evaluations and worked examples only when real usage exposes a decision-quality gap

## Creator

Built by Vince Servidad, a Paid Acquisition Specialist focused on Google Ads, Meta Ads, Shopify growth, CRO, creative strategy, and AI marketing systems.
