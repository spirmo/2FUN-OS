ARCHITECTURE RULE
ID: UI-001

Title:
Fixed Logo Layout Rule

Status:
LOCKED

Description:
تمام صفحات Super App باید از قالب مشترک صفحه استفاده کنند.
لوگوی 2FUN همیشه ثابت در بالای صفحه باقی می‌ماند.
هیچ متن، جدول، لیست، دکمه یا ویجتی مجاز نیست روی لوگو قرار بگیرد یا هنگام اسکرول از روی آن عبور کند.
تمام محتوای اسکرول‌شونده باید از زیر لوگو آغاز شود و حداقل به اندازه یک ارتفاع دکمه از لوگو فاصله داشته باشد.

Implementation:
تمام صفحات باید از ویجت پایه
TwoFunPage
(یا AppPageLayout)
استفاده کنند و ساخت مستقیم Scaffold برای صفحات جدید مجاز نیست.

Priority:
Mandatory

Applies To:
All current and future pages.
