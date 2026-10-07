# 2FUN / توفان
# On-Chain Value Units Architecture
## Architecture Snapshot v1.0

**Status:** ARCHITECTURE DECISION
**Date:** 2026-10-06
**Canonical Source:** 2FUN-OS
**Principle:** Archive, Never Delete

---

# 1. PURPOSE
# هدف

این Snapshot معماری رسمی «واحدهای ارزش درون‌زنجیره‌ای 2FUN»
را ثبت می‌کند.

هدف این معماری:

1. ایجاد یک واحد پایه برای ثبت مقدار در دفترکل.
2. امکان جابه‌جایی واحدهای ارزش درون زنجیره.
3. امکان استفاده و معامله واحدهای مختلف ارزش.
4. جلوگیری از ایجاد Token Ledger مستقل برای هر واحد.
5. حفظ 2FUNC به‌عنوان تنها Native Coin بلاکچین 2FUN.
6. حفظ POINT به‌عنوان Activity / Score Unit و خارج از Value Ledger.

---

# 2. CORE ARCHITECTURE
# معماری اصلی

اصل بنیادی:

    Drika (دریکا)
    = Base Value Ledger Unit
    = واحد پایه ثبت ارزش در دفترکل

تمام مقادیر اقتصادی در Value Ledger در نهایت
قابلیت بیان برحسب Drika را دارند.

اصل:

    ONE VALUE LEDGER
    MULTIPLE DENOMINATIONS

یعنی:

    یک دفترکل ارزش
    چند واحد اسمی ارزش

---

# 3. VALUE HIERARCHY
# سلسله‌مراتب واحدها

ساختار مفهومی:

    POINT
       |
       v
    Drika
       |
       v
    SHIR
       |
       v
    ΣSHIR
       |
       v
    2FUNC
       |
       v
    Drik

نکته:

Drik (دریک) «واحد ارزش مرجع کلان» است
و Token مستقل محسوب نمی‌شود.

رابطه Drik و 2FUNC یک رابطه ارزش/محاسباتی است.

---

# 4. FORMAL VALUE RATIOS
# نسبت‌های رسمی ارزش

نسبت‌های تثبیت‌شده:

    4 POINT = 1 Drika

    1,000 POINT = 1 SHIR

    10 SHIR = 1 ΣSHIR

    2 ΣSHIR = 1 2FUNC

    2,000,000,000 2FUNC = 1 Drik

نتایج:

    1 Drika = 4 POINT

    1 Drik = 10,000,000,000,000 Drika

    1 Drik = 40,000,000,000,000 POINT

    1 Drik = 2,000,000,000 2FUNC

---

# 5. LEDGER PRINCIPLE
# اصل دفترکل

Value Ledger مقدار پایه را برحسب Drika
به‌صورت دقیق و قطعی حسابداری می‌کند.

واحدهای بالاتر از روی مقدار پایه محاسبه
و برای نمایش، انتقال و بازار استفاده می‌شوند.

مثال مفهومی:

    Base Ledger Amount:
        1,000,000 Drika

    Display / Trading Denomination:
        X SHIR

SHIR به معنی ایجاد یک Token Ledger مستقل نیست.

---

# 6. TRANSFERABILITY
# قابلیت جابه‌جایی

واحدهای لایه ارزش می‌توانند قابلیت انتقال
درون‌زنجیره‌ای داشته باشند:

    Drika
    SHIR
    ΣSHIR
    2FUNC

انتقال آن‌ها بر پایه Value Ledger مشترک انجام می‌شود.

قابل انتقال بودن به معنی ایجاد Token Contract
مستقل نیست.

---

# 7. MARKETABILITY
# قابلیت معامله

Transferability و Marketability دو مفهوم جدا هستند.

Exchange می‌تواند برای واحدهای مختلف
Market Pair ایجاد کند.

نمونه:

    SHIR / 2FUNC
    ΣSHIR / 2FUNC
    Drika / 2FUNC
    Drik / 2FUNC

این Market Pairها به معنی ایجاد چند Token
مستقل نیستند.

---

# 8. 2FUNC NATIVE COIN RULE
# قانون کوین بومی 2FUNC

2FUNC تنها Native Coin بلاکچین 2FUN است.

نقش‌های اصلی:

    - Native Coin
    - Gas Asset
    - Network Staking Asset
    - Settlement Asset
    - Exchange Asset
    - DeFi Utility Asset

واحدهای:

    Drika
    Drik
    SHIR
    ΣSHIR

Native Coin مستقل نیستند.

---

# 9. POINT SEPARATION RULE
# قانون جداسازی POINT

POINT یک Token و Value Asset نیست.

POINT:

    - Activity Unit
    - Score Unit
    - Calculation Input

است.

مسیر:

    User Activity
         |
         v
       POINT
         |
         v
    Calculation Engine
         |
         v
       Drika
         |
         +----> SHIR
         |
         +----> ΣSHIR
         |
         +----> 2FUNC

POINT خارج از Value Ledger باقی می‌ماند.

---

# 10. SINGLE VALUE RESERVOIR
# اصل مخزن واحد ارزش

معماری اقتصادی از ایجاد چند Economic Reservoir
مستقل جلوگیری می‌کند.

اصل:

    ONE VALUE RESERVOIR
    MULTIPLE DENOMINATIONS

بنابراین:

    انتقال
    تبدیل
    حسابداری
    تسویه
    بازارسازی

بر پایه یک لایه ارزش مشترک انجام می‌شوند.

