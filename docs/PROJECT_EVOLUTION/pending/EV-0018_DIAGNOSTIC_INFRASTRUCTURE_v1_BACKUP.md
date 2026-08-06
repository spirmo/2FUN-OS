# EV-0018 Diagnostic Infrastructure v1.0

## Status

Planned

## Priority

High Priority

## Reason for Creation

During development of 2FUN-OS, several critical issues caused significant debugging delays:

- New APK update installation failure
- Release APK replacement problems
- Application crash immediately after launch
- Missing crash logs from real user devices
- Difficulty comparing old and new APK builds

Manual investigation consumed several development days.

The purpose of this infrastructure is to create a unified diagnostic system that can quickly identify the source of failures and reduce debugging time.

---

# Objectives

## 1. APK Installation Diagnostic System

Create a diagnostic layer to analyze update installation problems:

- Package name comparison
- Version code comparison
- Version name comparison
- Signing certificate comparison
- Minimum SDK comparison
- Target SDK comparison
- Manifest difference detection
- Native library compatibility check

The system should clearly identify whether installation failure is caused by:

- Signature mismatch
- Version downgrade
- Package conflict
- Manifest conflict
- Device compatibility
- APK corruption

---

# 2. Runtime Crash Reporting System

Create automatic crash reporting infrastructure.

Requirements:

- Capture Flutter exceptions
- Capture Android native crashes
- Store crash information locally
- Generate crash report ID
- Send anonymous diagnostic report to GitHub or backend endpoint

Crash report should include:

- App version
- Build number
- Device information
- Android version
- Stack trace
- Timestamp
- Last user action
- Current screen

---

# 3. User Diagnostic Report System

Add a user-accessible error reporting feature.

When application stops or encounters a critical error:

User should be able to:

- Send error report
- Add description
- Attach diagnostic information
- Submit report

The report should create a structured issue.

---

# 4. CI/CD Build Diagnostic System

Integrate diagnostics into GitHub Actions.

Every build should generate:

- APK metadata report
- Version report
- Signing report
- Dependency report
- Build environment report

Before publishing APK:

Automatic validation should check:

- Correct package ID
- Correct version code
- Correct signing
- Successful installation simulation if possible

---

# Architecture

## Diagnostic Core

Central diagnostic module:

Diagnostic Core | |
|           |            | APK       Runtime      CI/CD Checker   Monitor     Validator | | Report Generator | | GitHub Issue / Backend



---

# Future Integration

This infrastructure should integrate with:

- Event Bus Architecture
- Snapshot Listener Architecture
- Audit System
- Analytics System
- AI Advisory Layer

Diagnostic events should be published through Event Bus.

AI can analyze reports but has no authority to change system state.

---

# Implementation Priority

## Phase 1 - MVP

- Crash log collector
- APK metadata checker
- Version comparison tool
- Manual report generator

## Phase 2

- Automatic GitHub issue creation
- User crash reporting UI
- Build validation pipeline

## Phase 3

- Full diagnostic intelligence system
- Pattern detection
- AI-assisted debugging suggestions

---

# Related Issues

Created from:

- APK update installation failure investigation
- Release signing migration
- 2FUN-OS stability improvements

---

# Current Decision

Approved as planned infrastructure.

Implementation postponed until current MVP stabilization is completed.
