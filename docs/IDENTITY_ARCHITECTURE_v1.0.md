# IDENTITY_ARCHITECTURE_v1.0

## 2FUN / TUFAN Identity System

Status: LOCKED  
Version: 1.0

---

# 1. Personal Code

هر کاربر در زمان ورود به پروژه یک کد پرسنلی دریافت می‌کند.

مشخصات:
- 8 رقمی
- یکتا در سطح پروژه
- ثابت تا زمان حضور کاربر در پروژه
- شناسه عمومی کاربر در هوم کلونی

مثال:
80274046

---

# 2. Home Colony

هر کاربر فقط یک Home Colony دارد.

مشخصات:
- اولین کلونی پذیرنده کاربر
- هویت دائمی کاربر
- تا زمان خروج کامل از پروژه تغییر نمی‌کند

فیلد دیتابیس:
home_colony_id

---

# 3. Colony ID

هر کلونی دارای یک شناسه اختصاصی است.

مشخصات:
- 6 رقمی
- یکتا در سطح جهانی
- Sequential (دنباله‌ای / Auto Increment)
- از 000001 تا 999999
- غیرتصادفی

مثال:
000001
000002
000003

---

# 4. Guest ID

زمانی که کاربر در کلونی میزبان حضور دارد شناسه مهمان نمایش داده می‌شود.

ساختار:
GuestID = ColonyID + PersonalCode

مثال:
48192758271436

طول:
14 رقم

---

# 5. Display Rules

## داخل Home Colony
80274046

فقط کد پرسنلی نمایش داده می‌شود.

---

## داخل Host Colony
48192758271436

کاربران متوجه مهمان بودن فرد می‌شوند اما هویت کلونی مبدأ او مستقیم دیده نمی‌شود.

---

# 6. Geography Identity

- Country
- Province
- County
- City

استفاده:
- KYC
- احراز هویت
- سطوح دسترسی ارکان کلونی

---

# 7. Colony Authority Visibility

User:
- Personal Code

Deputy 2:
- Country
- Province
- Personal Code

Deputy 1:
- Country
- Province
- County
- Personal Code

Leader:
- Full Geography
- Personal Code

---

# 8. Host Colony Tracking

تمام ورودهای کاربر به کلونی‌های میزبان باید ثبت شود.

محل ذخیره:
users_extension

در آینده:
host_colony_history

---

# 9. Identity Stability Principle

هیچ تغییر مکانی یا عضویتی نباید:
- Personal Code
- Home Colony ID
- Guest ID Logic

را تغییر دهد.

---

# 10. Core Principle

Identity ≠ Location

- مکان قابل تغییر است
- هویت ثابت است
- کلونی فقط لایه نمایش و حکمرانی است

---

END OF DOCUMENT
