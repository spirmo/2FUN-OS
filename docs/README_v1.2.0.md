# 2FUN_GAME
## Colony Governance Core

**Current Stable Version: v1.1.0**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-locked-success)
![Python](https://img.shields.io/badge/python-3.x-yellow)

🚀 **Core v1.0 – Colony Governance Locked**  
سیستم مدیریت کلونی‌ها، تخلفات، ارتقاء کاربران و رأی‌گیری ارکان کلونی.

---

## 📌 درباره پروژه

2FUN_GAME یک هسته مدیریت کلونی است که شامل موارد زیر است:

- مدیریت کلونی‌ها و گروه کلونی
- ثبت تخلفات و تشویق کاربران
- سیستم ارتقاء مرحله‌ای و شرطی کاربران
- رأی‌گیری ارکان کلونی
- قوانین ویژه برای اخراج خودکار و دستی کاربران

---

## 🧠 معماری کامل سیستم

مستند کامل فنی، ساختار دیتابیس و قوانین دقیق در فایل زیر قرار دارد:

👉 [`CORE_ARCHITECTURE.md`](CORE_ARCHITECTURE.md)

---

## ⚙️ نصب و اجرا

### 1️⃣ کلون کردن پروژه
```bash
git clone https://github.com/spirmo/2FUN_GAME.git
cd 2FUN_GAME
```

### 2️⃣ نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 3️⃣ اجرای مهاجرت‌ها و ایجاد دیتابیس
```bash
python3 -m app.migrations
```

### 4️⃣ اجرای تست قوانین کلونی
```bash
python3 -m app.test_colony_rules
```

### 5️⃣ اجرای سیستم رنک و ارتقاء
```bash
python3 -m app.rank_scheduler
```

---

## 🗄️ تکنولوژی‌ها

- Python 3
- SQLite
- Structured Colony Governance Engine

---

## 🔐 نسخه

- **Core v1.0**  
  این نسخه قفل شده و تغییرات اصلی در آن اعمال نمی‌شود.  
  توسعه‌های بعدی در نسخه‌های جدید ثبت خواهند شد.

---

## 📬 پشتیبانی

در صورت وجود مشکل یا پیشنهاد، از طریق بخش **Issues** در GitHub اقدام کنید:  
[2FUN_GAME Issues](https://github.com/spirmo/2FUN_GAME/issues)
