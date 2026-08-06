EV-0018 Diagnostic Infrastructure v2.0

Universal Diagnostic & Recovery Infrastructure

2FUN Ecosystem Core Infrastructure

Status: Planned

Priority: Critical Core Infrastructure

Category: Core Runtime Infrastructure

Dependencies: None

Architecture Level: System Core

Target Version: 2FUN Platform v2.x

# 1. Vision

هدف این پروژه ایجاد یک زیرساخت واحد برای تشخیص، تحلیل، ثبت، گزارش و بازیابی خودکار خطاها در کل اکوسیستم 2FUN است.

این زیرساخت فقط برای اپلیکیشن موبایل طراحی نشده است.

بلکه باید بتواند در تمام اجزاء زیر عمل کند:

- 2FUN Super App
- 2FUN GAME
- Governance System
- Knowledge Engine
- Telegram Bot
- Platform API
- Render Services
- Supabase
- Python Services
- Flutter Applications
- Future Desktop Client
- Future Web Client
- Future AI Services
- Future Blockchain Services

# 2. Philosophy

در معماری جدید 2FUN هیچ خطایی نباید "بی‌صدا" از بین برود.

هر خطا باید:

- ثبت شود.
- طبقه‌بندی شود.
- علت‌یابی شود.
- اطلاعات محیط جمع‌آوری شود.
- راهکار احتمالی تولید شود.
- در صورت امکان بازیابی خودکار انجام شود.
- در صورت نیاز برای توسعه‌دهنده ارسال شود.
- در پایگاه دانش ذخیره شود.
- در نسخه‌های آینده از تکرار آن جلوگیری شود.

# 3. Mission

ایجاد یک سیستم مرکزی که بتواند:

- Error Detection
- Error Classification
- Root Cause Analysis
- Recovery
- Reporting
- Telemetry
- Crash Analytics
- Self Diagnosis

را در کل اکوسیستم انجام دهد.

# 4. Goals

## 4.1 کاهش زمان رفع خطا

از چند ساعت

به چند دقیقه

## 4.2 جلوگیری از تکرار خطا

هر خطا یکبار تحلیل می‌شود.

بارهای بعد سیستم خودش آن را می‌شناسد.

## 4.3 کاهش وابستگی به توسعه‌دهنده

سیستم ابتدا خودش تلاش می‌کند مشکل را رفع کند.

## 4.4 ساخت پایگاه دانش خطاها

هر خطا تبدیل به دانش می‌شود.

## 4.5 افزایش پایداری کل اکوسیستم

# 5. Scope

این سیستم باید بتواند خطاهای زیر را مدیریت کند.

## Mobile

- Crash
- Freeze
- UI Failure
- Database Failure
- Permission Failure
- Navigation Failure
- Rendering Failure
- Memory Leak

## Backend

- Python Exception
- Flask Exception
- FastAPI Exception
- SQLite Error
- PostgreSQL Error
- API Failure

## Infrastructure

- Render Failure
- Service Restart
- Deployment Failure
- Environment Variable Error

## Telegram

- Webhook Failure
- Bot Failure
- Polling Failure
- Telegram API Failure

## Knowledge Engine

- Graph Failure
- Taxonomy Failure
- Validation Failure
- Knowledge Injection Failure

## Governance

- Permission Failure
- Snapshot Failure
- Event Bus Failure
- Audit Failure

## Future

- Blockchain Failure
- Wallet Failure
- AI Failure
- Sync Failure

# 6. Architecture Principles

## Rule 1

هیچ Exception نباید بدون ثبت از بین برود.

## Rule 2

هیچ Crash نباید بدون Report باشد.

## Rule 3

هیچ نصب ناموفقی نباید بدون علت باقی بماند.

## Rule 4

هر سرویس باید Health Check داشته باشد.

## Rule 5

هر خطا باید دارای Error ID باشد.

## Rule 6

تمام اجزاء اکوسیستم باید از همین زیرساخت استفاده کنند.

# 7. Core Components

سیستم از چند زیرسیستم مستقل تشکیل می‌شود.

- Diagnostic Core
  - مرکز مدیریت تمام خطاها.

- Error Collector
  - جمع‌آوری اطلاعات خام.

- Crash Analyzer
  - تحلیل Crash.

