import 'package:flutter/material.dart';

enum AppLogoType {
  splash,
  welcome,
  login,
  dashboard,
  appBar,
  normal,
}

class AppLogo extends StatelessWidget {
  final double? width;
  final double? height;
  final AppLogoType type;

  const AppLogo({
    super.key,
    this.width,
    this.height,
    this.type = AppLogoType.normal,
  });

  @override
  Widget build(BuildContext context) {
    double logoWidth;

    switch (type) {
      case AppLogoType.splash:
        logoWidth = 230;
        break;

      case AppLogoType.welcome:
        logoWidth = 162;
        break;

      case AppLogoType.login:
        logoWidth = 195;
        break;

      case AppLogoType.dashboard:
        logoWidth = 128;
        break;

      case AppLogoType.appBar:
        logoWidth = 128;
        break;

      case AppLogoType.normal:
        logoWidth = 220;
        break;
    }

    return Hero(
      tag: "twofun_logo",
      child: Image.asset(
        'assets/images/logo/logo.png',
        width: width ?? logoWidth,
        height: height,
        fit: BoxFit.contain,
        filterQuality: FilterQuality.high,
        errorBuilder: (context, error, stackTrace) {
          return const Icon(
            Icons.error,
            color: Colors.red,
            size: 80,
          );
        },
      ),
    );
  }
}
