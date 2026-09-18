# Data Contracts and Modeling

Use this reference when designing marketing data models, semantic layers, marts, or warehouse contracts.

## Data-contract minimum

For each source or model declare:

| Field | Requirement |
|---|---|
| Owner | Team/system accountable for meaning and access |
| Source | API/report/table/file/system of record |
| Grain | What one row represents |
| Primary/business key | Stable uniqueness rule |
| Update behavior | Append, mutable rows, snapshot, delete/tombstone |
| Event/business time | Timestamp used for business analysis |
| Ingestion time | When the platform received the record |
| Time zone | Explicit source and reporting zone |
| Currency | Source/reporting currency and FX rule |
| Freshness | Expected availability and tolerance |
| Retention/backfill | History available and replay window |
| Sensitive fields | PII/secrets/access restrictions |
| Reconciliation | Source totals or samples used to verify |

## Grain-first modeling

Write the grain in plain language before SQL or formulas.

Examples:

- one row per Google Ads campaign per account per local calendar date
- one row per order
- one row per order line
- one row per lead status transition
- one row per customer per cohort month

A correct-looking join can still multiply rows. Before joining, state expected cardinality:

- one-to-one
- one-to-many
- many-to-one
- many-to-many

Many-to-many joins require an explicit bridge or allocation rule. Never solve them with an unexamined DISTINCT.

## Metric semantic contract

For every decision-critical metric specify: name, business question, numerator, denominator, inclusions, exclusions, time basis, currency basis, attribution/source, grain, aggregation behavior, maturity window, and owner.

### Aggregation behavior

- Additive: safe to sum across declared dimensions, for example spend within one currency basis.
- Semi-additive: additive across some dimensions but not others, for example ending balance across entities but not time.
- Non-additive: ratio, rate, median, or unique count that must be recalculated at the requested grain.

Never average averages unless the weighting rule is explicit.

## Marketing source boundaries

Keep at least these concepts distinct:

- platform-attributed conversion
- analytics/session-attributed conversion
- CRM-qualified lead/opportunity
- order/revenue from commerce source of truth
- refunds/cancellations
- realized profit/contribution metric when available

Platform-attributed values can be useful for platform optimization but are not automatically deduplicated business truth.

## Recommended model layers

raw/source to staging to core/conformed to marts to semantic/metric layer to dashboard/report/analysis.

Do not force this exact stack when a smaller system is sufficient. The principle is separation of extraction, normalization, business semantics, and presentation.

## Slowly changing and mutable data

State how the system handles renamed campaigns/products, changed budgets/statuses, lead stage changes, order refunds/cancellations, customer attribute changes, and deleted source rows.

If historical state matters, use snapshots/history rather than overwriting the past without trace.

## Identity and deduplication

A dedupe rule must specify the entity, key or matching fields, source priority, time/window rule, conflict resolution, and auditability.

Do not merge users/customers across sources from weak identifiers merely to increase match rate.