- Recovery Engine
  - بازیابی خودکار.

- Reporting Engine
  - تولید گزارش.

- Telemetry Engine
  - جمع‌آوری داده‌های اجرایی.

- Knowledge Builder
  - تبدیل خطاها به دانش.

- Event Integration
  - اتصال به Event Bus.

---

**پایان Part 1**

Event Integration Layer

Diagnostic events from all ecosystem components
must be normalized and published into the main Event Bus.

Primary Event Bus:

platform_core/event_bus/event_bus.py

Flow:

Component
    ↓
Diagnostic Collector
    ↓
Diagnostic Event Model
    ↓
Main Event Bus
    ↓
Listeners
    ↓
Audit / Snapshot / Analytics / Recovery


## 7.1 Event Bus Integration Architecture

تمام اجزاء اکوسیستم 2FUN باید خطاها را فقط از طریق زیرساخت تشخیص خطا منتشر کنند.

هیچ ماژولی مجاز نیست مستقیماً گزارش خطا را برای سیستم‌های دیگر ارسال کند.

جریان استاندارد به صورت زیر است:

Application / Service
        ↓
Diagnostic Collector
        ↓
Diagnostic Event
        ↓
Diagnostic Core
        ↓
Main Event Bus
(platform_core/event_bus/event_bus.py)
        ↓
Listeners
        ├── Audit Listener
        ├── Snapshot Listener
        ├── Analytics Listener
        ├── Recovery Listener
        ├── Notification Listener
        └── Future Extensions

تمام Event ها باید قبل از ورود به Event Bus نرمال‌سازی شوند.

هیچ Listener نباید مستقیماً با Application ارتباط داشته باشد.

تمام تصمیمات بعدی از طریق Event Bus انجام می‌شود.

این معماری باعث می‌شود زیرساخت Diagnostic برای کل اکوسیستم قابل استفاده باشد و هیچ وابستگی مستقیمی بین اجزاء ایجاد نشود.


## 7.2 Client Diagnostic Agents

هر جزء اکوسیستم باید دارای یک Diagnostic Agent مستقل باشد.

این Agent مسئول جمع‌آوری اطلاعات خام از همان جزء است و اجازه ندارد مستقیماً تصمیم‌گیری کند.

### Responsibilities

- Capture Startup Failure
- Capture Runtime Exception
- Capture Crash
- Capture Update Failure
- Capture Installation Failure
- Capture Permission Failure
- Capture Database Failure
- Capture Network Failure
- Capture Dependency Failure
- Capture Performance Degradation
- Capture Memory Leak
- Capture Environment Information

### Environment Information

هر گزارش باید حداقل شامل اطلاعات زیر باشد:

- Platform
- Component Name
- Version
- Build Number
- Git Commit
- Runtime
- OS Version
- Device Information
- Database Version
- Event Timestamp

### Supported Agents

Current:

- Flutter Diagnostic Agent
- Python Diagnostic Agent
- Backend Diagnostic Agent

Future:

- Telegram Diagnostic Agent
- Web Diagnostic Agent
- Desktop Diagnostic Agent
- AI Diagnostic Agent
- Blockchain Diagnostic Agent

تمام Agent ها فقط Diagnostic Event تولید می‌کنند.

هیچ Agent اجازه بازیابی مستقیم سیستم را ندارد.

تمام Recovery ها فقط توسط Recovery Engine انجام می‌شود.

## 7.3 Update & Deployment Diagnostics

این زیرساخت باید بتواند تمام فرآیند نصب، بروزرسانی و استقرار را نیز تحلیل کند.

هدف این بخش جلوگیری از صرف زمان زیاد برای یافتن علت نصب نشدن نسخه‌های جدید است.

### Installation Diagnostics

سیستم باید بتواند تشخیص دهد:

- APK Installation Failure
- Package Conflict
- Version Conflict
- Signature Mismatch
- Keystore Mismatch
- ABI Incompatibility
- Permission Conflict
- Android Version Incompatibility
- Missing Dependency
- Migration Failure
- Database Upgrade Failure

### Deployment Diagnostics

سیستم باید بتواند مشکلات زیر را تحلیل کند:

- GitHub Actions Build Failure
- Artifact Corruption
- Upload Failure
- Render Deployment Failure
- Supabase Connection Failure
- Environment Variable Failure

