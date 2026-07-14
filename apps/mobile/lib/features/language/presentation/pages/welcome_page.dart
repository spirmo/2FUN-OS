import 'package:flutter/material.dart';

import '../../../../shared/widgets/app_logo.dart';
import '../../../auth/presentation/pages/login_page.dart';

class WelcomePage extends StatelessWidget {
  const WelcomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        centerTitle: true,
        title: const Text(
          "2FUN",
          style: TextStyle(color: Colors.amber),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const AppLogo(width: 120),

            const SizedBox(height: 20),

            const Expanded(
              child: SingleChildScrollView(
                child: Text(
                  '''
«تمدن‌ها با قدرت ساخته نمی‌شوند؛ با دانشی که حفظ، تکمیل و به نسل‌های بعد منتقل می‌شود ساخته می‌شوند.»

به توفان (2FUN) خوش آمدید.

توفان تنها یک بازی یا یک سوپر اپلیکیشن نیست؛ بلکه اکوسیستمی برای ساخت، حفظ و گسترش دانش است. باور ما این است که ارزشمندترین میراث هر جامعه، دانش آن است؛ دانشی که اگر به‌درستی ثبت، سازمان‌دهی و منتقل نشود، به‌مرور زمان از بین خواهد رفت.

به همین دلیل از شما دعوت می‌کنیم تا در تولید، تکمیل، ترجمه، بررسی و اعتبارسنجی دانش مشارکت کنید. هر مشارکت ارزشمند، پس از بررسی و تأیید، بخشی از پایگاه دانش توفان خواهد شد و نام و نقش شما در این مسیر محفوظ می‌ماند.

برای قدردانی از این مشارکت، سامانه بر اساس کیفیت، دقت و میزان تأثیر هر فعالیت، امتیاز، اعتبار و پاداش اختصاص می‌دهد. این پاداش‌ها به‌تدریج در اکوسیستم توفان قابل استفاده خواهند بود و با رشد پروژه، ارزش و کاربرد بیشتری پیدا می‌کنند.

ما معتقدیم آینده را تنها با فناوری نمی‌توان ساخت؛ آینده با همکاری انسان‌هایی ساخته می‌شود که دانش خود را با دیگران به اشتراک می‌گذارند و برای ساختن جهانی آگاه‌تر، مسئولانه‌تر و عادلانه‌تر تلاش می‌کنند.

از اینکه بخشی از این مسیر هستید، سپاسگزاریم. شاید مشارکت امروز شما، دانشی باشد که فردا مسیر زندگی انسان دیگری را تغییر دهد.
''',
                  textAlign: TextAlign.justify,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    height: 1.7,
                  ),
                ),
              ),
            ),

            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const LoginPage(),
                    ),
                  );
                },
                child: const Text(
                  "شروع سفر",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 12),
          ],
        ),
      ),
    );
  }
}
