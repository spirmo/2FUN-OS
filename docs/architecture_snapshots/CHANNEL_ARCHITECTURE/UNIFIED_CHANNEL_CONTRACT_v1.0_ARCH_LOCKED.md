# 2FUN / توفان
# Unified Channel Contract
## قرارداد یکپارچه لایه کانال

**Version:** 1.0  
**Status:** ARCHITECTURE LOCKED  
**Scope:** Channel / Bot Architecture  
**Decision:** Multi-Channel

---

## 1. هدف

این سند قرارداد معماری یکپارچه برای اتصال کانال‌های
خارجی 2FUN به Platform API را تعریف می‌کند.

کانال‌های خارجی می‌توانند شامل موارد زیر باشند:

- Telegram
- Discord
- WhatsApp
- Web
- سایر کانال‌های آینده

افزودن یک کانال جدید نباید باعث ایجاد یا تکثیر Game Logic،
Knowledge Logic، Governance Logic یا Economy Logic شود.

---

## 2. معماری کلان

```text
External Channels
┌──────────┬──────────┬──────────┬──────────┐
│ Telegram │ Discord  │ WhatsApp │ Future   │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┘
     └──────────┴──────────┴──────────┘
                    │
                    ▼
              2FUN-BOT
            Channel Layer
                    │
                    ▼
        Unified Channel Contract
                    │
                    ▼
            2FUN Platform API
                    │
                    ▼
              2FUN-OS Runtime
                    │
                    ▼
                 EventBus
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Game      Knowledge   Governance
```

---

## 3. مالکیت

### 3.1 Channel

Telegram، Discord، WhatsApp و سایر کانال‌ها صرفاً Transport / Channel هستند.

Channel نباید مالک منطق Game یا منطق مرکزی 2FUN باشد.

### 3.2 2FUN-BOT

2FUN-BOT یک Multi-Channel Channel Layer مستقل است.

مسئولیت‌های آن:

- دریافت درخواست از Channel
- تبدیل ورودی Channel به Unified Channel Contract
- ارسال درخواست به Platform API
- دریافت پاسخ
- تبدیل پاسخ به فرمت مناسب Channel
- مدیریت Adapter مخصوص هر Channel

2FUN-BOT نباید منطق اصلی Game، Knowledge، Governance یا Economy را پیاده‌سازی کند.

### 3.3 Platform API

Platform API مرز مشترک ورود سرویس‌های خارجی به 2FUN-OS است.

Platform API نباید وابسته به یک Channel خاص باشد.

### 3.4 Game

Game Logic فقط در Game Module/Engine قرار دارد.

Channel Layer نباید Game Logic را بازتولید کند.

---

## 4. Unified Channel Request

قرارداد ورودی منطقی:

```text
ChannelRequest
├── channel
├── external_user
├── message
└── context
```

### channel

شناسه Channel حمل‌کننده درخواست.

نمونه:

```text
telegram
discord
whatsapp
web
```

### external_user

شناسه کاربر در Channel خارجی.

این شناسه با User ID اصلی 2FUN یکسان نیست.

تبدیل و نگاشت هویت باید از طریق معماری Identity انجام شود.

### message

محتوای درخواست کاربر.

این فیلد می‌تواند شامل متن، فرمان، ورودی ساختاریافته یا سایر داده‌های مجاز Channel باشد.

### context

اطلاعات جانبی موردنیاز برای پردازش درخواست، بدون انتقال منطق داخلی Game یا Engine به Channel Layer.

---

## 5. Unified Channel Response

قرارداد خروجی منطقی:

```text
ChannelResponse
├── status
├── response
├── events
└── metadata
```

### status

وضعیت پردازش درخواست.

### response

محتوای پاسخ قابل ارائه به Channel.

### events

رویدادهای مجاز خروجی در صورت نیاز.

Event ID و Trace Path توسط EventBus مدیریت می‌شوند.

### metadata

