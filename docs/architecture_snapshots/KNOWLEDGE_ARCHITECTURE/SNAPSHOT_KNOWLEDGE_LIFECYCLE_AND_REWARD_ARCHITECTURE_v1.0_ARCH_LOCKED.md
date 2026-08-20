# SNAPSHOT_KNOWLEDGE_LIFECYCLE_AND_REWARD_ARCHITECTURE_v1.0_ARCH_LOCKED

Project:
2FUN Super App (توفان)

Module:
Knowledge Architecture / Knowledge Injection Engine / Knowledge Completion Engine

Status:
ARCHITECTURE LOCKED

Version:
1.0

Purpose:
این سند معماری کامل چرخه زندگی Concept (کانسپت)، قوانین ورود دانش به اکوسیستم، سیستم تکمیل دانش، و مدل جدید پاداش‌دهی را تعریف می‌کند.

این Snapshot مرجع اصلی توسعه‌های آینده در حوزه:
- Concept Creation
- Governance Approval
- Knowledge Engine
- Knowledge Completion Engine
- Reward Engine

خواهد بود.

---

# 1. Architectural Decision Summary

در نسخه‌های قبلی معماری، چند بخش از چرخه زندگی Concept و مدل Reward به صورت جداگانه تعریف شده بودند.

این Snapshot با هدف یکپارچه‌سازی قوانین زیر ایجاد شده است:

1. جداسازی کامل مرحله ایجاد Concept از مرحله تکمیل دانش.
2. تعریف Governance Approval به عنوان دروازه ورود دانش به Knowledge Engine.
3. اصلاح مدل امتیازدهی Fieldها.
4. ایجاد سیستم تشویقی برای تکمیل Conceptهای ناقص.
5. جلوگیری از سوءاستفاده از ضریب‌های تشویقی.

تمام قوانین این سند LOCKED هستند و هر تغییر آینده نیازمند Snapshot جدید خواهد بود.

---

# 2. Concept Lifecycle Architecture

چرخه کامل زندگی یک Concept:

Concept Creation

↓

Mandatory Validation

↓

Concept Registration

↓

Governor Approval

↓

Knowledge Engine Entry

↓

Knowledge Completion Analysis

↓

Completion Queue (در صورت نیاز)

↓

Published Knowledge


---

# 3. Concept Creation Rules

Concept Creation اولین مرحله تولید دانش است.

در این مرحله فقط بررسی می‌شود که آیا Concept از نظر ساختاری قابل ثبت است یا خیر.

Concept بدون Dataset حداقلی معتبر، وجود رسمی در سیستم ندارد.

---

# 4. Mandatory Dataset Rule

هر Concept برای ایجاد شدن باید تمام آیتم‌های اجباری خود را داشته باشد.

آیتم‌های اجباری شرط وجود Concept هستند.

نمونه آیتم‌های اجباری:

- عنوان فارسی
- دامنه دانش
- دسته‌بندی
- معنای اصلی Concept
- تعریف Concept
- توضیح کوتاه
- منبع اطلاعات
- آدرس منبع
- نویسنده منبع
- سال انتشار منبع
- شواهد و مستندات

---

# 5. Mandatory Validation Behavior

در زمان ایجاد Concept:

اگر حتی یک آیتم اجباری وجود نداشته باشد:

- Concept ساخته نمی‌شود.
- وارد Registry دانش نمی‌شود.
- وارد Completion Queue نمی‌شود.
- Reward ایجاد نمی‌شود.

Concept فقط زمانی ثبت می‌شود که تمام Mandatory Items معتبر باشند.

---

# 6. Governance Approval Gate

ثبت اولیه Concept به معنی فعال شدن آن در اکوسیستم نیست.

هر Concept بعد از عبور از Mandatory Validation باید وارد مرحله Governance Approval شود.

چرخه:

Concept Registered

↓

Governor Review

↓

Approved / Rejected


