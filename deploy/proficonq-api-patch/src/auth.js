import { randomBytes, scryptSync, timingSafeEqual, randomUUID } from 'node:crypto';
import { db } from './db.js';
import { looksLikeFirebaseJwt, verifyFirebaseIdToken } from './firebase.js';

const SESSION_TTL_DAYS = Number(process.env.SESSION_TTL_DAYS || 30);
const SCRYPT_KEYLEN = 64;

export function hashPassword(password, salt = randomBytes(16).toString('hex')) {
  const hash = scryptSync(password, salt, SCRYPT_KEYLEN).toString('hex');
  return { hash, salt };
}

export function verifyPassword(password, salt, expectedHashHex) {
  const hash = scryptSync(password, salt, SCRYPT_KEYLEN);
  const expected = Buffer.from(expectedHashHex, 'hex');
  if (hash.length !== expected.length) return false;
  return timingSafeEqual(hash, expected);
}

export function createUser(email, password) {
  const { hash, salt } = hashPassword(password);
  const now = Date.now();
  const id = randomUUID();
  db.prepare(
    `INSERT INTO users (id, email, password_hash, password_salt, email_verified, plan, created_at, updated_at)
     VALUES (?, ?, ?, ?, 0, 'free', ?, ?)`
  ).run(id, email, hash, salt, now, now);
  return getUserById(id);
}

export function getUserByEmail(email) {
  return db.prepare('SELECT * FROM users WHERE email = ?').get(email);
}

export function getUserById(id) {
  return db.prepare('SELECT * FROM users WHERE id = ?').get(id);
}

export function setUserVerified(userId) {
  db.prepare('UPDATE users SET email_verified = 1, updated_at = ? WHERE id = ?').run(Date.now(), userId);
}

export function setUserPassword(userId, password) {
  const { hash, salt } = hashPassword(password);
  db.prepare('UPDATE users SET password_hash = ?, password_salt = ?, updated_at = ? WHERE id = ?')
    .run(hash, salt, Date.now(), userId);
}

export function createSession(userId, userAgent) {
  const token = randomBytes(32).toString('hex');
  const now = Date.now();
  const expiresAt = now + SESSION_TTL_DAYS * 86400000;
  db.prepare('INSERT INTO sessions (token, user_id, created_at, expires_at, user_agent) VALUES (?, ?, ?, ?, ?)')
    .run(token, userId, now, expiresAt, userAgent || null);
  return { token, expiresAt };
}

export function getSession(token) {
  if (!token) return null;
  const s = db.prepare('SELECT * FROM sessions WHERE token = ?').get(token);
  if (!s) return null;
  if (s.expires_at < Date.now()) {
    db.prepare('DELETE FROM sessions WHERE token = ?').run(token);
    return null;
  }
  return s;
}

export function deleteSession(token) {
  if (token) db.prepare('DELETE FROM sessions WHERE token = ?').run(token);
}

export function deleteUserSessions(userId) {
  db.prepare('DELETE FROM sessions WHERE user_id = ?').run(userId);
}

export function createEmailToken(userId, type, ttlMs) {
  const token = randomBytes(32).toString('hex');
  const expiresAt = Date.now() + ttlMs;
  db.prepare('INSERT INTO email_tokens (token, user_id, type, expires_at, used) VALUES (?, ?, ?, ?, 0)')
    .run(token, userId, type, expiresAt);
  return token;
}

export function consumeEmailToken(token, type) {
  if (!token) return null;
  const row = db.prepare('SELECT * FROM email_tokens WHERE token = ? AND type = ?').get(token, type);
  if (!row || row.used || row.expires_at < Date.now()) return null;
  db.prepare('UPDATE email_tokens SET used = 1 WHERE token = ?').run(token);
  return row;
}

const COOKIE_NAME = 'pq_session';

export function tokenFromRequest(req) {
  let token = req.cookies && req.cookies[COOKIE_NAME];
  if (!token) {
    const auth = req.headers['authorization'];
    if (auth && auth.startsWith('Bearer ')) token = auth.slice(7).trim();
  }
  return token || null;
}

export function findOrCreateUserFromFirebase(decoded) {
  const email = String(decoded.email || '').trim().toLowerCase();
  if (!email) {
    throw new Error('firebase_email_required');
  }
  let user = getUserByEmail(email);
  if (user) {
    if (!user.email_verified) setUserVerified(user.id);
    return user;
  }
  const randomPassword = randomBytes(32).toString('hex');
  user = createUser(email, randomPassword);
  setUserVerified(user.id);
  return user;
}

export async function getRequestUser(req) {
  const token = tokenFromRequest(req);
  if (!token) return null;

  if (looksLikeFirebaseJwt(token)) {
    try {
      const decoded = await verifyFirebaseIdToken(token);
      return findOrCreateUserFromFirebase(decoded);
    } catch {
      return null;
    }
  }

  const session = getSession(token);
  if (!session) return null;
  return getUserById(session.user_id);
}

export { publicUserWithLimits as publicUser } from './wordLimit.js';

export { COOKIE_NAME };