### Diagnostic Report

برای هر خطا اطلاعات زیر ذخیره می‌شود:

- Error ID
- Timestamp
- Component
- Platform
- Package Name
- Installed Version
- New Version
- Build Number
- Git Commit
- Signature Fingerprint
- Device Model
- Android Version
- Database Version
- Error Code
- Stack Trace
- Recovery Suggestion

### Recovery Engine

Recovery Engine باید بتواند در آینده:

- علت خطا را تشخیص دهد.
- راهکار پیشنهادی تولید کند.
- در صورت امکان بازیابی خودکار انجام دهد.
- در غیر اینصورت گزارش کامل برای توسعه‌دهنده تولید کند.

### Knowledge Integration

تمام خطاهای تأیید شده وارد Knowledge Base می‌شوند تا در نسخه‌های بعدی از وقوع مجدد آن‌ها جلوگیری شود.



# 8. System Architecture

2DI بر پایه معماری ماژولار طراحی می‌شود.

```
                +-------------------------+
                |     Applications        |
                |-------------------------|
                | 2FUN-OS                 |
                | 2FUN GAME               |
                | Governance              |
                | Knowledge Engine        |
                | Backend API             |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                | Diagnostic Collector    |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                | Diagnostic Core         |
                +-----------+-------------+
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
 Crash Analyzer      Log Analyzer      Health Monitor
          |                 |                  |
          +-----------------+------------------+
                            |
                            v
                +-------------------------+
                | Root Cause Analyzer     |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                | Recovery Engine         |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                | Reporting Engine        |
                +-----------+-------------+
                            |
                            v
         GitHub / Snapshot / Local DB / Future Cloud
```

---

# 9. Diagnostic Layers

## Layer 1 – Detection

تشخیص وقوع خطا

نمونه‌ها:

- Crash
- Exception
- نصب نشدن APK
- Timeout
- Database Error
- API Error

---

## Layer 2 – Collection

جمع‌آوری اطلاعات

نمونه اطلاعات:

- زمان
- نسخه
- Build Number
- Device
- Android Version
- Stack Trace
- مسیر فایل
- آخرین Event
- آخرین Snapshot
- آخرین عملیات کاربر

---

## Layer 3 – Classification

طبقه‌بندی

مثلاً:

```
Installation

Runtime

Database

Network

Permission

Configuration

Rendering

Memory

Logic

AI

Governance
```

---

## Layer 4 – Analysis

تحلیل علت

نمونه:

```
APK نصب نشد

↓

VersionCode پایین‌تر

↓

Installation Conflict
```

یا

```
Crash

↓

Null Pointer

↓

LanguageService

↓

Missing Translation
```

---

## Layer 5 – Recovery

اگر امکان داشته باشد:

- Restart
- Rollback
- Retry
- Cache Reset
- Safe Mode
- پیشنهاد نسخه سالم

---

## Layer 6 – Reporting

گزارش تولید می‌شود.

---

# 10. Error Categories

## Installation Errors

- APK نصب نشد
- Signature Conflict
- Version Conflict
- Split APK Error
- Manifest Conflict

---

## Runtime Errors

- Crash
- Freeze
- Infinite Loop

---

## Database Errors

- SQLite Locked
- Missing Table
- Corrupted DB

---

## Network Errors

- Timeout
- DNS
- SSL
- Connection Refused

---

## API Errors

- 400
- 401
- 403
- 404
- 500

---

## Permission Errors

- Camera
- Storage
- Notification
- Internet

---

## Rendering Errors

- Widget Tree
- Layout
- Overflow
- Flutter Exception

---

## Configuration Errors

- Missing ENV
- Wrong Config
- Wrong Endpoint

---

## Governance Errors

- Permission
- Role
- EventBus
- Snapshot

---

## AI Errors

- Model Failure
- Timeout
- Invalid Response

---

# 11. Installation Diagnostic

یکی از مهم‌ترین قابلیت‌ها.

سیستم باید بتواند علت نصب نشدن نسخه جدید را تشخیص دهد.

مثلاً:

```
VersionCode

↓

Signature

↓

Package Name

↓

Manifest

↓

Native Library

↓

SDK Conflict

↓

Split APK

↓

Storage

↓

Permission
```