---

# 11. EXAMPLE
# مثال مفهومی

فرض:

    Base Amount = 1,000,000 Drika

این مقدار می‌تواند در Exchange با یک
Denomination مشخص نمایش داده شود.

مثلاً:

    Display Unit = SHIR

در Trade Record می‌توان ثبت کرد:

    Display Unit:
        SHIR

    Base Unit:
        Drika

    Base Amount:
        1,000,000 Drika

نام SHIR در این رکورد به معنی ایجاد
Token Ledger مستقل برای SHIR نیست.

---

# 12. ARCHITECTURAL BENEFITS
# مزایای معماری

این مدل:

1. چند Token Ledger مستقل ایجاد نمی‌کند.
2. نقدشوندگی را به یک واحد محدود نمی‌کند.
3. امکان انتقال واحدهای ارزش مختلف را فراهم می‌کند.
4. امکان ایجاد بازارهای مختلف را فراهم می‌کند.
5. حسابداری را بر پایه یک واحد مشترک انجام می‌دهد.
6. 2FUNC را مرکز اقتصاد بلاکچین حفظ می‌کند.
7. با Calculation Engine موجود سازگار است.
8. از ایجاد Economic Engine موازی جلوگیری می‌کند.
9. توسعه Wallet و Exchange چندواحدی را ساده‌تر می‌کند.
10. از ایجاد Token Contractهای غیرضروری جلوگیری می‌کند.

---

# 13. ARCHITECTURAL CONSTRAINTS
# محدودیت‌های معماری

قواعد LOCKED:

    Drika
        != Native Coin

    Drik
        != Native Coin

    SHIR
        != Native Coin

    ΣSHIR
        != Native Coin

    2FUNC
        = Native Coin

قاعده دوم:

    POINT
        != Value Asset

قاعده سوم:

    هیچ واحد ارزش غیر از 2FUNC
    بدون تصمیم معماری مستقل نباید
    به Token مستقل تبدیل شود.

قاعده چهارم:

    Value Ledger
        باید Drika را به‌عنوان
        Base Accounting Unit حفظ کند.

---

# 14. RELATION TO EXISTING CALCULATION ENGINE
# رابطه با موتور محاسبات موجود

این Snapshot یک Economic Engine جدید ایجاد نمی‌کند.

Calculation Engine / Universal Value Engine موجود
مرجع محاسباتی باقی می‌ماند.

این معماری فقط نحوه اتصال خروجی محاسبات
به On-Chain Value Ledger را تعریف می‌کند.

مسیر:

    Activity
       |
       v
    POINT
       |
       v
    Universal Value / Calculation Engine
       |
       v
    Drika
       |
       v
    On-Chain Value Ledger
       |
       +---- SHIR
       +---- ΣSHIR
       +---- 2FUNC
       +---- Drik Reference

---

# 15. BLOCKCHAIN PRINCIPLE
# اصل بلاکچین

بلاکچین 2FUN از ابتدا با این فرض طراحی می‌شود:

    2FUNC
        = Native Coin

و:

    Drika
        = Base Value Accounting Unit

Blockchain Runtime باید قابلیت پشتیبانی از:

    - Drika-based accounting
    - 2FUNC native balance
    - conversion rules
    - transfer rules
    - settlement rules
    - fee rules
    - exchange integration

را داشته باشد.

---

# 16. FINAL ARCHITECTURE STATEMENT
# بیانیه نهایی معماری

2FUN از یک Value Ledger مشترک استفاده می‌کند
که Drika را به‌عنوان Base Value Unit نگهداری می‌کند.

SHIR، ΣSHIR و 2FUNC واحدهای ارزش/اسمی قابل استفاده
در اکوسیستم هستند که مقدار آن‌ها بر پایه همین لایه
قابل محاسبه و تسویه است.

2FUNC تنها Native Coin بلاکچین 2FUN است.

POINT خارج از Value Ledger قرار دارد و به‌عنوان
Activity / Score Unit عمل می‌کند.

ساختار نهایی:

    POINT
       |
       v
    Calculation Engine
       |
       v
    Drika
       |
       v
    Shared Value Ledger
       |
       +---- SHIR
       |
       +---- ΣSHIR
       |
       +---- 2FUNC
       |
       +---- Drik Reference

اصل بنیادی:

    ONE VALUE LEDGER
    MULTIPLE DENOMINATIONS
    ONE NATIVE COIN

یعنی:

    یک دفترکل ارزش
    چند واحد اسمی
    یک کوین بومی

---

# 17. CANONICAL SOURCE
# مرجع رسمی

این سند در:

    ~/2FUN-OS/docs/architecture_snapshots/

به‌عنوان Canonical Source معماری واحدهای ارزش
درون‌زنجیره‌ای 2FUN نگهداری می‌شود.

نسخه‌های جداگانه این قانون در سایر Repositoryها
به‌عنوان Source of Truth ایجاد نمی‌شوند.

در صورت تغییر معماری:

    Snapshot جدید ایجاد شود.

نسخه قبلی حذف نشود.

اصل:

    Archive, Never Delete

---

# 18. STATUS

    ARCHITECTURE DECISION
    SNAPSHOT v1.0
    CANONICAL
    2FUN-OS

این Snapshot مبنای طراحی مراحل بعدی:

    - Blockchain Runtime
    - Ledger
    - Wallet
    - Exchange
    - Settlement
    - Gas / Fee
    - Staking
    - Smart Contracts
    - Economic Specification

خواهد بود.

