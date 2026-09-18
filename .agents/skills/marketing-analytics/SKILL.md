---
name: marketing-analytics
description: Govern marketing analytics engineering when the work is to design, build, repair, or verify data contracts, source models, warehouse transformations, semantic metric layers, recurring pipelines, data-quality controls, or BI dashboards rather than merely analyze an already trustworthy dataset.
---

# Marketing Analytics

Own the data-engineering and BI layer that turns marketing and commercial source systems into decision-ready, reproducible datasets and dashboards.

Use this skill when the requested deliverable is a data product: a contract, model, pipeline, metric layer, dashboard, refresh process, lineage map, reconciliation system, or analytics implementation.

Do not use it to replace the decision owner. $tracking-measurement owns tracking architecture and attribution validity; $performance-diagnostics owns causal triage and interpretation of metric changes; $marketing-reporting owns stakeholder communication; channel and business skills own the decisions made from the data.

## Required inputs

Establish the smallest decision-grade specification before designing or changing the analytics layer:

- business questions and decisions the data product must support
- source systems and authoritative fields
- entity grain, join keys, event identifiers, account/store/property IDs, and deduplication rules
- metric definitions, attribution boundaries, time zones, currencies, tax/refund/discount treatment, and reporting windows
- required dimensions, measures, cohorts, and segmentation
- refresh cadence, acceptable latency, backfill window, retention, and recovery expectations
- current warehouse, database, spreadsheet, BI, orchestration, or transformation stack when one exists
- access, privacy, compliance, authorization, and secrets boundary
- reconciliation samples or known source totals that can verify correctness
- downstream consumers and required implementation state: design only, configured, processing, or verified

If a missing definition can materially change the schema or metric meaning, stop that portion at a documented contract rather than inventing it.

## Method

1. Name the decision contract. State what business decisions the data product must support and which metrics are decision-critical.
2. Inventory sources and authority. For every source, record system, object/table/report, extraction method, grain, primary/business keys, update behavior, freshness, and authoritative fields.
3. Define grain before joins. Declare the row grain for raw/staging/core/mart outputs. Identify one-to-many and many-to-many relationships before writing aggregation logic.
4. Define metric semantics. Specify numerator, denominator, inclusions/exclusions, time basis, currency, attribution source, and whether the measure is additive, semi-additive, or non-additive.
5. Design the transformation path. Prefer explicit layers such as source/raw to staging to core/conformed to marts/semantic layer. Preserve source values needed for reconciliation.
6. Design idempotent ingestion and backfills. A rerun should not double-count data. Declare incremental keys, late-arriving behavior, deletion/update handling, watermark logic, and safe replay/backfill boundaries.
7. Add data-quality controls. Test uniqueness, nullability, accepted values, referential integrity, freshness, volume anomalies, reconciliation to source totals, and metric invariants where relevant.
8. Design BI/dashboard semantics. Dashboards consume governed measures and dimensions; they do not redefine the same KPI independently in each chart. State filters, default windows, drill paths, freshness, caveats, and ownership.
9. Implement only through an authorized runtime. SQL, dbt, warehouse, spreadsheet, BI, API, connector, or orchestration changes require an actually available tool and appropriate authorization. Otherwise return an implementation-ready specification.
10. Verify end to end. Reconcile a bounded sample from source to transformed model to final metric/dashboard. Report mismatches before calling the implementation verified.
11. Publish lineage and runbook. Record ownership, dependencies, refresh schedule, failure/retry behavior, alerting, rollback/backfill procedure, and known limitations.

## Decision rules

- Never join tables before declaring their grains and expected cardinality.
- Never silently deduplicate events, orders, leads, users, or conversions without a stated key and rule.
- Never aggregate platform-attributed conversions across platforms as if they were deduplicated business revenue.
- Keep source-system facts separate from modeled or attributed values.
- Make time zone, currency, tax, discounts, refunds, cancellations, and FX treatment explicit when they affect business metrics.
- Prefer stable business keys over display names.
- Preserve raw/source-level fields needed for audit and reconciliation.
- Treat late-arriving data, mutable source rows, deletions, and backfills as normal pipeline design concerns rather than edge cases.
- A dashboard is not verified because it renders. Verify metric values against source-of-truth samples.
- A data-quality test passing does not prove the business definition is correct; both semantic definition and technical implementation must be validated.
- Minimize personal data. Do not copy customer-level PII into marts or dashboards when the decision can be supported with less sensitive data.
- Do not create credentials, expose secrets, or widen access scopes to make an integration easier.
- Do not mutate a production warehouse, BI asset, spreadsheet, connector, or scheduled pipeline without explicit authorization for that scope.

## Ownership boundaries

Route to:

- $marketing-intake when metric definitions, source authority, access, scope, or authorization are materially unclear.
- $tracking-measurement for event instrumentation, conversion architecture, attribution reconciliation, incrementality, or experiment validity.
- $performance-diagnostics when trustworthy data already exists and the main question is why a metric changed.
- $retention-economics for LTV/payback/cohort economics methodology; this skill may engineer the dataset that implements the approved definitions.
- $optimization-scaling for paid-media allocation and scale decisions after the data is trustworthy.
- $marketing-reporting for stakeholder narrative, cadence, scorecards, and executive communication after the underlying dataset/metrics are governed.
- channel or commercial owners for the marketing action chosen from the analysis.

## Output contract

Return the smallest useful combination of:

### Decision contract
- decisions supported
- authoritative sources
- critical metric definitions
- freshness/latency requirement
- privacy/access boundary

### Data contract
- source to target mapping
- grain and keys
- dimensions/measures
- transformation rules
- update/backfill behavior
- ownership

### Model / pipeline design
- layer/model names
- dependencies
- incremental strategy
- tests and reconciliation checks
- failure/retry/backfill behavior

### Dashboard / BI specification
- governed metrics
- dimensions/filters
- views and drill paths
- freshness indicator
- caveats and source lineage

### Verification record
- source sample
- transformed result
- reconciliation
- mismatches
- implementation state
- unresolved risks

Use references/data-contracts-and-modeling.md for schema and metric-layer design and references/pipelines-quality-and-dashboarding.md for pipeline, quality, and BI implementation rules.

## QA

Before finalizing, verify:

- Is each important table/model grain explicit?
- Are keys and join cardinalities stated?
- Are metric semantics separate from source extraction?
- Are time, currency, attribution, refunds/discounts, and dedupe rules explicit where relevant?
- Can incremental loads/backfills rerun without double counting?
- Are source reconciliation and data-quality checks defined?
- Does the dashboard consume governed metrics rather than redefine them?
- Are privacy and access minimized?
- Is implementation state exact?
- Were production mutations gated by actual authorization?
- Can another operator trace a final metric back to its source and transformation logic?
