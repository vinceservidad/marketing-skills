# Pipelines, Data Quality, and Dashboarding

## Pipeline contract

A recurring data flow should declare:

- trigger or schedule
- source and destination
- extraction window
- incremental/watermark key
- late-arriving-data window
- retry policy
- idempotency strategy
- backfill procedure
- failure state
- alert/escalation owner
- verification step
- rollback or safe-disable method

A written schedule is not an active schedule. Call it active only when the runtime is configured and verified.

## Idempotency

A rerun of the same logical input should not create duplicate business facts.

Common patterns include upsert by stable source ID, partition overwrite for bounded dates, merge using source version/update timestamp, or immutable append with a governed latest-state view.

Document the selected pattern and its failure modes.

## Data-quality layers

### Schema
- required columns exist
- types are valid
- enumerations are expected

### Entity integrity
- primary key uniqueness
- required foreign keys resolve
- duplicate rate is explained

### Freshness and volume
- newest event/business date within tolerance
- row counts/volume changes reviewed against source behavior
- missing partitions/dates detected

### Business invariants
Examples:
- order-line totals reconcile to order totals within defined rules
- spend is nonnegative unless credits are explicitly represented
- conversion rate denominator is not smaller than the defined eligible numerator population
- currency values are not mixed without conversion metadata

### Source reconciliation
Reconcile bounded totals/samples against the source system. A successful ETL job is not proof that the values are correct.

## Dashboard contract

Every production dashboard should state audience and decisions supported, source models, metric owner, default time zone and currency, refresh timestamp and expected latency, default filters, drill path, attribution basis where relevant, known exclusions/limitations, and access/privacy class.

## Dashboard design rules

- Put the primary business outcome and key guardrails before diagnostic vanity metrics.
- Do not mix incompatible attribution systems in one total without an explicit reconciliation layer.
- Display freshness or last-updated state when stale data can change decisions.
- Use consistent metric definitions across pages.
- Keep filters visible when they materially change interpretation.
- Prefer diagnostic drill paths over adding more top-level tiles.
- A chart title should state the measure and grain clearly enough to audit it.

## Verification before live

Use exact states: draft to configured to processing to reconciled to verified.

A dashboard can be live but unverified. A pipeline can be processing while stale or wrong. State both runtime state and evidence state.

## Handoff

When the data product is verified:

- $performance-diagnostics may analyze changes
- $marketing-reporting may create stakeholder narratives
- $growth-strategy or channel/commercial owners may make decisions
- $optimization-scaling may use governed marginal evidence

The analytics layer supplies trustworthy data products; it does not inherit those decisions.