بدون اینکه توسعه‌دهنده مجبور شود چند روز دنبال علت بگردد.

---

# 12. Crash Diagnostic

در زمان Crash:

```
Catch Exception

↓

Stack Trace

↓

Memory State

↓

Current Page

↓

Current Event

↓

Current User

↓

Current Language

↓

Database Status

↓

Network Status
```

همه ثبت می‌شوند.

---

# 13. Diagnostic Report

نمونه:

```
Report ID

Time

Platform

Application

Module

Severity

Category

Root Cause

Suggested Fix

Recovery Result
```

---

# 14. Error Knowledge Base

هر خطا تبدیل به دانش می‌شود.

بعدها:

```
اگر همان خطا تکرار شود

↓

سیستم

↓

قبلاً آن را می‌شناسد

↓

راه‌حل آماده ارائه می‌کند.
```

---


# 15. 2DI SDK

تمام اجزای اکوسیستم باید فقط از طریق 2DI SDK با زیرساخت تشخیص خطا ارتباط برقرار کنند.

این SDK یک رابط استاندارد برای ثبت، تحلیل و گزارش خطا فراهم می‌کند.

---

## Responsibilities

- Error Reporting
- Crash Reporting
- Performance Monitoring
- Installation Diagnostics
- Health Reporting
- Recovery Request
- Snapshot Request

---

## Supported Platforms

- Flutter
- Python
- Flask
- FastAPI
- Telegram Bot
- Web Applications
- Desktop Applications
- Future Services

---

# 16. Event Bus Integration

2DI باید مستقیماً با Event Bus اکوسیستم یکپارچه باشد.

هر Event مهم باید بتواند در صورت وقوع خطا اطلاعات لازم را به Diagnostic Core ارسال کند.

نمونه:

```
User Login

↓

Permission Check

↓

Crash

↓

Event Bus

↓

Diagnostic Core
```

---

# 17. Snapshot Integration

در زمان وقوع خطا، سیستم باید آخرین Snapshot معتبر را ثبت کند.

اطلاعات نمونه:

- آخرین Event
- آخرین Transaction
- آخرین صفحه
- آخرین Database State
- آخرین User State

---

# 18. Health Monitoring

تمام اجزای اکوسیستم باید وضعیت سلامت خود را به 2DI گزارش کنند.

Health شامل:

- Alive
- Warning
- Critical
- Offline

---

نمونه:

```
Knowledge Engine

Status = Warning

↓

Diagnostic Core

↓

Reason Analysis
```

---

# 19. Self-Healing

اگر امکان بازیابی خودکار وجود داشته باشد، سیستم باید بدون دخالت کاربر اقدام کند.

نمونه عملیات:

- Restart Service
- Retry API
- Reset Cache
- Restore Snapshot
- Rollback Version
- Reload Configuration

---

# 20. Safe Mode

اگر سیستم تشخیص دهد که اجرای عادی امکان‌پذیر نیست، باید وارد Safe Mode شود.

در Safe Mode:

- فقط سرویس‌های حیاتی اجرا می‌شوند.
- گزارش خطا تولید می‌شود.
- امکان ارسال گزارش برای توسعه‌دهنده وجود دارد.
- از Crash Loop جلوگیری می‌شود.

---

# 21. GitHub Reporting

2DI باید امکان تولید گزارش استاندارد برای GitHub را داشته باشد.

گزارش شامل:

- Error ID
- Timestamp
- Build Version
- VersionCode
- Platform
- Module
- Stack Trace
- Device Info
- Root Cause
- Suggested Fix

---

# 22. Local Diagnostic Database

تمام گزارش‌ها ابتدا در پایگاه داده محلی ذخیره می‌شوند.

جدول نمونه:

```
diagnostic_reports

id

timestamp

severity

category

module

message

stacktrace

status

recovery_result
```

---

# 23. Diagnostic Knowledge Base

هر خطای تحلیل‌شده تبدیل به دانش می‌شود.

```
Error

↓

Analysis

↓

Root Cause

↓

Verified Solution

↓

Knowledge Base
```

در آینده، موتور AI از همین پایگاه برای پیشنهاد راه‌حل استفاده خواهد کرد.

---

