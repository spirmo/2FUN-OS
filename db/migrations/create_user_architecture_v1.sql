-- ======================================================
-- 2FUN / TANDIL GOVERNANCE SYSTEM
-- DATABASE IMPLEMENTATION v1
-- ======================================================

-- MASTER RULE:
-- All tables link via user_code

-- ======================================================
-- TABLE: users_identity
-- ======================================================

CREATE TABLE IF NOT EXISTS users_identity (
user_code TEXT PRIMARY KEY,

first_name TEXT,
last_name TEXT,
mobile TEXT,
email TEXT,
country TEXT,
province TEXT,
county TEXT,
city TEXT,
verification_level INTEGER DEFAULT 0,
identity_status TEXT DEFAULT 'UNVERIFIED',

reserved01 TEXT,
reserved02 TEXT,
reserved03 TEXT,
reserved04 TEXT,
reserved05 TEXT,
reserved06 TEXT,
reserved07 TEXT,
reserved08 TEXT,
reserved09 TEXT,
reserved10 TEXT,
reserved11 TEXT,
reserved12 TEXT,
reserved13 TEXT,
reserved14 TEXT,
reserved15 TEXT,
reserved16 TEXT,
reserved17 TEXT,
reserved18 TEXT,
reserved19 TEXT,
reserved20 TEXT

);

-- ======================================================
-- TABLE: users_public
-- ======================================================

CREATE TABLE IF NOT EXISTS users_public (
user_code TEXT PRIMARY KEY,

rank TEXT,
colony_rank TEXT,
activity_level INTEGER DEFAULT 0,
contribution_score INTEGER DEFAULT 0,
social_reputation REAL DEFAULT 0,
badges TEXT,
achievements TEXT,
join_date DATETIME,

reserved01 TEXT,
reserved02 TEXT,
reserved03 TEXT,
reserved04 TEXT,
reserved05 TEXT,
reserved06 TEXT,
reserved07 TEXT,
reserved08 TEXT,
reserved09 TEXT,
reserved10 TEXT,
reserved11 TEXT,
reserved12 TEXT,
reserved13 TEXT,
reserved14 TEXT,
reserved15 TEXT

);

-- ======================================================
-- TABLE: users_governance
-- ======================================================

CREATE TABLE IF NOT EXISTS users_governance (
user_code TEXT PRIMARY KEY,

trust_index REAL DEFAULT 0,
risk_index REAL DEFAULT 0,
stability_index REAL DEFAULT 0,
governance_score REAL DEFAULT 0,
discipline_status TEXT,
violation_history INTEGER DEFAULT 0,
loyalty_index REAL DEFAULT 0,
retention_probability REAL DEFAULT 0,
long_term_participation REAL DEFAULT 0,

reserved01 TEXT,
reserved02 TEXT,
reserved03 TEXT,
reserved04 TEXT,
reserved05 TEXT,
reserved06 TEXT,
reserved07 TEXT,
reserved08 TEXT,
reserved09 TEXT,
reserved10 TEXT,
reserved11 TEXT,
reserved12 TEXT,
reserved13 TEXT,
reserved14 TEXT,
reserved15 TEXT

);

-- ======================================================
-- TABLE: users_hidden
-- ======================================================

CREATE TABLE IF NOT EXISTS users_hidden (
user_code TEXT PRIMARY KEY,

financial_intelligence REAL DEFAULT 0,
technical_skill REAL DEFAULT 0,
leadership REAL DEFAULT 0,
networking_power REAL DEFAULT 0,
decision_power REAL DEFAULT 0,
crisis_management REAL DEFAULT 0,
learning_index REAL DEFAULT 0,
innovation_index REAL DEFAULT 0,
influence_index REAL DEFAULT 0,
behavior_pattern TEXT,

reserved01 TEXT,
reserved02 TEXT,
reserved03 TEXT,
reserved04 TEXT,
reserved05 TEXT,
reserved06 TEXT,
reserved07 TEXT,
reserved08 TEXT,
reserved09 TEXT,
reserved10 TEXT,
reserved11 TEXT,
reserved12 TEXT,
reserved13 TEXT,
reserved14 TEXT,
reserved15 TEXT

);

-- ======================================================
-- TABLE: users_position
-- ======================================================

CREATE TABLE IF NOT EXISTS users_position (
user_code TEXT PRIMARY KEY,

member_status TEXT,
contributor_status TEXT,
senior_contributor_status TEXT,
colony_leader_status TEXT,
governance_council_status TEXT,
founder_status TEXT,

reserved01 TEXT,
reserved02 TEXT,
reserved03 TEXT,
reserved04 TEXT,
reserved05 TEXT,
reserved06 TEXT,
reserved07 TEXT,
reserved08 TEXT,
reserved09 TEXT,
reserved10 TEXT

);

-- ======================================================
-- INDEX RULE (optional optimization)
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_identity_user_code
ON users_identity(user_code);

CREATE INDEX IF NOT EXISTS idx_public_user_code
ON users_public(user_code);

CREATE INDEX IF NOT EXISTS idx_governance_user_code
ON users_governance(user_code);

CREATE INDEX IF NOT EXISTS idx_hidden_user_code
ON users_hidden(user_code);

CREATE INDEX IF NOT EXISTS idx_position_user_code
ON users_position(user_code);

-- ======================================================
-- END OF IMPLEMENTATION v1
-- ======================================================