---

# 7. Governance Decision Rules

## Approved

اگر Concept توسط Governor تأیید شود:

- اجازه ورود به Knowledge Engine را دریافت می‌کند.
- امکان بررسی کامل بودن دانش آن فعال می‌شود.
- می‌تواند وارد فرآیند Completion شود.

---

## Rejected

اگر Concept رد شود:

- وارد Knowledge Engine نمی‌شود.
- فعال نمی‌شود.
- وضعیت رد شدن آن در History ثبت می‌شود.

هیچ اطلاعاتی حذف نمی‌شود.

---

# 8. Knowledge Engine Entry Rule

تنها Conceptهایی که:

1. تمام Mandatory Items را دارند.
2. Approval Governance را دریافت کرده‌اند.

می‌توانند وارد Knowledge Engine شوند.


---

# 9. Separation Between Creation and Completion

یک تصمیم معماری مهم:

Concept Creation و Knowledge Completion دو فرآیند جدا هستند.


## Concept Creation

هدف:

ایجاد یک Concept معتبر.


شرط:

تکمیل Mandatory Dataset


---

## Knowledge Completion

هدف:

افزایش کیفیت و کامل کردن اطلاعات Concept.


شرط:

Concept قبلاً ثبت و تأیید شده باشد.


---

# 10. Completion Queue Architecture

Completion Queue محل نگهداری Conceptهای ناقص بعد از Approval است.

Completion Queue شامل:

Approved Concept

+

Incomplete Knowledge Fields


است.


---

# 11. Completion Queue Exclusion Rules

موارد زیر وارد Completion Queue نمی‌شوند:

- Concept ناقص در زمان ایجاد اولیه
- Concept رد شده توسط Governance
- Concept فاقد Mandatory Dataset


---

# 12. Completion Priority Model

هدف Completion Queue:

ایجاد رقابت برای تکمیل دانش ناقص است.

اهمیت تکمیل دانش بر اساس ساختار زیر تعریف می‌شود:

Mandatory Contribution:

30%


Optional Contribution:

70%


---

# 13. Knowledge Completeness Calculation

هر Concept دارای درصد تکمیل است.

نمونه:

25%

↓

60%

↓

90%

↓

100%


این درصد نشان‌دهنده میزان تکمیل دانش Concept است.

این مقدار در موارد زیر استفاده می‌شود:

- Progress Tracking
- Completion Incentive
- Knowledge Quality Analysis


---

# 14. Completion Ownership Concept

تکمیل دانش دارای مالکیت مستقل است.

هر Field تکمیل‌شده دارای:

- Creator
- First Approved Contributor
- Last Editor
- Create Date
- Edit Date

خواهد بود.


هیچ کاربری برای تکمیل Field دیگران پاداش دریافت نمی‌کند.


---

# 15. Knowledge Reward Architecture

سیستم پاداش Knowledge بر اساس تکمیل Field طراحی شده است.

اصل اصلی:

هر Field ارزش مستقل دارد و تکمیل معتبر هر Field می‌تواند Reward ایجاد کند.


---

# 16. اصلاح مدل قدیمی Reward

در معماری قبلی:

برای آیتم‌های اختیاری فقط یک پاداش بر اساس سختی تعیین شده بود:

- 25 XP
- 30 XP
- 35 XP


این مدل اصلاح شد.

---

# 17. مدل جدید Reward Calculation

هر Field دارای دو بخش پاداش است:

1. Base Reward
2. Difficulty Reward


---

# 18. Base Reward

تمام Fieldها:

اعم از:

- Mandatory Fields
- Optional Fields


دارای پاداش پایه یکسان هستند.


Base Reward:

10 XP


فرمول:

Reward Base = 10 XP


---

# 19. Optional Field Difficulty Reward

فقط Fieldهای اختیاری دارای پاداش سختی هستند.


سطوح سختی:

## Easy

Difficulty Reward:

