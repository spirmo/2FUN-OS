# EV-0010 — Foundation Architecture Amendments

Status: Pending

Purpose:
ثبت متمم‌های معماری کشف‌شده در دوره Foundation که پس از بررسی وارد PROJECT_CONSTITUTION خواهند شد.

---

# Amendment 1 — Canonical Source Principle

هر سند، قانون، قرارداد یا مشخصات فنی فقط یک نسخه مرجع دارد.

- هیچ‌گاه دو نسخه قابل ویرایش هم‌زمان از یک سند وجود نخواهد داشت.
- سایر پروژه‌ها یا ماژول‌ها فقط به نسخه مرجع ارجاع می‌دهند.
- در دوره مهاجرت، Reference جایگزین Copy خواهد شد.

---

# Amendment 2 — Bilingual Documentation Principle

تمام اسناد رسمی پروژه باید دارای نسخه مرجع انگلیسی باشند.

- نسخه فارسی ترجمه رسمی همان سند است.
- هیچ سند رسمی نباید فقط به یک زبان نگهداری شود.

Naming:

DOCUMENT.md
DOCUMENT.fa.md

در آینده زبان‌های دیگر نیز با همین الگو اضافه خواهند شد.

---

# Amendment 3 — Documentation Contract Principle

هر سند رسمی باید دارای Contract باشد.

نمونه‌ها:

- Language Contract
- Documentation Contract
- Snapshot Contract
- Naming Contract

تمام این قراردادها زیرمجموعه سیستم Contracts خواهند بود.

---

# Amendment 4 — Automated Enforcement Principle

هر قانونی که امکان پیاده‌سازی خودکار داشته باشد، نباید فقط در مستندات باقی بماند.

باید توسط ابزارهای پروژه کنترل شود.

نمونه‌ها:

- Git Hooks
- CI/CD
- Validation Scripts
- Contract Validators

---

# Amendment 5 — Architectural Immutability Principle

تصمیمات معماری، پس از تصویب، حذف یا تغییر داده نمی‌شوند مگر از طریق فرآیند رسمی قانون اساسی.

هر تغییر باید:

- مستندسازی شود.
- نسخه‌بندی شود.
- دلیل تغییر ثبت شود.
- در Snapshotهای معماری ذخیره شود.

---

# Amendment 6 — Architecture Snapshot Principle

هر تصمیم مهم پروژه باید قبل از اجرای تغییرات بزرگ در قالب Snapshot ثبت شود.

Snapshot باید شامل:

- وضعیت فعلی
- دلیل تصمیم
- اهداف
- برنامه مهاجرت
- اثرات بر سایر ماژول‌ها
- تاریخ
- نسخه

باشد.

---

# Amendment 7 — Progressive Migration Principle

در مهاجرت بین پروژه‌ها:

1. ابتدا Reference ایجاد می‌شود.
2. سپس اعتبارسنجی انجام می‌شود.
3. سپس مهاجرت کامل انجام می‌شود.

در هیچ مرحله‌ای دو مرجع مستقل ایجاد نمی‌شود.

---

# Amendment 8 — Guardian Architecture Principle

پوشه contracts صرفاً محل نگهداری قراردادهای API نیست.

بلکه نگهبان معماری کل اکوسیستم است.

Contracts شامل:

- API
- Events
- Schemas
- Governance
- Documentation
- Architecture
- Naming
- Release
- سایر قراردادهای بنیادین

خواهد بود.

---

# Amendment 9 — Project Memory Independence Principle

پروژه نباید وابسته به حافظه افراد باشد.

هر تصمیم مهم باید در یکی از موارد زیر ثبت شود:

- PROJECT_CONSTITUTION
- Contract
- Snapshot
- Architecture Documentation

به گونه‌ای که سال‌ها بعد نیز قابل بازیابی و استناد باشد.

---

# Amendment 10 — Foundation First Principle

در دوره Foundation:

- از مهاجرت‌های بزرگ خودداری می‌شود.
- ابتدا زیرساخت پایدار می‌شود.
- سپس انتقال قوانین، ماژول‌ها و معماری انجام می‌شود.

---

Status:
Pending Review

Target:
PROJECT_CONSTITUTION
