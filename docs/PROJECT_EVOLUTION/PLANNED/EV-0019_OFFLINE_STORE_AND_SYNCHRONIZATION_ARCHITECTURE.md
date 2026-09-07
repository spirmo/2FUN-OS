EV — Offline Store / Draft / Sync Architecture

وضعیت: ثبت‌شده برای توسعه آینده — فعلاً خارج از مسیر اجرایی فعلی

هدف

تبدیل SQLite موجود در Mobile از یک Concept Storage محلی به یک Offline Store / Local Replica / Draft & Sync Queue، بدون ایجاد مالکیت مستقل برای Concept در APK.

اصل معماری

مالکیت رسمی Concept، وضعیت آن، Version، Concept Code، Approval، Reject، امتیاز، انتشار و انتقال به Knowledge Engine همچنان در Concept Engine و Database Service مرکزی باقی می‌ماند.

Mobile SQLite فقط می‌تواند در آینده برای موارد زیر استفاده شود:

- نگهداری Replica/Cache از داده‌های دریافت‌شده از Backend
- نگهداری Draftهای ایجادشده توسط کاربر
- نگهداری عملیات Pending برای Sync
- نگهداری وضعیت همگام‌سازی
- پشتیبانی از فعالیت کاربر در حالت Offline

مسیر آینده Offline

Mobile
→ Local Draft / Offline Store
→ Sync Queue
→ اتصال مجدد
→ Concept API
→ Concept Engine
→ Database Service مرکزی
→ Approval / Governance
→ EventBus
→ Knowledge Engine

محدودیت مالکیت

Mobile نباید در حالت Offline یا Online:

- Concept رسمی ایجاد و مالک شود
- Concept Code رسمی تولید کند
- Node رسمی تولید کند
- Approval یا Reject رسمی را مستقیماً در SQLite اعمال کند
- وضعیت رسمی Concept را مستقل از Backend تغییر دهد
- امتیاز یا Publication رسمی را محلی تعیین کند

موارد Legacy که در زمان اجرای EV باید تعیین تکلیف شوند

- "concepts"
- "concept_items"
- "concept_system"
- "concept_extensions"
- "createFullConcept()"
- "_calculateCompleteness()"
- صفحات و سرویس‌هایی که مستقیماً به جداول Concept محلی وابسته‌اند

این اجزا باید در آینده یا به Offline Store/Replica/Draft تبدیل شوند یا در صورت عدم نیاز، به‌صورت کنترل‌شده بازنشسته شوند.

نکته مهم درباره Reject

مسیر فعلی Reject که مستقیماً وضعیت "concepts" را در SQLite موبایل تغییر می‌دهد، یک نمونه روشن از مالکیت نادرست Local Storage است.

در معماری نهایی:

Governance APK → Reject API → Concept Engine → Database Service → EventBus / downstream processing

و Mobile SQLite صرفاً در آینده می‌تواند نتیجه Reject را به‌عنوان Replica/Cache دریافت و نگهداری کند.

ترتیب اجرا

این EV فقط پس از تکمیل کامل Pipeline اصلی اجرا خواهد شد.

اولویت فعلی:

User APK
→ Concept Engine
→ Database Service
→ Approval Queue
→ Governance APK
→ Approve / Reject
→ EventBus
→ Knowledge Engine / KCE
→ Completion / Publication
→ تست واقعی APK

Offline Development تا پایان این مسیر کاملاً متوقف است.
