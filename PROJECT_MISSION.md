# 2FUN Project Mission Control

## Project
2FUN Ecosystem

## Active Mission — Mission 1
Complete the 2FUNC core and its value, recording, supply, and release-preparation mechanisms.

## Mission Status
ACTIVE

## Mission Boundary

### In Scope
- 2FUNC economic core and exact value calculations.
- Correct integration with the central Universal Value Infrastructure (UVI).
- Transaction and ledger recording through the existing central architecture.
- Data integrity, identity correctness, and idempotency.
- Enforcement of already-approved supply and release rules.
- Relevant tests, documentation, and release-readiness checks.
- Only the minimum necessary integration between governance-approved activity and the 2FUNC value flow.

### Explicitly Out of Scope
- Exchange implementation or behavior changes.
- Blockchain implementation.
- Other ecosystem components unrelated to completing the 2FUNC core.
- Any parallel value engine, ledger, or persistent ecosystem database.

## Immutable Architecture Decisions
- UVI is owned by 2FUN-OS at `platform_core/universal_value/`.
- The central ecosystem database is `2FUN-OS/db/2fun.db`.
- Finance components consume UVI through the established contract; they do not host a parallel value engine.
- The official coin name is exactly `2FUNC`.
- POINT is an activity unit, not a spendable or transferable balance.
- XP is a legacy technical name for the same activity unit as POINT; they are not separate balances.
- Existing approved economic rules must not be changed without explicit user approval.

## Approved Value Units
- 1 Drika = 4 POINT
- 1 SHIR = 250 Drika
- 1 ΣSHIR = 2,500 Drika
- 1 2FUNC = 5,000 Drika
- 1 Drik = 2,000,000 2FUNC

Drik is a valid selectable unit. The spelling "Darik" is not an approved unit name.

## Approved 2FUNC Reference Price
- Exact reference rate: 1 USD = 2,719,050 2FUNC.
- Exact unit USD price: Decimal(1) / Decimal(2719050).
- 0.000000368 USD is display approximation only, not the exact stored rate.
- 1 2FUNC = 10^18 base units.
- Do not round intermediate calculations.
- The reference price is not a market price and does not guarantee USD backing or redemption.

## Approved Supply and Release Constraints
- Total supply: 14,441,417,005,600 base units.
- Preserve the approved supply and release schedule.
- Existing constraints include MIN_ISSUED_PERCENT = 90, MIN_INTERVAL_MONTHS = 6, and 10 emission stages.
- Do not alter issuance or mining rules without explicit approval.

## Mission Completion Requirements
The mission cannot be closed until all applicable requirements below have evidence:

1. Required 2FUNC core components are implemented.
2. Integration uses the central UVI and central ecosystem database.
3. Value calculations, unit conversions, and transaction records comply with approved rules.
4. Idempotency and duplicate-operation handling are demonstrated.
5. Approved supply and release constraints are enforced.
6. Relevant unit and integration tests pass with actual recorded results.
7. Required documentation and release-readiness checks are complete.
8. The user explicitly approves mission closure.

A requirement without evidence must remain unverified. A test must never be reported as passed without its actual result.

## Workflow Rules
- Only one mission may be active at a time.
- Do not start another mission before explicit user approval of this mission's closure.
- Do not reopen a completed stage without new evidence or a demonstrated dependency.
- Do not repeat broad audits or rediscover established facts without a specific reason.
- Before every technical step, state its exact target, reason, and minimal command.
- Inspect actual source code and existing tests before proposing or running tests.
- Protect all pre-existing working-tree changes. Never reset, clean, stash, or overwrite them without explicit approval.
- Do not commit or push before relevant tests pass and the user authorizes it.
- Any proposed change to mission scope, order, or approved economic rules requires explicit user approval.
- Record decisions, commands, results, evidence, and approvals in the workflow history.

## Evidence Discipline
- Distinguish IMPLEMENTED, TESTED, and VERIFIED.
- Record the command and actual output for test evidence.
- Do not infer completion from memory, intention, or an unverified status.
- Preserve unresolved warnings and limitations until they are actually resolved.
