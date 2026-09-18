# Marketing Analytics Evaluation Review

## Purpose

These cases test the boundary between analytics engineering and neighboring marketing decision owners.

## Review standard

A passing response should:

- declare grain, keys, metric semantics, and source authority before implementation
- prevent row multiplication, double counting, silent deduplication, and incompatible attribution aggregation
- require idempotent pipeline behavior and source reconciliation
- preserve time/currency/refund/maturity rules when decision-relevant
- minimize sensitive data
- keep dashboard rendering separate from data verification
- preserve $tracking-measurement, $performance-diagnostics, $marketing-reporting, and domain-owner boundaries
- avoid claiming live data/warehouse/BI mutation without an authorized runtime and verification

Static registration or model grading does not prove a real warehouse or dashboard implementation works.
