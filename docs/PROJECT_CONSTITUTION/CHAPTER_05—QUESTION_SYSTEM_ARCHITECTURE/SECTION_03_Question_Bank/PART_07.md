CHAPTER_05 — QUESTION SYSTEM ARCHITECTURE

SECTION_03 — Question Bank

PART_07 — رابطه Question Bank با Knowledge Graph

Question Bank و Knowledge Graph دو بخش کاملاً متفاوت از معماری TANDIL هستند، اما بدون یکدیگر نمی‌توانند وظیفه خود را به‌درستی انجام دهند.

Knowledge Graph حقیقت و روابط میان Conceptها را نگهداری می‌کند.

Question Bank روش‌های تعامل با آن حقیقت را ذخیره می‌کند.

این دو باید به‌صورت دقیق و استاندارد با یکدیگر در ارتباط باشند.

---

اصل بنیادین

Knowledge Graph حقیقت را نگهداری می‌کند.

Question Bank ابزار تعامل با حقیقت را نگهداری می‌کند.

هیچ‌یک جایگزین دیگری نیست.

---

تعریف رابطه

«Question Bank از Knowledge Graph تغذیه می‌شود و تمام اعتبار معماری خود را از ارتباط با Conceptها و Relationshipهای موجود در Knowledge Graph دریافت می‌کند.»

---

هدف این ارتباط

این مفهوم برای پاسخ به این پرسش طراحی شده است:

«Question Bank از کجا می‌فهمد هر Template برای چه مفهومی طراحی شده است؟»

پاسخ:

از Knowledge Graph.

---

جهت وابستگی

وابستگی فقط در یک جهت است.

Knowledge Graph
        ↓
Question Bank

اما:

Question Bank
        ✕
Knowledge Graph

Question Bank حق تغییر Knowledge Graph را ندارد.

---

نقش Concept

هر Question Template باید به یک یا چند Concept موجود در Knowledge Graph متصل باشد.

اگر Concept حذف شود یا تغییر اساسی کند،

Templateهای وابسته نیز باید بررسی شوند.

---

نقش Relationship

گاهی Question فقط به یک Concept وابسته نیست.

Knowledge Graph مشخص می‌کند:

- چه Conceptهای دیگری مرتبط هستند.
- چه پیش‌نیازهایی وجود دارد.
- و چه مسیرهایی برای ادامه یادگیری مناسب‌تر هستند.

Question Bank از این اطلاعات برای طراحی یا انتخاب Template استفاده می‌کند.

---

مثال

فرض کنید Concept اصلی:

«مسئولیت‌پذیری»

باشد.

Knowledge Graph نشان می‌دهد که این Concept با موارد زیر ارتباط دارد:

- صداقت
- اعتماد
- وفای به عهد

Question Bank می‌تواند Templateهایی طراحی کند که:

- فقط مسئولیت‌پذیری را بررسی کنند،
- یا چند Concept مرتبط را هم‌زمان درگیر نمایند.

---

استقلال بانک سؤال

اگر تمام Question Templateها حذف شوند،

Knowledge Graph همچنان معتبر باقی می‌ماند.

اما اگر Knowledge Graph حذف شود،

Question Bank دیگر معنای معماری خود را از دست خواهد داد.

این موضوع نشان می‌دهد که وابستگی تنها در یک جهت است.

---

نقش در توسعه آینده

با اضافه شدن Conceptهای جدید به Knowledge Graph،

Question Bank می‌تواند برای آن‌ها Templateهای جدید ایجاد کند.

بنابراین، توسعه Question Bank از توسعه Knowledge Graph پیروی می‌کند.

---

مزایای این معماری

این ساختار باعث می‌شود:

- حقیقت و تعامل از هم جدا باقی بمانند.
- توسعه بانک سؤال ساده‌تر شود.
- تغییر در روش آموزش، حقیقت را تغییر ندهد.
- موتور سؤال همیشه بر پایه Knowledge Graph تصمیم بگیرد.

---

اصل معماری

بر اساس قانون اساسی TANDIL:

Question Bank باید تمام ارتباطات مفهومی خود را از Knowledge Graph دریافت کند و هیچ Templateی نباید بدون اتصال به Conceptهای معتبر و Relationshipهای تعریف‌شده در Knowledge Graph در بانک سؤال ثبت یا استفاده شود.

این اصل تضمین می‌کند که تمام سؤال‌های TANDIL ریشه در حقیقت معماری‌شده داشته باشند و هیچ Question مستقلی خارج از ساختار دانش سیستم ایجاد نشود.
