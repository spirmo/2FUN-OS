# ARCHITECTURE SNAPSHOT
## Dynamic POINT Reward Law — قانون پویای پاداش POINT

Status: LOCKED ARCHITECTURAL DECISION
Domain: 2FUN Blockchain Economy / Reward System / Token Mining
Snapshot Name: SNAPSHOT_2FUNC_PRICE_ADJUSTED_POINT_REWARD.md

---

## 1. اصل بنیادین

در 2FUN، مقدار POINT پایه برای هر عملکرد (Operation / Activity) از قبل در سیستم تعریف می‌شود.

این مقدار پایه حذف یا بازتعریف نمی‌شود.

با تغییر ارزش 2FUNC، مقدار POINT پرداخت‌شده برای همان عملکرد به‌صورت پویا تعدیل می‌شود تا ارزش اقتصادی نسبی آن عملکرد در زمان‌های مختلف تا حد امکان پایدار باقی بماند.

اصل:

نوع و ارزش پایه عملکرد ثابت است؛
مقدار POINT پرداختی متغیر است.

---

## 2. سلسله‌مراتب واحدهای ارزش

ساختار واحدهای اقتصادی:

1 SHIR = 1,000 POINT
1 ΣSHIR = 10 SHIR = 10,000 POINT
1 2FUNC = 2 ΣSHIR = 20 SHIR = 20,000 POINT

بنابراین:

1 2FUNC = 20,000 POINT

این نسبت، قانون تبدیل واحدها است و مستقل از قیمت بازار 2FUNC می‌باشد.

---

## 3. Reward Base

برای هر عملکرد یک مقدار پایه از پیش تعریف می‌شود:

RewardBase(operation)

مثال:

Operation A → 40 POINT
Operation B → 100 POINT
Operation C → 250 POINT
Operation D → 1,000 POINT

اعداد فوق صرفاً نمونه هستند.

هر Operation می‌تواند Reward Base مستقل خود را داشته باشد.

---

## 4. قانون تعدیل قیمت

مقدار واقعی POINT قابل دریافت از رابطه زیر محاسبه می‌شود:

DynamicReward =
    RewardBase × ReferencePriceAtBase / CurrentReferencePrice

یا:

R = B × P₀ / Pₜ

تعریف متغیرها:

R  = مقدار نهایی POINT پاداش
B  = Reward Base عملکرد
P₀ = قیمت مرجع 2FUNC در مبنای تعریف Reward Base
Pₜ = قیمت مرجع فعلی 2FUNC در زمان محاسبه پاداش

---

## 5. رفتار سیستم در تغییر قیمت

با افزایش قیمت 2FUNC، مقدار POINT پاداش همان عملکرد کاهش می‌یابد.

مثال:

RewardBase = 40 POINT
Reference Price = $2

قیمت 2FUNC    Reward
$1            80 POINT
$2            40 POINT
$4            20 POINT
$10           8 POINT
$20           4 POINT
$100          0.8 POINT

بنابراین:

2FUNC Price ↑ → POINT Reward ↓

و:

2FUNC Price ↓ → POINT Reward ↑

---

## 6. هدف اقتصادی

هدف این قانون آن است که ارزش اقتصادی نسبی یک فعالیت، صرفاً به دلیل تغییر قیمت 2FUNC دچار تغییر شدید نشود.

این مکانیزم:

1. Reward Base عملکردها را ثابت نگه می‌دارد.
2. با افزایش ارزش 2FUNC، نرخ انتشار POINT را کاهش می‌دهد.
3. با کاهش ارزش 2FUNC، امکان افزایش POINT Reward را فراهم می‌کند.
4. مانع از افزایش خودکار Reward صرفاً به دلیل افزایش قیمت 2FUNC می‌شود.
5. به مشارکت‌کنندگان اولیه در دوره ارزش پایین‌تر 2FUNC مزیت طبیعی می‌دهد.
6. نرخ انتشار POINT را با رشد ارزش اقتصادی اکوسیستم هماهنگ می‌کند.

---

## 7. رابطه با Mining

تمام ایجاد POINT جدید باید از طریق فعالیت و عملکرد معتبر در اکوسیستم انجام شود.

POINT نباید بدون یک فعالیت معتبر و قابل اثبات ایجاد شود.

مسیر اقتصادی:

USER ACTIVITY
      ↓
VALIDATED OPERATION
      ↓
