# IDENTITY_ENGINE_SPEC_v1.0

## Project
2FUN / TOOFAN

## Status
DRAFT LOCKED

---

# 1. PURPOSE

Identity Engine مسئول تولید، مدیریت، نمایش و آرشیو شناسه‌های کاربران پروژه است.

این سیستم مستقل از سیستم رتبه‌بندی، کلونی‌ها و اقتصاد عمل می‌کند اما با آنها یکپارچه است.

---

# 2. IDENTITY COMPONENTS

هر کاربر دارای دو شناسه اصلی است:

## 2.1 Personal Code

کد پرسنلی هشت رقمی

Format:

XXXXXXXX

Example:

12345678

ویژگی‌ها:

- یکتا در سطح پروژه
- از زمان ورود کاربر ایجاد می‌شود
- در کلونی مبدأ شناسه اصلی کاربر محسوب می‌شود
- برای همه اعضای کلونی مبدأ قابل مشاهده است

---

## 2.2 Home Colony ID

شناسه کلونی مبدأ

Format:

CCCCCC

Example:

000123

ویژگی‌ها:

- هنگام ایجاد کلونی تولید می‌شود
- همیشه ثابت است
- با خروج یا ورود به کلونی‌های دیگر تغییر نمی‌کند
- به کلونی تعلق دارد نه به کاربر

---

# 3. USER ID

شناسه کامل کاربر

ساختار:

CCC PP CC SS XXXXXXXX

شامل:

CCC = Country Code (3 digits)

PP = Province Code (2 digits)

CC = County Code (2 digits)

SS = City Code (2 digits)

XXXXXXXX = Personal Code (8 digits)

Example:

12345060712345678

---

# 4. PARTIAL USER ID

تا قبل از احراز هویت کامل

قسمت‌های نامشخص با ** نمایش داده می‌شوند.

Example:

123-**-**-**-12345678

---

# 5. DISPLAY RULES

## 5.1 Home Colony

نمایش:

XXXXXXXX

Example:

12345678

---

## 5.2 Guest User

نمایش:

CCCCCCXXXXXXXX

Example:

00012312345678

ویژگی:

- اعضای کلونی میزبان فقط متوجه مهمان بودن کاربر می‌شوند
- نام کلونی مبدأ مشخص نمی‌شود
- فقط شناسه 14 رقمی نمایش داده می‌شود

---

# 6. COLONY ID SYSTEM

شناسه کلونی شش رقمی است.

Format:

000001
000002
000003
...
999999

ویژگی‌ها:

- ترتیبی
- یکتا
- غیرتصادفی
- غیرقابل تغییر

---

# 7. MEMBERSHIP TRACE

تمام جابجایی‌های کاربر بین کلونی‌ها ثبت می‌شود.

حداقل اطلاعات:

- User ID
- Home Colony
- Host Colony
- Join Date
- Leave Date
- Status

---

# 8. USER STATUS

ACTIVE

کاربر فعال

DORMANT

کاربر موجود ولی غیرفعال

EXPELLED

اخراج‌شده از پروژه

---

# 9. EXPULSION RULE

در صورت اخراج:

- شناسه عملیاتی کاربر حذف می‌شود
- امکان استفاده مجدد از شناسه وجود ندارد
- تمام سوابق تاریخی حفظ می‌شوند

---

# 10. RESERVED FIELDS

users_extension

reserved1

Home Colony Trace

reserved2

Guest Colony Trace

reserved3

Identity Verification State

reserved4

Identity Metadata

reserved5+

Future Expansion

---

# 11. ENGINE RESPONSIBILITIES

Identity Engine باید:

- تولید کد پرسنلی
- تولید شناسه کامل
- تولید شناسه موقت
- مدیریت Home Colony
- مدیریت Trace
- مدیریت نمایش شناسه‌ها
- آرشیو شناسه‌های حذف‌شده

را انجام دهد.

---

END OF SPEC
