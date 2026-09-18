# Real-World Validation

This layer records evidence that a governed Marketing OS decision or implementation was exercised against real work.

It does not manufacture case-study proof. Real-world validation is an evidence process, not a one-time repository checkbox.

## Evidence classes

Use one of:

- synthetic: fictional data; useful for behavior and tooling checks only
- anonymized-real: based on real work with identifying/confidential information removed; internal provenance must remain traceable
- verified-public: real business/result that can be published with appropriate permission and supporting evidence

Only verified-public may be presented publicly as a case study with achieved results.

## Registry

registry.json is the machine-readable index.

A validation record may be registered only when it includes:

- stable id
- capability/owning skill
- evidence class
- business context at an appropriate privacy level
- decision/request
- evidence sources or provenance references
- implementation state
- outcome window/maturity rule
- observed outcome
- limitations/contradictions
- permission/publication state
- review state

Do not put credentials, PII, client-confidential exports, or private account identifiers in the repository.

## What counts as stronger validation

Strength increases when the record has:

1. real source evidence
2. traceable definitions and time window
3. verified implementation state
4. mature primary business outcome and guardrails
5. counterfactual/causal design where the claim requires causality
6. negative/null outcomes preserved
7. independent or human review
8. replication in another scoped context before promoting a pattern

One successful client result does not make a universal rule.

## Real-world validation workflow

permission + privacy review -> bounded evidence packet -> owning skill decision -> authorized implementation -> implementation verification -> maturity window -> outcome collection -> validity/measurement review -> scoped learning record -> optional public case study only if publishable

## Public repository rule

The public repository should normally store:

- anonymized decision structure
- metric definitions/formulas
- redacted or aggregated evidence
- validation result and limitations
- provenance pointer that does not reveal private data

Raw client exports and account screenshots should remain in the authorized private system unless explicit publication permission exists.

## Validation states

Use:

registered -> evidence-complete -> implementation-verified -> outcome-mature -> reviewed -> publishable

A record can stop at any earlier state. Do not skip a state in prose merely because later data exists.

## Current evidence status

The repository can be structurally complete while the real-world evidence base continues to grow. The registry must never claim a real-world count or success rate that the registered evidence does not support.

Run:

python3 scripts/validate-system-boundaries.py

This validates registry truth-state rules; it does not create evidence.
