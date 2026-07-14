class Country {
  final int id;
  final String nameFa;
  final String nameEn;
  final String nameAr;
  final String language;
  final String flag;

  const Country({
    required this.id,
    required this.nameFa,
    required this.nameEn,
    required this.nameAr,
    required this.language,
    required this.flag,
  });

  factory Country.fromJson(Map<String, dynamic> json) {
    return Country(
      id: json["id"],
      nameFa: json["name_fa"],
      nameEn: json["name_en"],
      nameAr: json["name_ar"],
      language: json["language"],
      flag: json["flag"],
    );
  }

  String name(String lang) {
    switch (lang) {
      case "fa":
        return nameFa;
      case "ar":
        return nameAr;
      default:
        return nameEn;
    }
  }
}
