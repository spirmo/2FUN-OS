# 2FUN / توفان
# Component Ownership Registry
## Version 1.0 (Current Architecture Inventory)

---

# 1. Platform Core (هسته پلتفرم)

| Component | Path | Ownership | Visibility |
|-----------|------|-----------|------------|
| Governance Core | TANDIL_GOVERNANCE/core_engine | Private Core | Internal |
| Event Bus | TANDIL_GOVERNANCE/core_engine/event_bus | Private Infrastructure | Internal |
| Snapshot Manager | TANDIL_GOVERNANCE/core_engine/snapshot_manager.py | Private Infrastructure | Internal |
| Snapshot Engine | core_engine/snapshot | Private Infrastructure | Internal |
| Runtime Layer | core_engine/runtime | Private Infrastructure | Internal |
| Founder System | core_engine/founder | Private Core | Internal |

---

# 2. Governance Engines

| Engine | Ownership | Visibility |
|---------|-----------|------------|
| Governance Engine | Private | Internal |
| Rule Engine | Private | Internal |
| Policy Engine | Private | Internal |
| Policy Registry | Private | Internal |
| Policy Draft Engine | Private | Internal |
| Approval Layer | Private | Internal |
| Enforcement Engine | Private | Internal |
| Conflict Engine | Private | Internal |
| Conflict Resolver Advanced | Private | Internal |
| Audit Engine | Private | Internal |
| Reporting Engine | Private | Internal |
| Simulation Engine | Private | Internal |
| Adaptive Engine | Private | Internal |
| Router Engine | Private | Internal |
| Arbitration Engine | Private | Internal |

---

# 3. Identity & Behavior

| Engine | Ownership | Visibility |
|---------|-----------|------------|
| Identity Engine | Shared Platform | Shared |
| Behavioral Engine | Shared Platform | Shared |
| Memory Engine | Shared Platform | Shared |
| Life Memory | Shared Platform | Shared |

---

# 4. Knowledge System

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| Knowledge Engine | Shared Platform | Shared |
| Knowledge Nodes | Shared Platform | Shared |
| Knowledge Graph | Shared Platform | Shared |
| Question Templates | Shared Platform | Shared |

---

# 5. Civilization System

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| Colony Engine | Shared Platform | Shared |
| Strategic Engine | Shared Platform | Shared |
| Civilization Intelligence | Shared Platform | Shared |

---

# 6. Economy System

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| XP System | Shared Platform | Shared |
| XP Log | Shared Platform | Shared |
| Token System | Shared Platform | Shared |
| SHIR Economy | Shared Platform | Shared |
| Economy Architecture | Shared Platform | Shared |

---

# 7. Ranking System

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| Rank Engine | Shared Platform | Shared |
| Reputation Layer | Shared Platform | Shared |

---

# 8. Database Layer

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| SQLite Runtime Database | Private Infrastructure | Internal |
| Database Models | Private Infrastructure | Internal |
| Migration Engine | Private Infrastructure | Internal |
| Database Backup System | Private Infrastructure | Internal |

---

# 9. Event Architecture

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| EventBus | Private Infrastructure | Internal |
| Event Validator | Private Infrastructure | Internal |
| Event Logger | Private Infrastructure | Internal |
| Async Queue | Private Infrastructure | Internal |
| Risk Analyzer | Private Infrastructure | Internal |
| Governance Score | Private Infrastructure | Internal |
| Event Rules | Private Infrastructure | Internal |

---

# 10. Runtime Assets

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| PROJECT_STATE | Private Infrastructure | Internal |
| Runtime Snapshots | Private Infrastructure | Internal |
| Development Snapshots | Private Infrastructure | Internal |
| TARGO Snapshots | Private Infrastructure | Internal |
| Backup Archives | Private Infrastructure | Internal |

---

# 11. Public Platform APIs

| Component | Ownership | Visibility |
|-----------|-----------|------------|
| Identity Service | Shared Platform | Public API |
| Knowledge Service | Shared Platform | Public API |
| Colony Service | Shared Platform | Public API |
| Economy Service | Shared Platform | Public API |
| Governance Service | Shared Platform | Public API (Rule Controlled) |

---

# 12. Private Internal Infrastructure

این بخش‌ها فقط توسط هسته سیستم استفاده می‌شوند و هیچ ماژولی نباید مستقیماً به آن‌ها وابسته شود:

- EventBus Core
- Snapshot Manager
- Runtime Context
- Rule Engine
- Founder Engine
- Audit Engine
- Policy Registry
- Database Runtime
- Backup System
- Async Queue
- Conflict Resolution Core

---

# 13. Shared Engines

این موتورها برای استفاده سایر ماژول‌ها طراحی شده‌اند:

- Identity
- Knowledge
- Colony
- Economy
- Reputation
- Ranking
- Memory
- Behavioral Engine

---

# 14. Current Ownership Summary

| Category | Count |
|----------|------:|
| Private Core Engines | 14 |
| Private Infrastructure Components | 16 |
| Shared Platform Engines | 8 |
| Public Service Interfaces | 5 |

---

## Status

**Document Status:** Draft v1.0

**Scope:** Current discovered architecture from 2FUN GAME + TANDIL Governance

**Next Phase:** Complete registry by adding 2FUN-OS (Flutter), Platform APIs, AI Layer, Wallet, Marketplace, Super App modules.
