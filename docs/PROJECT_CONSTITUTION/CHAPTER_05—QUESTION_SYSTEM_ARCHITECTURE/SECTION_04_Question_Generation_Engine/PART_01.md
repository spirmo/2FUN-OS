CHAPTER_05 — QUESTION SYSTEM ARCHITECTURE

SECTION_04 — Question Generation Engine

PART_01 — موتور تولید سؤال چیست؟

Question Bank مجموعه‌ای از Question Templateهای معتبر را در اختیار سیستم قرار می‌دهد.

اما همه تعاملات را نمی‌توان صرفاً با Templateهای از پیش طراحی‌شده انجام داد.

در بسیاری از موقعیت‌ها، سیستم باید بتواند متناسب با وضعیت واقعی کاربر، Question جدید ایجاد کند.

این وظیفه بر عهده Question Generation Engine (موتور تولید سؤال) است.

---

اصل بنیادین

Question Generation Engine سؤال را از هیچ تولید نمی‌کند.

بلکه با استفاده از حقیقت موجود در Knowledge Graph و الگوهای موجود در Question Bank، Question مناسب را ایجاد می‌کند.

---

تعریف Question Generation Engine

«Question Generation Engine زیرسیستمی است که بر اساس Conceptها، Question Templateها، Context، Human Model و قوانین معماری، Questionهای جدید یا شخصی‌سازی‌شده تولید می‌کند.»

---

هدف موتور تولید سؤال

این موتور برای پاسخ به این پرسش طراحی شده است:

«اگر Question آماده‌ای برای وضعیت فعلی وجود نداشته باشد، چگونه باید مناسب‌ترین Question را ایجاد کنیم؟»

---

جایگاه در معماری

Question Generation Engine یکی از زیرمجموعه‌های Question Engine است.

جریان کلی به شکل زیر است:

Knowledge Graph
        ↓
Question Bank
        ↓
Question Engine
        ↓
Question Generation Engine
        ↓
Generated Question

بنابراین، موتور تولید سؤال تصمیم‌گیر نیست.

تصمیم توسط Question Engine گرفته می‌شود.

---

چه زمانی فعال می‌شود؟

Question Generation Engine معمولاً در شرایط زیر فعال می‌شود:

- Question مناسب در بانک وجود ندارد.
- شخصی‌سازی عمیق لازم است.
- Context ویژه‌ای ایجاد شده است.
- مثال اختصاصی موردنیاز است.
- Question باید متناسب با مسیر زندگی همان کاربر ساخته شود.

---

ورودی‌های موتور

برای تولید یک Question، موتور از اطلاعات زیر استفاده می‌کند:

- Concept
- Relationshipهای Knowledge Graph
- Question Template
- Context
- Human Model
- Digital Twin
- Book of Life
- هدف تعامل
- راهبرد تعامل
- قوانین Governance

---

خروجی موتور

خروجی این موتور یک Question قابل اجرا است.

این Question:

- دارای شناسه است.
- به Conceptها متصل است.
- قابل تحلیل است.
- و می‌تواند به کاربر نمایش داده شود.

---

تفاوت با AI Chat

هدف این موتور، تولید متن آزاد نیست.

هدف آن، تولید Question معتبر معماری است.

هر خروجی باید:

- ساختار مشخص داشته باشد.
- قوانین سیستم را رعایت کند.
- و قابل تحلیل باشد.

---

نقش در آینده

با رشد TANDIL، نقش این موتور افزایش پیدا خواهد کرد.

زیرا تعداد موقعیت‌هایی که نیازمند تعامل اختصاصی هستند، بسیار بیشتر از تعداد Questionهای از پیش طراحی‌شده خواهد بود.

---

اصل معماری

بر اساس قانون اساسی TANDIL:

Question Generation Engine مسئول تولید Questionهای معتبر، شخصی‌سازی‌شده و سازگار با معماری است و تنها بر اساس Conceptهای Knowledge Graph، Question Templateهای معتبر و وضعیت واقعی کاربر عمل می‌کند.

این اصل تضمین می‌کند که حتی Questionهای جدید نیز همان کیفیت، انسجام و قابلیت تحلیل Questionهای استاندارد را حفظ کنند.
