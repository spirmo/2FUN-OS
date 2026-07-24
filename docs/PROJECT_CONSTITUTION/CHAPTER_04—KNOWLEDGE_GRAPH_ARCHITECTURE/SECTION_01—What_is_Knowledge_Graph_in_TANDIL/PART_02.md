CHAPTER_04 — KNOWLEDGE GRAPH ARCHITECTURE

SECTION_01 — What is Knowledge Graph in TANDIL

PART_02 — تفاوت Knowledge Graph و Relationship System

در معماری TANDIL، یکی از سوءبرداشت‌های رایج این است که Knowledge Graph و Relationship System یک مفهوم واحد هستند.

در حالی که این دو، در دو سطح متفاوت از معماری عمل می‌کنند:

- Relationship System → تعریف ارتباطات
- Knowledge Graph → اجرای شبکه کامل دانش

---

اصل بنیادین

Relationship System زیرساخت معنایی شبکه است.

Knowledge Graph خروجی اجرایی و زنده این زیرساخت است.

---

تعریف Relationship System

Relationship System مجموعه‌ای از قوانین، انواع و ساختارهایی است که:

- نحوه ارتباط میان موجودیت‌ها را تعریف می‌کند
- معنا و نوع ارتباط را مشخص می‌سازد
- اعتبار روابط را کنترل می‌کند

به بیان ساده:

«Relationship System = زبان ارتباطات»

---

تعریف Knowledge Graph

Knowledge Graph ساختاری است که:

- تمام موجودیت‌ها را در یک شبکه واحد قرار می‌دهد
- Relationshipها را فعال و قابل اجرا می‌کند
- جریان دانش را در سیستم ایجاد می‌کند

به بیان ساده:

«Knowledge Graph = اجرای زنده شبکه دانش»

---

تفاوت بنیادین

Relationship System

- سطح منطقی (Logical Layer)
- تعریف قواعد
- مستقل از اجرا
- تمرکز بر معنا

Knowledge Graph

- سطح اجرایی (Execution Layer)
- استفاده از قواعد
- فعال‌سازی شبکه
- تمرکز بر رفتار

---

تفاوت در نقش

Relationship System می‌گوید:

«چه نوع ارتباطی وجود دارد»

Knowledge Graph می‌گوید:

«این ارتباط چگونه در سیستم زنده عمل می‌کند»

---

مثال ساده

فرض کنیم:

Concept A: «اعتماد»
Concept B: «صداقت»

Relationship:

SUPPORTED_BY

---

در Relationship System:

- تعریف می‌شود که اعتماد توسط صداقت پشتیبانی می‌شود
- نوع رابطه مشخص می‌شود
- هیچ اجرایی انجام نمی‌شود

---

در Knowledge Graph:

- این رابطه در مسیر استدلال فعال می‌شود
- در تحلیل‌ها استفاده می‌شود
- در مسیرهای یادگیری اثر می‌گذارد

---

سطح انتزاع

Relationship System = طراحی نقشه

Knowledge Graph = اجرای نقشه در دنیای واقعی

---

وابستگی بین آن‌ها

Knowledge Graph بدون Relationship System قابل تعریف نیست.

اما Relationship System بدون Knowledge Graph می‌تواند به‌صورت نظری وجود داشته باشد.

---

نقش در معماری کلان

Relationship System پایه طراحی است.

Knowledge Graph نتیجه عملی آن طراحی است.

---

اصل استقلال

این دو لایه نباید با هم اشتباه گرفته شوند:

- تغییر در Relationship System الزاماً به معنای تغییر در Graph نیست
- Graph ممکن است نسخه‌های مختلف Relationship System را اجرا کند

---

نقش در TANDIL

در TANDIL:

- Relationship System = طراحی معنا
- Knowledge Graph = اجرای معنا

این تفکیک باعث می‌شود سیستم هم دقیق باشد و هم قابل اجرا در مقیاس بزرگ.

---

اصل معماری

بر اساس قانون اساسی TANDIL:

Relationship System مسئول تعریف قواعد ارتباط است و Knowledge Graph مسئول اجرای زنده این روابط در یک شبکه یکپارچه است.

این جداسازی تضمین می‌کند که طراحی منطقی و اجرای عملی سیستم، دو لایه مستقل اما هماهنگ باقی بمانند.
