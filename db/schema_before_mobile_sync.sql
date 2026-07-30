CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE colony_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        , max_colonies INTEGER DEFAULT NULL);
CREATE TABLE "users" (
            id INTEGER NOT NULL PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            language VARCHAR,
            state VARCHAR,
            username TEXT,
            colony_id INTEGER,
            rank TEXT,
            stars INTEGER DEFAULT 0,
            credit INTEGER DEFAULT 100,
            violations INTEGER DEFAULT 0,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_code CHAR(35) UNIQUE,
            host_colonies TEXT DEFAULT NULL,
            role TEXT DEFAULT 'user',
            rank_step INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1, user_id TEXT, status TEXT DEFAULT 'ACTIVE', home_colony_id INTEGER, last_active DATETIME,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE SET NULL
        );
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_users_colony ON users(colony_id);
CREATE INDEX ix_users_rank ON users(rank);
CREATE UNIQUE INDEX ix_users_telegram_id ON users (telegram_id);
CREATE UNIQUE INDEX ix_users_user_code ON users (user_code);
CREATE TABLE "users_extension" (
            user_id INTEGER PRIMARY KEY,
            reserved1 TEXT,
            reserved2 TEXT,
            reserved3 TEXT,
            reserved4 TEXT,
            reserved5 TEXT,
            reserved6 TEXT,
            reserved7 TEXT,
            reserved8 TEXT,
            reserved9 TEXT,
            reserved10 TEXT,
            reserved11 TEXT,
            reserved12 TEXT,
            reserved13 TEXT,
            reserved14 TEXT,
            reserved15 TEXT,
            reserved16 TEXT,
            reserved17 TEXT,
            reserved18 TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE INDEX ix_users_extension_user_id ON users_extension(user_id);
CREATE TABLE "rank_logs" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            old_rank TEXT,
            new_rank TEXT,
            change_type TEXT,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE TABLE "colonies" (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            rank TEXT,
            stars INTEGER DEFAULT 0,
            credit INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            group_id INTEGER,
            created_by INTEGER,
            FOREIGN KEY(group_id) REFERENCES colony_groups(id) ON DELETE SET NULL,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        );
CREATE INDEX ix_colonies_rank ON colonies(rank);
CREATE INDEX ix_colonies_stars ON colonies(stars);
CREATE INDEX ix_colonies_credit ON colonies(credit);
CREATE TABLE "colonies_extension" (
            colony_id INTEGER PRIMARY KEY,
            short_code CHAR(5) UNIQUE,
            description TEXT,
            language VARCHAR DEFAULT 'en',
            region VARCHAR,
            member_count INTEGER DEFAULT 0,
            score BIGINT DEFAULT 0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            reserved1 TEXT,
            reserved2 TEXT,
            reserved3 TEXT,
            reserved4 TEXT,
            reserved5 TEXT,
            reserved6 TEXT,
            reserved7 TEXT,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE
        );
CREATE INDEX ix_colonies_extension_colony_id ON colonies_extension(colony_id);
CREATE INDEX ix_colonies_score ON colonies_extension(score);
CREATE TABLE "colony_memberships" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            colony_id INTEGER,
            join_count INTEGER DEFAULT 0,
            last_joined_at DATETIME,
            last_active_at DATETIME,
            status TEXT DEFAULT 'ACTIVE',
            removal_reason TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE
        );