+25 XP


## Medium

Difficulty Reward:

+30 XP


## Hard

Difficulty Reward:

+35 XP


---

# 20. Final Field Reward Formula


## Mandatory Field

Final Reward:

10 XP


---

## Optional Field

Final Reward:

Base Reward + Difficulty Reward


مثال:

Optional Field - Hard


10 XP

+

35 XP


=

45 XP


---

# 21. Reward Philosophy

هدف این مدل:

1. ارزش‌گذاری تمام مشارکت‌ها.
2. جلوگیری از بی‌ارزش شدن تکمیل آیتم‌های اجباری.
3. تشویق بیشتر برای تکمیل بخش‌های پیچیده‌تر دانش.
4. ایجاد رقابت سالم برای توسعه Knowledge Base.


---

# 22. Reward Ownership Rule

پاداش فقط به اولین مشارکت‌کننده‌ای تعلق می‌گیرد که آن Field را:

- تکمیل کند.
- اعتبارسنجی شود.
- Approved شود.


ویرایش‌های بعدی همان Field پاداش تکمیل اولیه ایجاد نمی‌کند.


---

# 23. Reward History

تمام Rewardها باید قابل ردیابی باشند.


هر Reward Event باید شامل:

- User ID
- Concept ID
- Field ID
- Reward Type
- Base Reward
- Difficulty Reward
- Multiplier
- Final Reward
- Timestamp
- Approval Reference


باشد.


---

# 24. Reward Security Rule

سیستم باید جلوگیری کند از:

- ثبت دوباره یک Field برای دریافت پاداش.
- تغییرات صوری برای دریافت Reward.
- حذف و ایجاد دوباره اطلاعات.
- تقسیم مصنوعی یک Contribution.


تمام رخدادها باید در History ثبت شوند.


---

# 25. Completion Incentive Multiplier System

هدف این سیستم:

ایجاد انگیزه قوی برای تکمیل Conceptهای ناقص موجود در Knowledge Base است.

با توجه به اینکه:

Mandatory Items = 30%

Optional Items = 70%


بخش اصلی رشد کیفیت دانش از طریق تکمیل آیتم‌های اختیاری انجام می‌شود.

بنابراین برای جلوگیری از کم‌رقبتی در تکمیل Conceptهای ناقص، ضریب تشویقی تعریف می‌شود.


---

# 26. Completion Percentage Reward Rule

ضریب تشویقی بر اساس درصد تکمیل Concept در زمان ورود کاربر به فرآیند Completion تعیین می‌شود.


جدول ضریب:

| Completion Entry Range | Reward Multiplier |
|---|---|
| 30% تا 40% | ×2 |
| 40% تا 50% | ×3 |
| 50% تا 60% | ×4 |
| 60% تا 70% | ×5 |
| 70% تا 80% | ×6 |
| 80% تا 90% | ×7 |
| 90% به بالا | ×8 |


---

# 27. Multiplier Calculation Example

مثال:

یک Concept با 70% تکمیل وارد Completion Queue شده است.

کاربری در این مرحله وارد تکمیل می‌شود.


ضریب کاربر:

×6


اگر این کاربر یک Optional Field با ارزش پایه:

45 XP


تکمیل کند:


45 × 6


=

270 XP


دریافت می‌کند.


---

# 28. Multiplier Ownership Rule

ضریب تشویقی متعلق به:

User + Concept


است.


یعنی:

هر کاربر برای هر Concept فقط یک بار ضریب دریافت می‌کند.


---

# 29. Multiplier Lock Rule

بعد از اولین ورود کاربر به Completion یک Concept:

ضریب او ثبت و قفل می‌شود.


مثال:

Concept در زمان ورود:

75%


کاربر دریافت می‌کند:

×6


بعد از مدتی Concept به:

85%


رسیده است.


همان کاربر همچنان:

×6


دارد.


ضریب جدید محاسبه نمی‌شود.


