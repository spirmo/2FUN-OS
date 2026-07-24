# SNAPSHOT_CONCEPT_DATABASE_SCHEMA_v1.0_LOCKED

Project:
2FUN Super App (توفان)

Module:
Knowledge Injection Engine

Status:
LOCKED

Version:
1.0


# Concept Item Architecture


## Visible Items

Total:
36 Items


### Mandatory Items
(11 Items)

1. عنوان فارسی
2. دامنه دانش
3. دسته‌بندی
4. معنای اصلی کانسپت
5. تعریف کانسپت
6. توضیح کوتاه
7. منبع اطلاعات
8. آدرس منبع
9. نویسنده منبع
10. سال انتشار منبع
11. شواهد و مستندات


### Optional Items
(25 Items)

1. عنوان انگلیسی
2. عنوان عربی
3. عنوان سایر زبان‌ها
4. ترجمه‌ها
5. زبان ترجمه
6. متن ترجمه شده
7. کانسپت‌های مرتبط
8. ویژگی‌ها
9. مقدار ویژگی
10. سوالات مرتبط
11. پاسخ‌ها
12. ماموریت‌ها
13. عنوان ماموریت
14. توضیح ماموریت
15. برچسب‌ها
16. سطح سختی
17. یادداشت‌ها
18. تصاویر
19. ویدئوها
20. فایل‌های ضمیمه
21. نمونه‌ها
22. نمونه‌های نقض
23. منابع تکمیلی
24. یادداشت اعتبارسنجی
25. پیشنهادهای توسعه آینده


# Internal Database Items

Total:
11 Items

1. node_id
2. concept_code
3. database_id
4. topic_id
5. creator
6. created_at
7. status
8. completeness
9. history
10. version
11. snapshot_reference


# Database Expansion Reservation

Reserved Columns:

25 Columns

Purpose:

Future compatibility and preventing schema migration challenges.

Status:

Reserved for future Knowledge Engine expansion.


# Final Architecture

Visible Concept Items:
36

Internal System Items:
11

Database Columns:
43 Existing + Expansion Fields

Architecture Status:

LOCKED
CONCEPT ARCHITECTURE v1.1

1) concepts
----------------
هسته اصلی کانسپت


2) concept_items
----------------
۳۶ آیتم قابل مشاهده کاربر

- ۱۱ آیتم اجباری
- ۲۵ آیتم اختیاری


3) concept_system
----------------
۱۱ آیتم غیر قابل مشاهده

- node_id
- concept_code
- id
- topic_id
- creator
- created_at
- status
- completeness
- history
- version
- snapshot_reference


4) concept_extensions
----------------
۲۵ فضای توسعه آینده

- extension_key
- extension_value
- data_type
- created_at
- updated_at