CREATE TABLE "colony_council_votes" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colony_id INTEGER,
            user_id INTEGER,
            target_user_id INTEGER,
            vote_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(target_user_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE TABLE "colony_votes" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            colony_id INTEGER,
            voter_id INTEGER,
            vote TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(colony_id) REFERENCES colonies(id) ON DELETE CASCADE,
            FOREIGN KEY(voter_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE TABLE "strategic_council_members" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            joined_at DATETIME,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE TABLE "strategic_decisions" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            emergency INTEGER DEFAULT 0,
            status TEXT DEFAULT 'PENDING',
            created_by INTEGER,
            created_at DATETIME,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE SET NULL
        );
CREATE TABLE "strategic_votes" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            voter_id INTEGER,
            vote TEXT,
            created_at DATETIME,
            FOREIGN KEY(decision_id) REFERENCES strategic_decisions(id) ON DELETE CASCADE,
            FOREIGN KEY(voter_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE TABLE "strategic_veto" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            veto_by INTEGER,
            reason TEXT,
            created_at DATETIME,
            FOREIGN KEY(decision_id) REFERENCES strategic_decisions(id) ON DELETE CASCADE,
            FOREIGN KEY(veto_by) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE TABLE "emergency_log" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            activated_at DATETIME,
            expires_at DATETIME,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(decision_id) REFERENCES strategic_decisions(id) ON DELETE CASCADE
        );
CREATE TABLE "project_veto_entities" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
CREATE UNIQUE INDEX ix_users_user_id
            ON users(user_id);
CREATE TABLE users_identity (
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
CREATE TABLE users_public (
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
CREATE TABLE users_governance (
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

, governance_status TEXT DEFAULT 'NOT_ELIGIBLE', strike_count INTEGER DEFAULT 0, stability_started_at DATETIME, recovery_until DATETIME, governance_level TEXT DEFAULT 'OBSERVER', stake_locked REAL DEFAULT 0);
CREATE TABLE users_hidden (
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
CREATE TABLE users_position (
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
CREATE INDEX idx_identity_user_code
ON users_identity(user_code);
CREATE INDEX idx_public_user_code
ON users_public(user_code);
CREATE INDEX idx_governance_user_code
ON users_governance(user_code);
CREATE INDEX idx_hidden_user_code
ON users_hidden(user_code);
CREATE INDEX idx_position_user_code
ON users_position(user_code);
CREATE TABLE xp_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_code TEXT,
    action TEXT,
    xp_gained INTEGER,
    multiplier REAL,
    rank_step INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE knowledge_nodes (
	id INTEGER NOT NULL, 
	code VARCHAR, 
	domain VARCHAR, 
	name VARCHAR, 
	title VARCHAR, 
	description TEXT, 
	purpose TEXT, 
	indicators TEXT, 
	positive_signs TEXT, 
	negative_signs TEXT, 
	sources TEXT, 
	related_nodes TEXT, 
	question_types TEXT, 
	mission_types TEXT, 
	capabilities TEXT, 
	capability_justification TEXT, 
	temporal_evolution TEXT, 
	future_evolution TEXT, 
	meta_data TEXT, 
	version VARCHAR, 
	status VARCHAR, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_knowledge_nodes_code ON knowledge_nodes (code);
CREATE TABLE reputation_records (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	node_code VARCHAR, 
	score INTEGER, 
	level VARCHAR, 
	signals JSON, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_reputation_records_user_id ON reputation_records (user_id);
CREATE INDEX ix_reputation_records_node_code ON reputation_records (node_code);
CREATE TABLE ie002_records (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	node_code VARCHAR, 
	trust_score INTEGER, 
	signals JSON, 
	rank VARCHAR, 
	next_rank VARCHAR, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_ie002_records_user_id ON ie002_records (user_id);
CREATE TABLE human_models (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	self_model JSON, 
	social_model JSON, 
	personality_state VARCHAR, 
	growth_direction VARCHAR, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_human_models_user_id ON human_models (user_id);
CREATE TABLE question_templates (
	id INTEGER NOT NULL, 
	node_code VARCHAR, 
	question_type VARCHAR, 
	template TEXT, 
	difficulty INTEGER, 
	version VARCHAR, 
	status VARCHAR, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_question_templates_node_code ON question_templates (node_code);
CREATE TABLE user_answers (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	node_code VARCHAR, 
	question TEXT, 
	answer TEXT, 
	score FLOAT, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_user_answers_node_code ON user_answers (node_code);
CREATE INDEX ix_user_answers_user_id ON user_answers (user_id);
CREATE TABLE life_memories (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	node_code VARCHAR, 
	memory_type VARCHAR, 
	title VARCHAR, 
	content TEXT, 
	confidence FLOAT, 
	source VARCHAR, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_life_memories_user_id ON life_memories (user_id);
CREATE INDEX ix_life_memories_node_code ON life_memories (node_code);
CREATE TABLE life_timeline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type TEXT,
    title TEXT,
    content TEXT,
    node_code TEXT,
    confidence REAL,
    timestamp TEXT
);
CREATE TABLE human_models_v2 (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	trait_profile JSON, 
	strengths JSON, 
	weaknesses JSON, 
	dominant_domains JSON, 
	identity_state VARCHAR, 
	growth_direction VARCHAR, 
	model_version VARCHAR, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_human_models_v2_user_id ON human_models_v2 (user_id);
