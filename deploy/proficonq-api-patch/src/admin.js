import { randomBytes } from 'node:crypto';
import { db } from './db.js';
import { verifyPassword } from './auth.js';

export const ADMIN_COOKIE_NAME = 'pq_admin_session';
const SESSION_TTL_DAYS = Number(process.env.ADMIN_SESSION_TTL_DAYS || 7);

export function verifyAdminCredentials(username, password) {
  const expectedUser = String(process.env.ADMIN_USERNAME || 'admin').trim();
  const hash = process.env.ADMIN_PASSWORD_HASH;
  const salt = process.env.ADMIN_PASSWORD_SALT;
  if (!hash || !salt) return false;
  if (String(username || '').trim() !== expectedUser) return false;
  return verifyPassword(String(password || ''), salt, hash);
}

export function createAdminSession(userAgent) {
  const token = randomBytes(32).toString('hex');
  const now = Date.now();
  const expiresAt = now + SESSION_TTL_DAYS * 86400000;
  db.prepare(
    'INSERT INTO admin_sessions (token, created_at, expires_at, user_agent) VALUES (?, ?, ?, ?)',
  ).run(token, now, expiresAt, userAgent || null);
  return { token, expiresAt };
}

export function getAdminSession(token) {
  if (!token) return null;
  const session = db.prepare('SELECT * FROM admin_sessions WHERE token = ?').get(token);
  if (!session) return null;
  if (session.expires_at < Date.now()) {
    db.prepare('DELETE FROM admin_sessions WHERE token = ?').run(token);
    return null;
  }
  return session;
}

export function deleteAdminSession(token) {
  if (token) db.prepare('DELETE FROM admin_sessions WHERE token = ?').run(token);
}

export function adminTokenFromRequest(req) {
  return (req.cookies && req.cookies[ADMIN_COOKIE_NAME]) || null;
}

export function isAdminRequest(req) {
  return !!getAdminSession(adminTokenFromRequest(req));
}
