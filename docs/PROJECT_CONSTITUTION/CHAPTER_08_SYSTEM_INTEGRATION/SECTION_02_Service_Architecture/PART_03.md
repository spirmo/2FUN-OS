CHAPTER_08 — SYSTEM INTEGRATION

SECTION_02 — Service Architecture

PART_03 — طبقه‌بندی Serviceها (Service Classification)

همه Serviceها نقش یکسانی ندارند.

برخی تنها داده‌ای را برمی‌گردانند.

برخی داده جدید ثبت می‌کنند.

برخی عملیات تحلیلی انجام می‌دهند.

و برخی تنها برای کنترل یا اعتبارسنجی به کار می‌روند.

برای جلوگیری از آشفتگی معماری، تمامی Serviceهای TANDIL در دسته‌های استاندارد طبقه‌بندی می‌شوند.

---

اصل بنیادین

هر Service باید دقیقاً در یک دسته معماری مشخص قرار گیرد.

---

تعریف Service Classification

«Service Classification فرآیند دسته‌بندی سرویس‌های معماری بر اساس نوع مسئولیت و نقش آن‌ها در سامانه است.»

---

هدف این طراحی

این مفهوم برای پاسخ به این پرسش طراحی شده است:

«هر Service دقیقاً چه نوع خدمتی ارائه می‌کند؟»

---

نوع اول — Query Service

این سرویس‌ها فقط اطلاعات را بازیابی می‌کنند.

ویژگی‌ها:

- داده را تغییر نمی‌دهند.
- وضعیت سامانه را تغییر نمی‌دهند.
- فقط خواندنی (Read Only) هستند.

نمونه‌ها:

- Get Human Model
- Load Timeline
- Search Concept

---

نوع دوم — Command Service

این سرویس‌ها وضعیت سامانه را تغییر می‌دهند.

نمونه‌ها:

- Register Event
- Update Human Model
- Create Snapshot

---

نوع سوم — Analysis Service

این سرویس‌ها داده‌ها را تحلیل می‌کنند.

نمونه‌ها:

- Answer Analysis
- Growth Analysis
- Profile Calculation

---

نوع چهارم — Validation Service

این سرویس‌ها مسئول بررسی اعتبار داده‌ها هستند.

نمونه‌ها:

- Validate Concept
- Validate Governance Rules
- Validate Input

---

نوع پنجم — Integration Service

این سرویس‌ها ارتباط میان چند موتور را مدیریت می‌کنند.

نمونه‌ها:

- Synchronization
- Data Mapping
- Cross Engine Coordination

---

ساختار منطقی

Services
   ├── Query
   ├── Command
   ├── Analysis
   ├── Validation
   └── Integration

---

مزایای این طراحی

این معماری باعث می‌شود:

- مسئولیت هر Service روشن باشد.
- توسعه سرویس‌ها آسان‌تر شود.
- امنیت سامانه افزایش یابد.
- طراحی APIها استاندارد باقی بماند.

---

ارتباط با Governance

Governance می‌تواند سیاست‌های متفاوتی برای هر دسته از Serviceها اعمال کند.

برای مثال:

- Query Service نیازمند مجوز خواندن است.
- Command Service نیازمند مجوز نوشتن است.

---

ارتباط با Explainability

Explainability می‌تواند بر اساس نوع Service،

روش مناسب توضیح را انتخاب کند.

---

نگاه فلسفی

در TANDIL:

هر سرویس باید تنها یک نقش مشخص داشته باشد.

چندوظیفه‌ای بودن Serviceها آغاز پیچیدگی معماری است.

---

اصل معماری

بر اساس قانون اساسی TANDIL:

تمام Serviceهای معماری TANDIL باید بر اساس نقش خود در یکی از دسته‌های Query، Command، Analysis، Validation یا Integration قرار گیرند و هیچ Service نباید هم‌زمان مسئول چند نقش معماری مستقل باشد.

این اصل تضمین می‌کند که معماری سرویس‌های TANDIL ساده، شفاف، قابل توسعه و منطبق بر اصل مسئولیت واحد باقی بماند.