# 24. Diagnostic API

تمام سرویس‌ها فقط از طریق API استاندارد با 2DI ارتباط برقرار می‌کنند.

نمونه:

```
reportError()

reportCrash()

requestRecovery()

healthCheck()

createSnapshot()

sendTelemetry()
```

---

# 25. Architecture Rules

Rule 1

تمام پروژه‌های 2FUN باید از 2DI استفاده کنند.

---

Rule 2

هیچ Exception نباید بدون ثبت باقی بماند.

---

Rule 3

هیچ Crash نباید بدون Report خاتمه یابد.

---

Rule 4

تمام سرویس‌ها باید Health Check داشته باشند.

---

Rule 5

هر خطا باید Error ID یکتا داشته باشد.

---

Rule 6

هیچ توسعه‌دهنده‌ای نباید برای یافتن علت خطا مجبور به بررسی دستی طولانی شود.

---

Rule 7

هر خطای مهم باید به دانش دائمی تبدیل شود.

---

Rule 8

2DI بخشی از Core Architecture است و حذف یا دور زدن آن مجاز نیست.

# 26. Implementation Roadmap

پیاده‌سازی 2DI به صورت مرحله‌ای انجام خواهد شد تا بدون ایجاد اختلال در توسعه فعلی اکوسیستم، به تدریج تمام اجزا را پوشش دهد.

---

# Phase 1 — Basic Diagnostic Layer

## هدف

ایجاد اولین لایه ثبت خطا.

## شامل:

- Global Error Handler
- Exception Capture
- Local Log Storage
- Error ID Generator
- Basic Diagnostic Report

## خروجی:

هر خطا دارای شناسه، زمان و اطلاعات پایه خواهد بود.

---

# Phase 2 — Mobile Diagnostic System

## هدف

پوشش کامل 2FUN Super App.

## شامل:

- Flutter Error Handler
- Flutter Crash Reporter
- Build Information Collector
- Device Information Collector
- APK Installation Diagnostic

## موارد تحت پوشش:

- Crash هنگام اجرا
- نصب نشدن APK
- مشکل Upgrade
- مشکل Permission
- مشکل UI

---

# Phase 3 — Ecosystem Integration

## هدف

اتصال تمام اجزای 2FUN.

## اتصال:

- Event Bus
- Snapshot System
- Audit System
- Governance System
- Knowledge Engine

---

# Phase 4 — Central Diagnostic Dashboard

## هدف

ایجاد مرکز کنترل خطاها.

قابلیت‌ها:

- مشاهده خطاهای فعال
- مشاهده تاریخچه خطاها
- وضعیت سلامت سرویس‌ها
- تحلیل روند خطاها
- اولویت‌بندی مشکلات

---

# Phase 5 — Automated Recovery

## هدف

کاهش نیاز به دخالت انسانی.

قابلیت‌ها:

- Auto Retry
- Auto Restart
- Safe Recovery
- Snapshot Restore
- Version Rollback

---

# Phase 6 — AI Diagnostic Assistant

## هدف

استفاده از AI به عنوان دستیار تحلیل.

AI Authority:

```
Advisor Only

Authority = NONE
```

وظایف:

- تحلیل گزارش‌ها
- پیشنهاد علت احتمالی
- پیشنهاد راه‌حل
- یافتن الگوهای تکراری

---

# Phase 7 — Predictive Diagnostics

## هدف

تشخیص مشکل قبل از وقوع.

نمونه:

```
Performance Degradation

↓

Pattern Detection

↓

Warning

↓

Preventive Action
```

---

# 27. Future Extensions

## Distributed Diagnostics

پشتیبانی از معماری توزیع‌شده.

---

## Cloud Diagnostic Service

انتقال تحلیل‌ها به زیرساخت ابری.

---

## Advanced Analytics

تحلیل:

- Frequency
- Impact
- Reliability
- Performance

---

## Automated Testing Integration

اتصال با:

- CI/CD
- GitHub Actions
- Automated Testing

---

## Release Quality Gate

قبل از انتشار نسخه جدید:

```
Build

↓

Test

↓

Diagnostic Check

↓

Release Approval
```

---

# 28. Relationship With Other EV Projects

## EV-0017 Event Bus Snapshot Listener Architecture

