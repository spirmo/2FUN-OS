import 'package:flutter/material.dart';

import '../../core/constants/app_assets.dart';

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
        logoWidth = 220;
        break;

      case AppLogoType.welcome:
        logoWidth = 150;
        break;

      case AppLogoType.login:
        logoWidth = 140;
        break;

      case AppLogoType.dashboard:
        logoWidth = 90;
        break;

      case AppLogoType.appBar:
        logoWidth = 42;
        break;

      case AppLogoType.normal:
        logoWidth = 180;
        break;
    }

    return Hero(
      tag: "twofun_logo",
      child: Image.asset(
        AppAssets.logo,
        width: width ?? logoWidth,
        height: height,
        fit: BoxFit.contain,
        filterQuality: FilterQuality.high,
      ),
    );
  }
}