---

# 30. First Contributor Exception

کاربری که Concept را از ابتدا ایجاد کرده است:

تا زمانی که همان Concept را تکمیل می‌کند:

ضریب Completion دریافت نمی‌کند.


دلیل:

او مالک اولیه ایجاد Concept است و سیستم برای جذب مشارکت‌کنندگان جدید طراحی شده است.


---

# 31. New Contributor Rule

اگر کاربر جدید در هر مرحله وارد Completion شود:

ضریب مرحله ورود او ثبت می‌شود.


مثال:

Concept:

70%


کاربر جدید وارد می‌شود.


Multiplier:

×6


حتی اگر تکمیل نهایی Concept چند ماه طول بکشد، ضریب او ثابت باقی می‌ماند.


---

# 32. Anti Abuse Rule

کاربر نمی‌تواند:

- خروج و ورود مجدد برای گرفتن ضریب بهتر انجام دهد.
- وضعیت Concept را تغییر دهد تا Multiplier جدید بگیرد.
- یک Contribution را چند بار ثبت کند.


تمام ثبت‌ها باید از طریق Reward History قابل بررسی باشند.


---

# 33. Database Requirements

برای پشتیبانی از معماری جدید Reward و Completion، سیستم داده باید اطلاعات زیر را نگهداری کند.


---

# 34. Concept Completion Data

هر Concept باید دارای اطلاعات زیر باشد:


## Completeness

درصد تکمیل Concept.


Example:

0 - 100


---

## Completion Status

وضعیت تکمیل:


- INCOMPLETE
- IN_PROGRESS
- COMPLETE
- PUBLISHED


---

## Completion History

تاریخچه تمام تغییرات:


شامل:

- Field Added
- Contributor
- Timestamp
- Previous Value
- New Value
- Approval Result


---

# 35. User Concept Multiplier Storage

برای جلوگیری از سوءاستفاده، ضریب هر کاربر باید ذخیره شود.


ساختار منطقی:


User Concept Completion Record:


- user_id
- concept_id
- entry_completion_percentage
- assigned_multiplier
- assigned_at
- status


---

# 36. Reward Log Extension

هر Reward باید قابلیت بازسازی داشته باشد.


حداقل داده‌ها:


- reward_id
- user_id
- concept_id
- field_id
- base_reward
- difficulty_reward
- multiplier
- final_reward
- approval_status
- created_at


---

# 37. EventBus Integration

تمام تغییرات مهم باید Event ایجاد کنند.


---

## Concept Completion Events


### COMPLETION_STARTED

زمانی که یک کاربر برای تکمیل Concept وارد می‌شود.


Payload:

- user_id
- concept_id
- current_completeness
- assigned_multiplier


---

### FIELD_COMPLETED

زمانی که یک Field تکمیل می‌شود.


Payload:

- concept_id
- field_id
- contributor
- field_type
- difficulty


---

### FIELD_APPROVED

زمان تأیید Field.


Payload:

- field_id
- reviewer
- approval_time


---

### REWARD_GRANTED

ثبت پرداخت Reward.


Payload:

- user_id
- concept_id
- field_id
- multiplier
- final_reward


---

# 38. Audit Requirements

تمام عملیات Knowledge Completion باید Audit شوند.


موارد Audit:


- چه کسی؟
- چه Fieldای؟
- چه زمانی؟
- چه تغییری؟
- چه Rewardای؟
- با چه ضریبی؟


---

# 39. Migration From Previous Snapshots

این Snapshot جایگزین بخش‌های Reward در اسناد قبلی می‌شود.


موارد نیازمند اصلاح:


## SNAPSHOT_KNOWLEDGE_INJECTION_ARCHITECTURE_v1.1


تغییر:

مدل Reward قبلی:


Optional Field:

25-35 XP


به:


Base Reward + Difficulty Reward + Multiplier


---

