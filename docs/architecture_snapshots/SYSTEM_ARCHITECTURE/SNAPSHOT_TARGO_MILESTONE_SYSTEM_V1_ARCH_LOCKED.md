# SNAPSHOT_TARGO_MILESTONE_SYSTEM_V1_ARCH_LOCKED.md

## STATUS

ARCHITECTURE LOCKED

---

## OBJECTIVE

ایجاد یک لایه دائمی برای ثبت نقاط عطف استراتژیک پروژه (TARGO Milestones) به‌صورت مستقل از چرخه عادی Snapshot ها.

---

## IMPLEMENTED COMPONENTS

### SnapshotDecider

قانون جدید اضافه شد:

- هر Event که event_type آن با `TARGO_` شروع شود
- بدون توجه به سایر شروط Snapshot
- به عنوان `targo_milestone` شناسایی می‌شود

---

### EventBus

در مرحله Snapshot Processing:

- پس از تشخیص `targo_milestone`
- علاوه بر Snapshot عادی
- تابع `save_targo_snapshot()` نیز فراخوانی می‌شود

---

### SnapshotManager

تابع جدید:

`save_targo_snapshot()`

اضافه شد.

وظیفه:

- ایجاد Snapshot اختصاصی برای نقاط عطف TARGO
- ذخیره در مسیر:

`snapshots/targo/`

---

## STORAGE STRUCTURE

snapshots/

├── snapshot_*.json

├── development/

└── targo/

    ├── TARGO_V1_LOCKED.snapshot.json

    └── TARGO_*.snapshot.json

---

## VERIFIED TESTS

### Test 1

TARGO_V1_LOCKED

Result: PASSED

---

### Test 2

TARGO_CORE_TARGET_LOCKED

Result: PASSED

Generated File:

TARGO_CORE_TARGET_LOCKED.snapshot.json

---

## EVENT FLOW

TARGO Event

↓

SnapshotDecider

↓

targo_milestone

↓

EventBus

↓

save_targo_snapshot()

↓

snapshots/targo/

---

## ARCHITECTURAL ROLE

TARGO Snapshots نمایانگر نقاط عطف استراتژیک پروژه هستند و از Snapshot های توسعه‌ای، Runtime Snapshot ها و Snapshot های Governance مستقل نگهداری می‌شوند.

---

## VERSION

TARGO_MILESTONE_SYSTEM_V1

---

## STATE

LOCKED

---

## DATE

2026-06-24

---

## NEXT TARGET

CIVILIZATION LAYER COMPLETION

Digital Twin Civilization Ranking

Population Calibration Expansion

Civilization Intelligence Layer
