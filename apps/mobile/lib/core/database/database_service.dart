import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

class DatabaseService {
  DatabaseService._();

  static final DatabaseService instance = DatabaseService._();

  Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;

    _database = await _initDatabase();

    return _database!;
  }

  Future<Database> _initDatabase() async {
    final databasesPath = await getDatabasesPath();

    final path = join(
      databasesPath,
      'twofun.db',
    );

    return await openDatabase(
      path,
      version: 6,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
      onOpen: _onOpen,
    );
  }

  Future<void> _onCreate(
    Database db,
    int version,
  ) async {

    await db.execute('''
CREATE TABLE domains(
id INTEGER PRIMARY KEY AUTOINCREMENT,
code TEXT UNIQUE NOT NULL,
name_fa TEXT NOT NULL,
name_en TEXT NOT NULL,
name_ar TEXT NOT NULL,
description TEXT,
status TEXT NOT NULL DEFAULT 'APPROVED',
created_at TEXT
)
''');

    await db.execute('''
CREATE TABLE topics(
id INTEGER PRIMARY KEY AUTOINCREMENT,
domain_id INTEGER NOT NULL,
code TEXT,
name_fa TEXT NOT NULL,
name_en TEXT NOT NULL,
name_ar TEXT NOT NULL,
description TEXT,
status TEXT NOT NULL DEFAULT 'PENDING',
created_at TEXT
)
''');

    await db.execute('''
CREATE TABLE concepts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
topic_id INTEGER NOT NULL,
code TEXT,
name_fa TEXT NOT NULL,
name_en TEXT NOT NULL,
name_ar TEXT NOT NULL,
description TEXT,
status TEXT NOT NULL DEFAULT 'PENDING',
created_at TEXT
)
''');

    await db.execute('''
CREATE TABLE attributes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
concept_id INTEGER NOT NULL,
name_fa TEXT,
name_en TEXT,
name_ar TEXT,
value TEXT,
status TEXT NOT NULL DEFAULT 'PENDING'
)
''');

    await db.execute('''
CREATE TABLE sources(
id INTEGER PRIMARY KEY AUTOINCREMENT,
concept_id INTEGER NOT NULL,
title TEXT,
url TEXT,
author TEXT,
year TEXT
)
''');

    await db.execute('''
CREATE TABLE translations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
concept_id INTEGER NOT NULL,
language TEXT,
translated_text TEXT
)
''');

    await db.execute('''
CREATE TABLE questions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
concept_id INTEGER NOT NULL,
question TEXT,
answer TEXT
)
''');

    await db.execute('''
CREATE TABLE missions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
concept_id INTEGER,
title TEXT,
description TEXT,
status TEXT DEFAULT 'PENDING'
)
''');

    await _seedDomains(db);
  }

  Future<void> _onUpgrade(
    Database db,
    int oldVersion,
    int newVersion,
  ) async {

    if (oldVersion < 2) {
      await db.execute(
        "ALTER TABLE domains ADD COLUMN status TEXT NOT NULL DEFAULT 'APPROVED';",
      );
    }

    if (oldVersion < 3) {
      await _seedDomains(db);
    }

    if (oldVersion < 4) {
  await _onCreate(db, 4);
}

    if (oldVersion < 5) {
  await _upgradeConceptArchitecture(db);
  }
        if (oldVersion < 6) {
      await _upgradeConceptReserveFields(db);
  }

  Future<void> _onOpen(Database db) async {
    Future<void> _onOpen(Database db) async {
    await _seedDomains(db);
  }

  Future<void> _seedDomains(Database db) async {

    final result = await db.rawQuery(
      'SELECT COUNT(*) AS c FROM domains',
    );

    final count = result.first['c'] as int;

    if (count > 0) return;

    final items = [
      {
        "code": "IE",
        "fa": "آموزش اسلامی",
        "en": "Islamic Education",
        "ar": "التعليم الإسلامي",
      },
      {
        "code": "IC",
        "fa": "فرهنگ اسلامی",
        "en": "Islamic Culture",
        "ar": "الثقافة الإسلامية",
      },
      {
        "code": "IEC",
        "fa": "اقتصاد اسلامی",
        "en": "Islamic Economics",
        "ar": "الاقتصاد الإسلامي",
      },
      {
        "code": "AI",
        "fa": "ایران باستان",
        "en": "Ancient Iran",
        "ar": "إيران القديمة",
      },
      {
        "code": "SN",
        "fa": "جامعه‌شناسی ملت‌ها",
        "en": "Sociology of Nations",
        "ar": "علم اجتماع الأمم",
      },
      {
        "code": "GK",
        "fa": "دانش عمومی",
        "en": "General Knowledge",
        "ar": "المعرفة العامة",
      },
      {
        "code": "2FUN",
        "fa": "پلتفرم توفان",
        "en": "2FUN Platform",
        "ar": "منصة توفان",
      },
    ];

    final batch = db.batch();

    for (final d in items) {
      batch.insert(
        "domains",
        {
          "code": d["code"],
          "name_fa": d["fa"],
          "name_en": d["en"],
          "name_ar": d["ar"],
          "status": "APPROVED",
        },
        conflictAlgorithm: ConflictAlgorithm.ignore,
      );
    }

    await batch.commit(noResult: true);
  }

  Future<void> insertTopic({
    required int domainId,
    required String fa,
    required String en,
    required String ar,
  }) async {

    final db = await database;

    await db.insert(
      'topics',
      {
        'domain_id': domainId,
        'name_fa': fa,
        'name_en': en,
        'name_ar': ar,
        'status': 'PENDING',
        'created_at': DateTime.now().toIso8601String(),
      },
    );
  }
  Future<void> insertConcept({
    required int topicId,
    required String fa,
    required String en,
    required String ar,
    String? description,
  }) async {

    final db = await database;

    await db.insert(
      'concepts',
      {
        'topic_id': topicId,
        'name_fa': fa,
        'name_en': en,
        'name_ar': ar,
        'description': description ?? '',
        'status': 'PENDING',
        'created_at': DateTime.now().toIso8601String(),
      },
    );
  }

  Future<void> _upgradeConceptArchitecture(Database db) async {

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN category TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN canonical_meaning TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN short_description TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN primary_source TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reference_location TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN evidence TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN completeness INTEGER DEFAULT 0
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN version TEXT DEFAULT '1.0'
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN snapshot_reference TEXT
''');
}
Future<void> _upgradeConceptReserveFields(Database db) async {

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_01 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_02 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_03 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_04 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_05 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_06 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_07 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_08 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_09 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_10 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_11 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_12 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_13 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_14 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_15 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_16 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_17 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_18 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_19 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_20 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_21 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_22 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_23 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_24 TEXT
''');

  await db.execute('''
ALTER TABLE concepts
ADD COLUMN reserve_25 TEXT
''');
}
}