REWARD BASE
      ↓
PRICE ADJUSTMENT
      ↓
DYNAMIC POINT REWARD
      ↓
POINT ACCUMULATION
      ↓
SHIR / ΣSHIR / 2FUNC

اصل:

فعالیت واقعی → کسب POINT → حرکت به واحدهای ارزش بالاتر

---

## 8. مزیت مشارکت اولیه

وقتی قیمت 2FUNC پایین‌تر است، یک عملکرد مشخص POINT بیشتری ایجاد می‌کند.

با افزایش قیمت 2FUNC، همان عملکرد POINT کمتری ایجاد می‌کند.

بنابراین مشارکت‌کننده‌ای که در مراحل اولیه و در قیمت پایین‌تر فعالیت کرده است، برای عملکرد برابر می‌تواند POINT بیشتری به دست آورده باشد.

این اثر با اصل:

Early Contribution Advantage

سازگار است.

هدف این است که مشارکت اولیه و کمک به شکل‌گیری و تثبیت اکوسیستم، در آینده بی‌ارزش نشود.

---

## 9. ثابت بودن Reward Base

قیمت 2FUNC نباید باعث تغییر مستقیم Reward Base شود.

مثال:

Operation A
RewardBase = 40 POINT

این مقدار همچنان 40 POINT باقی می‌ماند.

فقط Dynamic Reward بر اساس قیمت مرجع تغییر می‌کند.

بنابراین:

Reward Definition ≠ Market Price

و:

Reward Definition
+
Price Adjustment
=
Actual Reward

---

## 10. قیمت مرجع

سیستم نباید الزاماً از قیمت لحظه‌ای یک بازار واحد برای محاسبه Reward استفاده کند.

قیمت مورد استفاده باید:

Reference Price

باشد.

Reference Price می‌تواند بر اساس یکی از مکانیزم‌های معتبر زیر تعیین شود:

- Oracle
- TWAP (Time-Weighted Average Price)
- Epoch-Based Price
- یا ترکیب چند منبع معتبر

هدف:

نوسان لحظه‌ای یا دستکاری کوتاه‌مدت بازار نباید باعث تغییر غیرطبیعی Reward شود.

---

## 11. عدم تضمین قیمت دلاری

این قانون قیمت دلاری 2FUNC را تضمین نمی‌کند.

قانون فقط رابطه داخلی بین:

2FUNC
ΣSHIR
SHIR
POINT

و نحوه محاسبه Reward را تعریف می‌کند.

بنابراین:

Market Price ≠ Guaranteed Price

قیمت واقعی 2FUNC تابع بازار، عرضه، تقاضا، نقدینگی و سایر عوامل اقتصادی خواهد بود.

Dynamic Reward فقط مقدار POINT تولیدشده را نسبت به قیمت مرجع تنظیم می‌کند.

---

## 12. حفظ Denomination Law

Dynamic Reward نباید نسبت واحدهای اقتصادی زیر را تغییر دهد:

1 SHIR  = 1,000 POINT
1 ΣSHIR = 10 SHIR
1 ΣSHIR = 10,000 POINT
1 2FUNC = 2 ΣSHIR
1 2FUNC = 20 SHIR
1 2FUNC = 20,000 POINT

این نسبت‌ها:

Denomination Law

هستند.

Dynamic Reward فقط تعیین می‌کند برای انجام یک عملکرد معتبر، چه مقدار POINT جدید به کاربر اختصاص داده شود.

---

## 13. عدم ایجاد توکن از طریق افزایش قیمت

افزایش قیمت 2FUNC نباید به‌تنهایی باعث ایجاد 2FUNC جدید شود.

Price ↑

به معنی:

Token Supply ↑

نیست.

ایجاد واحدهای اقتصادی جدید باید از مسیر فعالیت، کسب POINT و قوانین رسمی Emission/Mining انجام شود.

---

## 14. اصل کنترل انتشار

با افزایش ارزش 2FUNC:

2FUNC Price ↑
        ↓
POINT Reward per Operation ↓
        ↓
POINT Emission Rate ↓

این مکانیزم یک کنترل طبیعی برای کاهش نرخ انتشار Reward در زمان رشد ارزش اکوسیستم ایجاد می‌کند.

---

## 15. ثبت تاریخی Reward

Rewardهای قبلی نباید با تغییر قیمت‌های آینده بازنویسی شوند.