اطلاعات تکمیلی غیرمنطقی و غیرحاکمیتی موردنیاز Adapter.

---

## 6. مرز Game

Channel Request نباید مستقیماً به Game Action Engine به‌عنوان Decision وارد شود.

مسیر صحیح:

```text
Channel Request
      ↓
2FUN-BOT
      ↓
Platform API
      ↓
Game Boundary
      ↓
Game Entry
      ↓
Game Action Engine
```

Game Entry مسئول دریافت قرارداد داخلی Game است، نه Telegram/Discord/WhatsApp.

---

## 7. EventBus Boundary

Channel Layer مالک EventBus نیست.

Channel Layer نباید:

- Event ID تولید کند
- Trace Path تولید کند
- EventBus مستقل ایجاد کند
- EventBus داخلی برای هر Channel بسازد

مسیر صحیح:

```text
Channel
   ↓
2FUN-BOT
   ↓
Platform API
   ↓
2FUN-OS Runtime
   ↓
EventBus
```

EventBus متعلق به Runtime مرکزی 2FUN-OS است.

---

## 8. Source و Channel

channel مشخص می‌کند درخواست از کدام Transport آمده است.

نمونه:

```text
channel = telegram
```

اما این الزاماً به معنی آن نیست که Event Source مرکزی باید نام Telegram باشد.

Channel identity و Event source دو مفهوم معماری متفاوت هستند.

---

## 9. Identity Boundary

شناسه خارجی Channel:

```text
external_user
```

با شناسه اصلی 2FUN:

```text
2FUN User ID
```

متفاوت است.

Channel Layer نباید User ID اصلی را تولید یا تعیین کند.

Identity Authority مسئول نگاشت هویت است.

---

## 10. ممنوعیت‌های معماری

موارد زیر ممنوع هستند:

```text
Telegram Bot → Game Logic
Discord Bot → Game Logic
WhatsApp Bot → Game Logic

Telegram Bot → Database مستقیم
Discord Bot → Database مستقیم
WhatsApp Bot → Database مستقیم

Channel → EventBus مستقل

Channel → Governance مستقیم

Channel → Economy مستقیم

Channel → Knowledge مستقیم
```

تمام این مسیرها باید از Boundaryهای رسمی Platform عبور کنند.

---

## 11. اصل Single Game Logic

تمام Channelها باید از یک Game Logic مشترک استفاده کنند:

```text
Telegram ─┐
Discord  ─┤
WhatsApp ─┤
Web      ─┤
Future   ─┘
          ↓
     Unified Contract
          ↓
      Platform API
          ↓
       Game Entry
          ↓
     Game Logic
```

هیچ Channel مجاز به ایجاد نسخه مستقل Game نیست.

---

## 12. Extensibility

افزودن Channel جدید باید با افزودن Adapter جدید امکان‌پذیر باشد، بدون تغییر در منطق اصلی Game.

نمونه:

```text
TelegramAdapter
DiscordAdapter
WhatsAppAdapter
FutureChannelAdapter
```

همه باید به Unified Channel Contract متصل شوند.

---

## 13. استقلال مخازن

2FUN-BOT یک پروژه/Repository مستقل است.

این سند در 2FUN-OS فقط قرارداد معماری و Boundary را تثبیت می‌کند.

2FUN-OS نباید ساختار داخلی 2FUN-BOT را کپی کند.

2FUN-BOT نیز نباید Engineهای مرکزی 2FUN-OS را کپی کند.

---

## 14. اصل نهایی

```text
Channel = Transport
2FUN-BOT = Channel Layer
Platform API = Platform Boundary
2FUN-OS Runtime = Infrastructure Authority
EventBus = Central Event Authority
Game = Game Logic Authority
Identity = Identity Authority
Governance = Final Rule Authority
```

این قرارداد مبنای طراحی و پیاده‌سازی آینده Multi-Channel Architecture در اکوسیستم 2FUN است.

END OF LOCKED CONTRACT
