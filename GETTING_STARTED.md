# Getting Started

Marketing Skills is an evidence-led marketing operating system for AI agents. The canonical source is [`.agents/skills/`](.agents/skills/); public portable bundles are generated under [`skills/`](skills/).

## 1. Fastest install

```bash
npx skills add vinceservidad/marketing-skills
```

List skills first:

```bash
npx skills add vinceservidad/marketing-skills --list
```

Install only what you need:

```bash
npx skills add vinceservidad/marketing-skills \
  --skill google-ads \
  --skill creative-strategy
```

Install everything globally for Codex:

```bash
npx skills add vinceservidad/marketing-skills --skill '*' -g -a codex -y
```

Install everything globally for Claude Code:

```bash
npx skills add vinceservidad/marketing-skills --skill '*' -g -a claude-code -y
```

Other Agent Skills-compatible runtimes can use the same repository.

## 2. Use one skill without installing

```bash
npx skills use vinceservidad/marketing-skills \
  --skill google-ads \
  --agent codex
```

## 3. Use the router when you are unsure

You do not need to memorize all 31 skills.

```text
$marketing-router I need to improve ecommerce growth. Decide which Marketing Skills capability should own this request and what evidence is needed first.
```

If you already know the owner, invoke it directly:

```text
$google-ads Audit this campaign data and separate observations, calculations, inferences, assumptions, and unknowns.

$creative-strategy Turn this verified customer evidence into testable paid-media concepts.
```

## 4. Why single-skill installs still work

Canonical skills share governance contracts, frameworks, workflows, and templates. The generated `skills/<name>/` bundle includes the dependencies required by that skill under `_shared/`.

That means this works independently:

```bash
npx skills add vinceservidad/marketing-skills --skill google-ads
```

Do not edit generated `skills/` bundles. Change `.agents/skills/` and rebuild with:

```bash
python3 scripts/build-portable-skills.py
```

## 5. Advanced managed install

If you want the repository's ownership-aware installer with collision protection, backups, repeat-install safety, and namespaced shared resources:

```bash
git clone https://github.com/vinceservidad/marketing-skills.git
cd marketing-skills

# Codex
bash scripts/install-skills.sh . "$HOME/.codex"

# Claude Code
bash scripts/install-claude-skills.sh
```

See [`INSTALLATION_SAFETY.md`](INSTALLATION_SAFETY.md) for the managed installer contract.

## 6. Pick the right owner

| Need | Primary owner |
|---|---|
| Decide where the business should focus | `$growth-strategy` |
| Decide which skill owns a request | `$marketing-router` |
| Scope, evidence, metrics, access, authorization | `$marketing-intake` |
| Google Ads | `$google-ads` |
| Meta Ads | `$meta-ads` |
| Paid creative strategy | `$creative-strategy` |
| Copywriting | `$copywriting` |
| CRO | `$cro` |
| Customer research | `$customer-research` |
| ICP / JTBD / competitors | `$icp-jtbd` |
| Offer strategy | `$offer-strategy` |
| Pricing / packaging / monetization | `$pricing-monetization` |
| Activation | `$activation` |
| Retention strategy | `$retention-strategy` |
| LTV / payback / cohort economics | `$retention-economics` |
| Tracking / attribution / experiments | `$tracking-measurement` |
| Warehouse / pipeline / BI / dashboards | `$marketing-analytics` |
| Diagnose performance changes | `$performance-diagnostics` |
| Paid-media scaling | `$optimization-scaling` |
| Recurring marketing operations | `$marketing-operations` |
| Executive reporting | `$marketing-reporting` |

[`CAPABILITY-REGISTRY.md`](CAPABILITY-REGISTRY.md) is authoritative.

## 7. Give the system evidence

Useful inputs include:

- business objective and decision
- product, offer, and pricing truth
- market, segment, geography, and timeframe
- campaign or funnel data with metric definitions
- customer research or traceable reviews
- current creative or pages
- unit economics and operating constraints
- authorization scope

The system should identify missing evidence rather than inventing it.

## 8. Live tools are separate

Installing skills does not automatically grant access to Google Ads, Meta, Shopify, GA4, CRM, warehouses, or other platforms.

```text
Marketing Skills = decision system
Connector / MCP / API / browser / database = optional data and action layer
```

Live reads and writes must use an actually available and authorized runtime. See [`integrations/README.md`](integrations/README.md).

## 9. Update

For installs managed by the Agent Skills CLI:

```bash
npx skills update
```

For the advanced cloned-repository installer:

```bash
git pull
bash scripts/install-skills.sh . "$HOME/.codex"
```

or:

```bash
git pull
bash scripts/install-claude-skills.sh
```

## 10. Contributor checks

Before a behavior-changing PR:

```bash
python3 scripts/build-portable-skills.py --check
python3 scripts/build-gpt-knowledge.py --check
python3 scripts/eval.py --static
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check-markdown-links.py
bash scripts/validate-agent-distribution.sh .
```

Read [`AGENTS.md`](AGENTS.md), [`CAPABILITY-REGISTRY.md`](CAPABILITY-REGISTRY.md), [`ARTIFACT-OWNERSHIP.md`](ARTIFACT-OWNERSHIP.md), and [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing governed behavior.