هر Reward باید بر اساس پارامترهای معتبر در زمان انجام فعالیت ثبت شود.

بنابراین:

Past Reward = Immutable Historical Record

تغییرات آینده فقط روی عملیات جدید اثر می‌گذارد.

---

## 16. قابلیت بازتولید و حسابرسی

هر Reward باید قابل پاسخ به این سؤال باشد:

«چرا این کاربر در این زمان این مقدار POINT دریافت کرده است؟»

حداقل داده‌های مورد نیاز برای Audit:

operation_id
user_id
reward_base
reference_price
price_timestamp / epoch
price_source
adjustment_factor
calculated_reward
rounding_rule
final_reward

محاسبه باید قابل بازتولید باشد:

RewardBase
+
Reference Price
+
Price Epoch
+
Formula
=
Final Reward

---

## 17. دقت محاسبات

محاسبات Reward باید دارای قوانین صریح برای:

- Precision
- Decimal Handling
- Rounding
- Minimum Reward
- Maximum Reward در صورت نیاز

باشد.

سیستم نباید به دلیل خطاهای اعشاری یا Rounding باعث ایجاد اختلاف اقتصادی قابل توجه شود.

---

## 18. حاکمیت

پارامترهای زیر باید تحت Governance و Rule Engine کنترل شوند:

- Reward Base
- Reference Price Mechanism
- Price Source
- Formula
- Precision
- Rounding
- Minimum Reward
- Maximum Reward
- Emission Limits

AI صرفاً نقش Advisory دارد.

AI = Advisory Only
Rule Engine = Final Authority

---

## 19. عدم بازنویسی گذشته

تغییر Rule در آینده نباید سوابق قبلی را تغییر دهد.

در صورت تغییر رسمی پارامترها:

Old Rewards
→ حفظ می‌شوند.

New Parameters
→ فقط برای عملیات جدید اعمال می‌شوند.

هر تغییر بنیادی باید به‌صورت Versioned Rule / Architecture Snapshot ثبت شود.

---

## 20. مثال کامل

فرض:

Operation X
RewardBase = 40 POINT
Reference Price at Base = $2

در قیمت $2:

R = 40 × 2 / 2
R = 40 POINT

در قیمت $4:

R = 40 × 2 / 4
R = 20 POINT

در قیمت $10:

R = 40 × 2 / 10
R = 8 POINT

در قیمت $100:

R = 40 × 2 / 100
R = 0.8 POINT

عملکرد هر چهار مورد یکسان است؛
Reward Base یکسان است؛
تنها قیمت مرجع 2FUNC تغییر کرده است.

---

# LOCKED ARCHITECTURAL PRINCIPLE

برای هر عملکرد، Reward Base ثابت و از پیش تعریف‌شده است. مقدار POINT واقعی پرداخت‌شده با استفاده از قیمت مرجع 2FUNC به‌صورت معکوس تعدیل می‌شود.

با افزایش ارزش 2FUNC، مقدار POINT موردنیاز برای همان عملکرد کاهش می‌یابد و با کاهش ارزش 2FUNC، مقدار POINT افزایش می‌یابد.

Rewardهای گذشته هرگز بازنویسی نمی‌شوند.

تمام POINTهای جدید باید از فعالیت‌های معتبر، قابل اثبات و قابل حسابرسی ایجاد شوند.

قیمت بازار 2FUNC توسط این قانون تضمین نمی‌شود.

فرمول مرجع:

DynamicReward =
    RewardBase × ReferencePriceAtBase / CurrentReferencePrice

سلسله‌مراتب واحدها:

1 SHIR  = 1,000 POINT
1 ΣSHIR = 10 SHIR
1 ΣSHIR = 10,000 POINT
1 2FUNC = 2 ΣSHIR
1 2FUNC = 20 SHIR
1 2FUNC = 20,000 POINT

این Snapshot به‌عنوان قانون اقتصادی پایه Dynamic POINT Reward در معماری 2FUN ثبت می‌شود.

هر تغییر آینده باید به‌صورت نسخه جدید Architecture Snapshot ثبت شود و نباید با تغییر خاموش این قانون انجام شود.

---

Snapshot Path:

2FUN_BLOCKCHAIN_ECONOMY/
└── SNAPSHOT_2FUNC_PRICE_ADJUSTED_POINT_REWARD.md
