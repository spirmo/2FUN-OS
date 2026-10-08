# 2FUN / توفان
# 2FUNC Mining & Staking Model — Architecture Snapshot v1.0

**Status:** Architecture Definition — Core Model Locked, Parameter Details Unlocked
**Asset:** 2FUNC
**Network:** 2FUN Blockchain
**Canonical Value Units:** Drika / Drik / SHIR / ΣSHIR / 2FUNC

---

## 1. Purpose

این Snapshot مدل پایهٔ استخراج (Mining) و استیکینگ (Staking) کوین بومی 2FUNC را تعریف می‌کند.

این سند مرجع معماری برای طراحی بعدی 2FUNC، UVI، Value Ledger، Exchange و Blockchain خواهد بود.

جزئیات پارامتریک که هنوز دربارهٔ آن‌ها تصمیم نهایی گرفته نشده‌اند، عمداً در این Snapshot قفل نشده‌اند.

---

## 2. Core Economic Principle

**ارزش اقتصادی یک فعالیت باید مستقل از تغییر ارزش بازار 2FUNC متعادل بماند.**

به همین دلیل مقدار POINT حاصل از یک فعالیت می‌تواند متناسب با ارزش مرجع 2FUNC تغییر کند، در حالی که ارزش هدف خود فعالیت حفظ می‌شود.

### رابطهٔ معکوس

- افزایش ارزش 2FUNC → POINT کمتر برای همان فعالیت
- کاهش ارزش 2FUNC → POINT بیشتر برای همان فعالیت

بنابراین تغییر قیمت 2FUNC نباید باعث شود همان فعالیت صرفاً به دلیل زمان ورود کاربر، ارزش اقتصادی نامتعارفی ایجاد کند.

---

## 3. POINT — Mining Gateway

**POINT (امتیاز فعالیت)** تنها ورودی مستقیم فرآیند Mining است.

هیچ فعالیتی بدون ایجاد POINT معتبر نباید مستقیماً 2FUNC جدید ایجاد کند.

### مسیر پایه

Activity → POINT → UVI → Mining Policy → 2FUNC

POINT معیار سنجش فعالیت است، نه خود کوین و نه یک دارایی مستقل قابل‌معامله.

---

## 4. UVI — Computation Engine

**UVI (موتور محاسبه ارزش)** مسئول محاسبهٔ ارزش حاصل از POINT و آماده‌سازی آن برای سیاست استخراج است.

UVI خودِ سیاست انتشار کوین نیست و نباید با Mining Policy یا Staking Policy ادغام شود.

### مسیر محاسباتی

POINT → UVI Value Calculation → Mining Policy → 2FUNC Emission

---

## 5. Mining و Staking مستقل هستند

### Mining — استخراج

Mining پاداشی است که بر اساس فعالیت معتبر و POINT واردشده به سیستم محاسبه می‌شود.

Activity → POINT → UVI → Mining → 2FUNC

### Network Staking — استیکینگ شبکه

Staking فرآیند قفل/اختصاص 2FUNC موجود برای امنیت و مشارکت شبکه است.

2FUNC → Stake → Network Security / Validator → Staking Reward

**اصل معماری:**

Mining Pool ≠ Staking Pool

افزایش مقدار Staking نباید به‌طور خودکار باعث ایجاد نامحدود 2FUNC جدید شود.

---

## 6. Emission Cap — سقف انتشار

**Emission Cap فقط سقف مقدار 2FUNC جدید قابل ایجاد است؛ سقف مقدار 2FUNC قابل سرمایه‌گذاری یا Staking نیست.**

بنابراین وجود سقف استخراج به معنی محدود شدن سرمایه‌گذاری Stakerها نیست.

برای مثال، اگر مقدار Mining قابل ایجاد در یک مرحله محدود باشد، همچنان می‌تواند مقدار بسیار بیشتری 2FUNC توسط دارندگان در Staking قرار گیرد؛ مشروط به قواعد امنیتی و عملیاتی شبکه.

---

## 7. Total Supply

حداکثر عرضهٔ کل 2FUNC:

**14,441,417,005,600 2FUNC**

هیچ فرآیند Mining یا Staking نباید باعث عبور مجموع عرضه از این سقف شود.

---

## 8. Value-Unit Relationship

