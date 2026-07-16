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

  }
}
Future<void> _onOpen(Database db) async {
  await _seedDomains(db);
}
