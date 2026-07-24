CHAPTER_05 — QUESTION SYSTEM ARCHITECTURE

SECTION_04 — Question Generation Engine

PART_11 — جمع‌بندی معماری Question Generation Engine

در این بخش، معماری موتور تولید سؤال به‌طور کامل تعریف شد.

مشخص گردید که Question Generation Engine یک تولیدکننده متن نیست، بلکه یک موتور معماری است که بر پایه حقیقت، ساختار و قوانین پروژه، تعامل مناسب را ایجاد می‌کند.

---

جایگاه Question Generation Engine

Question Generation Engine در مرکز ارتباط میان:

- Knowledge Graph
- Question Bank
- Human Model
- Digital Twin
- Book of Life

قرار دارد.

اما مالک هیچ‌یک از این بخش‌ها نیست.

---

آنچه در این بخش تثبیت شد

Question Generation Engine:

- از ورودی‌های معماری استفاده می‌کند.
- Question مناسب را انتخاب یا تولید می‌کند.
- Question را شخصی‌سازی می‌کند.
- خروجی را اعتبارسنجی می‌کند.
- Question Instance ایجاد می‌کند.
- خروجی را برای Question Engine ارسال می‌کند.
- هیچ تحلیل یا تصمیم نهایی درباره کاربر انجام نمی‌دهد.

---

رابطه با Question Bank

Question Bank منبع الگوهای سؤال است.

Question Generation Engine مصرف‌کننده این الگوهاست.

در صورت کافی بودن Templateها، تولید جدید انجام نمی‌شود.

---

رابطه با Knowledge Graph

Knowledge Graph حقیقت را فراهم می‌کند.

Question Generation Engine روش تعامل با آن حقیقت را ایجاد می‌کند.

---

رابطه با AI

AI تنها یک ابزار کمکی است.

تمام خروجی‌های AI تحت کنترل معماری قرار می‌گیرند.

هیچ خروجی هوش مصنوعی بدون اعتبارسنجی وارد چرخه تعامل نمی‌شود.

---

رابطه با Human Model

Human Model تنها اطلاعات لازم برای شخصی‌سازی را فراهم می‌کند.

Question Generation Engine مجاز به تغییر Human Model نیست.

---

رابطه با Book of Life

Book of Life نتیجه تعامل را ثبت می‌کند.

Question Generation Engine تنها Question را تولید می‌کند.

---

ویژگی‌های اصلی موتور

این موتور باید:

- قابل توسعه باشد.
- قابل ممیزی باشد.
- قابل بازتولید باشد.
- مستقل از مدل‌های AI باشد.
- مستقل از کاربران باشد.
- کاملاً نسخه‌بندی شود.

---

نگاه فلسفی

Question Generation Engine حقیقت را خلق نمی‌کند.

Question Generation Engine تنها بهترین مسیر گفت‌وگو با حقیقت را برای هر انسان طراحی می‌کند.

این تفاوت، مهم‌ترین مرز میان TANDIL و بسیاری از سامانه‌های متداول تولید محتواست.

---

نتیجه نهایی بخش

Question Generation Engine پلی است میان حقیقت و انسان.

نه حقیقت را تغییر می‌دهد،

نه انسان را تحلیل می‌کند،

بلکه مناسب‌ترین ابزار گفت‌وگو را میان این دو ایجاد می‌نماید.

---

اصل معماری

بر اساس قانون اساسی TANDIL:

Question Generation Engine مسئول طراحی و تولید تعاملات معتبر میان انسان و Conceptها است و تمام فعالیت‌های آن باید در چارچوب Knowledge Graph، Question Bank، قوانین Governance و اصول معماری پروژه انجام شود، بدون آنکه در مالکیت حقیقت یا تحلیل انسان دخالتی داشته باشد.

این اصل پایان معماری موتور تولید سؤال را مشخص می‌کند و زمینه را برای ورود به مرحله بعدی، یعنی Answer Analysis Engine (موتور تحلیل پاسخ) فراهم می‌سازد.