## SNAPSHOT_KNOWLEDGE_CONCEPT_ARCHITECTURE_v1.0


تغییر:

سیستم امتیازدهی قدیمی باید با مدل جدید Field Reward هماهنگ شود.


---

## SNAPSHOT_KNOWLEDGE_COMPLETION_ENGINE_v1.0


تغییر:

Completion Multiplier و Ownership Rule باید اضافه شود.


---

# 40. Backward Compatibility Rule

اطلاعات قبلی حذف نمی‌شوند.


تاریخچه Rewardهای قدیمی:

- حفظ می‌شوند.
- قابل مشاهده هستند.
- فقط مدل جدید برای Contributionهای آینده اعمال می‌شود.


---

# 41. Final Locked Decisions

این بخش شامل تصمیم‌هایی است که در معماری Knowledge Lifecycle و Reward نهایی شده‌اند.


---

# KD-LR-001
## Concept Existence Rule

Concept فقط زمانی معتبر است که:

- تمام Mandatory Fields را داشته باشد.
- Validation اولیه را عبور کرده باشد.
- Approval Governance را دریافت کرده باشد.


Concept ناقص در مرحله ایجاد، وارد اکوسیستم فعال نمی‌شود.


---

# KD-LR-002
## Completion Separation Rule

تکمیل دانش فرآیندی جدا از ایجاد Concept است.


Creation:

ساخت پایه دانش


Completion:

افزایش کیفیت و کامل‌سازی دانش


---

# KD-LR-003
## Field Based Reward Rule

Reward بر اساس Field پرداخت می‌شود، نه صرفاً Concept.


هر Field یک Contribution مستقل محسوب می‌شود.


---

# KD-LR-004
## New Reward Formula Rule

تمام Fieldها:

Base Reward:

10 XP


فقط Optional Fieldها:

Difficulty Reward:

+25 / +30 / +35 XP


فرمول:


Mandatory Field:

10 XP


Optional Field:

10 XP + Difficulty Reward


---

# KD-LR-005
## Completion Incentive Rule

برای تشویق تکمیل Conceptهای ناقص:


30-40%:

×2


40-50%:

×3


50-60%:

×4


60-70%:

×5


70-80%:

×6


80-90%:

×7


90%+:

×8


---

# KD-LR-006
## Multiplier Ownership Rule

ضریب متعلق به:

User + Concept


است.


هر کاربر برای هر Concept فقط یک بار ضریب دریافت می‌کند.


---

# KD-LR-007
## Multiplier Lock Rule

ضریب در اولین ورود کاربر ثبت می‌شود.

افزایش درصد تکمیل Concept باعث تغییر ضریب همان کاربر نمی‌شود.


---

# KD-LR-008
## Creator Exception Rule

ایجادکننده اولیه Concept:

برای تکمیل همان Concept:

Completion Multiplier دریافت نمی‌کند.


هدف:

ایجاد انگیزه برای ورود مشارکت‌کنندگان جدید.


---

# KD-LR-009
## No Duplicate Reward Rule

هیچ Field نباید بیشتر از یک بار برای یک کاربر Reward ایجاد کند.


ویرایش یا ثبت دوباره:

Reward جدید ایجاد نمی‌کند.


---

# KD-LR-010
## Full Traceability Rule

تمام تغییرات Knowledge باید قابل ردیابی باشند.


هیچ داده‌ای حذف نمی‌شود.


---

# 42. Development Continuation Reference

در ادامه توسعه، این Snapshot مرجع تصمیم‌گیری برای:


- Knowledge Injection Engine
- Knowledge Completion Engine
- Reward Engine
- XP Integration
- EventBus Integration
- Database Migration


خواهد بود.


هر توسعه جدید باید با قوانین این سند سازگار باشد.


---

# 43. Architecture Status

Status:

LOCKED


Version:

1.0


Next Changes:

فقط از طریق Snapshot Version جدید.


END OF DOCUMENT
