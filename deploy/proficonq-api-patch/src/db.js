import Database from 'better-sqlite3';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const DB_PATH = process.env.DB_PATH || join(here, '..', 'data', 'app.db');

mkdirSync(dirname(DB_PATH), { recursive: true });

export const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

db.exec(`
CREATE TABLE IF NOT EXISTS users (
  id             TEXT PRIMARY KEY,
  email          TEXT UNIQUE NOT NULL,
  password_hash  TEXT NOT NULL,
  password_salt  TEXT NOT NULL,
  email_verified INTEGER NOT NULL DEFAULT 0,
  plan           TEXT NOT NULL DEFAULT 'free',
  created_at     INTEGER NOT NULL,
  updated_at     INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS email_tokens (
  token      TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL,
  type       TEXT NOT NULL,
  expires_at INTEGER NOT NULL,
  used       INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sessions (
  token      TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  user_agent TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_data (
  user_id    TEXT NOT NULL,
  key        TEXT NOT NULL,
  json       TEXT NOT NULL,
  version    INTEGER NOT NULL DEFAULT 1,
  updated_at INTEGER NOT NULL,
  PRIMARY KEY (user_id, key),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_email_tokens_user ON email_tokens(user_id);
`);

function migrate() {
  const userCols = db.prepare('PRAGMA table_info(users)').all();
  if (!userCols.some((c) => c.name === 'word_limit')) {
    db.exec('ALTER TABLE users ADD COLUMN word_limit INTEGER');
  }

  db.exec(`
    CREATE TABLE IF NOT EXISTS promo_codes (
      code TEXT PRIMARY KEY,
      word_limit INTEGER NOT NULL,
      max_redemptions INTEGER,
      redemption_count INTEGER NOT NULL DEFAULT 0,
      active INTEGER NOT NULL DEFAULT 1,
      label TEXT,
      created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS promo_redemptions (
      user_id TEXT NOT NULL,
      code TEXT NOT NULL,
      redeemed_at INTEGER NOT NULL,
      PRIMARY KEY (user_id, code),
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS admin_sessions (
      token      TEXT PRIMARY KEY,
      created_at INTEGER NOT NULL,
      expires_at INTEGER NOT NULL,
      user_agent TEXT
    );
  `);
}

migrate();