ارتباط:

Event Bus اطلاعات رخدادها را فراهم می‌کند.

2DI از این اطلاعات برای تحلیل خطا استفاده می‌کند.

---

## EV-0014 Backup & Disaster Recovery Strategy

ارتباط:

2DI در زمان Recovery از Snapshot و Backup استفاده می‌کند.

---

## EV-0015 KPS Source Traceability Standard

ارتباط:

گزارش‌های خطا و تغییرات باید قابل ردیابی باشند.

---

## EV-0016 TANDIL Language Engine

ارتباط:

خطاهای زبان و ترجمه نیز باید توسط 2DI قابل تشخیص باشند.

---

# 29. Success Criteria

EV-0018 زمانی موفق محسوب می‌شود که:

✓ هر خطا دارای شناسه باشد.

✓ هیچ Crash بدون گزارش باقی نماند.

✓ علت خطا قابل تحلیل باشد.

✓ نصب نسخه جدید قابل تشخیص باشد.

✓ وضعیت سلامت اجزا قابل مشاهده باشد.

✓ Recovery خودکار برای خطاهای قابل حل انجام شود.

✓ خطاهای گذشته تبدیل به دانش شوند.

✓ توسعه‌دهنده زمان خود را صرف پیدا کردن دستی مشکل نکند.

---

# 30. Ultimate Goal

هدف نهایی 2DI ایجاد یک اکوسیستم خودآگاه در زمینه سلامت نرم‌افزار است.

در آینده:

```
Failure

↓

Detection

↓

Analysis

↓

Knowledge

↓

Recovery

↓

Prevention
```

سیستم نه تنها خطا را گزارش می‌کند، بلکه از وقوع دوباره آن جلوگیری خواهد کرد.

---

# Final Architecture Statement

2DI (2FUN Diagnostic Infrastructure)

یک زیرساخت مرکزی، دائمی و اجباری برای کل اکوسیستم 2FUN است که وظیفه آن:

تشخیص،
تحلیل،
گزارش،
بازیابی،
و تبدیل خطا به دانش

در تمام نسل‌های آینده 2FUN خواهد بود.

---

**Document Status: EV-0018 v2.0**

**Category: Critical Core Infrastructure**

**Priority: Critical**

**Architecture Level: Ecosystem Core**



## Future Architectural Improvements

### Diagnostic Module Dependency Injection Architecture

در نسخه‌های آینده، DiagnosticService نباید وابستگی‌های داخلی خود را مستقیماً ایجاد کند.

هدف:
ایجاد یک معماری قابل توسعه که ماژول‌های زیر بتوانند به صورت مستقل تزریق و جایگزین شوند:

- Diagnostic Logger
- Diagnostic Storage
- Diagnostic Reporter
- Recovery Engine

این طراحی باعث می‌شود زیرساخت Diagnostic در تمام اجزای اکوسیستم 2FUN بدون تغییرات شکننده قابل استفاده و توسعه باشد.

Future Direction:

DiagnosticService
        |
        +--> Logger Module
        |
        +--> Storage Module
        |
        +--> Reporter Module
        |
        +--> Recovery Module




#قسمت انگلیسی

### Dependency Injection Support

Future versions should support injected diagnostic modules instead of creating internal dependencies directly.

Target modules:
- Logger
- Storage
- Reporter
- Recovery Engine

This prevents architectural coupling and enables scalable diagnostic infrastructure across the entire 2FUN ecosystem.





## 9. Client Diagnostic Agents

Every client application must include a lightweight Diagnostic Agent.

Responsibilities:

- Capture startup failures
- Capture crash reports
- Capture installation/update failures
- Capture permission errors
- Capture database initialization errors
- Capture environment information
- Send diagnostic events to the ecosystem Diagnostic Core


## Update & Deployment Diagnostics

The system must diagnose:

- APK installation failure
- Signature mismatch
- Version conflict
- Package conflict
- Migration failure
- Dependency failure
- Build artifact mismatch

The report must include:

- Old version information
- New version information
- Package name
- Signature fingerprint
- Install error code
- Device information
- Build metadata





Future Extension:

DiagnosticService must support pluggable modules:

- Logger Module
- Storage Module
- Reporter Module
- Recovery Module
- Event Publisher Module