رابطه‌های ارزش پایهٔ فعلی:

- 4 POINT = 1 Drika
- 1,000 POINT = 1 SHIR
- 10 SHIR = 1 ΣSHIR
- 2 ΣSHIR = 1 2FUNC
- 1 2FUNC = 20,000 POINT
- 1 2FUNC = 5,000 Drika
- 1 Drik = 10,000,000,000,000 Drika
- 1 Drik = 2,000,000,000 2FUNC

این روابط، روابط محاسباتی/ارزشی هستند و به‌تنهایی به معنی ایجاد خودکار 2FUNC برای هر مقدار POINT نیستند.

---

## 9. Value Reservoir Principle

Drika **واحد پایهٔ ثبت ارزش (Base Value Ledger Unit)** است.

کل عرضهٔ 2FUNC از نظر نسبت محاسباتی معادل است با:

**72,207,085,028,000,000 Drika**

این مقدار یک **مبنای حسابداری/ارزشی** است و به معنی وجود ذخیرهٔ فیزیکی یا دلاری پشتوانه نیست.

---

## 10. Supply Protection

دو لایهٔ اصلی کنترل ایجاد 2FUNC وجود دارد:

### Layer 1 — Value Adjustment

ارزش هدف فعالیت حفظ می‌شود و POINT متناسب با ارزش مرجع 2FUNC تعدیل می‌گردد.

### Layer 2 — Emission Cap

مقدار 2FUNC جدید قابل ایجاد در هر مرحله و در مجموع کل عرضه، تحت سیاست انتشار قرار می‌گیرد.

این دو لایه نباید با Staking Capacity اشتباه گرفته شوند.

---

## 11. Staking Investment Principle

**مقدار Staking ذاتاً با Emission Cap محدود نمی‌شود.**

محدودیت‌های Staking، در صورت نیاز، باید از قواعدی مانند موارد زیر ناشی شوند:

- حداقل Stake
- شرایط Validator
- دورهٔ قفل
- قواعد امنیتی
- تعداد/ظرفیت Validatorها
- شرایط مشارکت شبکه

و نه از سقف Mining.

---

## 12. Architecture Boundary

### POINT

واحد سنجش فعالیت و دروازهٔ Mining.

### UVI

موتور محاسبهٔ ارزش.

### Mining Policy

سیاست تعیین مقدار 2FUNC قابل ایجاد از فعالیت معتبر.

### Staking Policy

سیاست مشارکت 2FUNC موجود در امنیت شبکه و محاسبهٔ پاداش Staking.

### 2FUNC

تنها Native Coin (کوین بومی) 2FUN Blockchain.

---

## 13. Explicit Non-Goals

این Snapshot هنوز موارد زیر را تعیین نهایی نمی‌کند:

- تقسیم دقیق عرضه بین ۱۰ مرحله
- فاصلهٔ دقیق زمانی هر مرحله، فراتر از قواعد مصوب بعدی
- درصد دقیق Mining / Staking / Validator / Treasury / Growth
- فرمول نهایی Reward
- فرمول دقیق Difficulty / Decay
- روش دقیق Price Reference و بازهٔ زمانی آن
- تعداد نهایی Validatorها
- قوانین کامل Burn
- مشخصات فنی Blockchain
- Decimal / Smallest On-Chain Unit نهایی 2FUNC

این موارد باید در مراحل بعدی جداگانه تصمیم‌گیری و Snapshot شوند.

---

## 14. Canonical Flow

User Activity
↓
POINT
↓
Value Adjustment
↓
UVI
↓
Mining Policy
↓
Emission Capacity
↓
2FUNC

مسیر مستقل شبکه:

2FUNC Existing Supply
↓
Staking
↓
Network Security / Validator
↓
Staking Reward

---

## 15. Architectural Statement

POINT معیار فعالیت است؛ UVI موتور محاسبهٔ ارزش است؛ 2FUNC تنها کوین بومی شبکه است؛ Mining و Staking دو فرآیند مستقل هستند؛ و Emission Cap فقط مقدار 2FUNC جدید قابل ایجاد را کنترل می‌کند، نه مقدار سرمایه‌ای را که کاربران می‌توانند در Staking قرار دهند.

---

**Document Status:** Core Model Locked / Parameters Unlocked

**Principle:** Archive, Never Delete
