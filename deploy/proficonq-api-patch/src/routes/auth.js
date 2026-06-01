import {
  createUser,
  getUserByEmail,
  getUserById,
  setUserVerified,
  setUserPassword,
  createSession,
  deleteSession,
  deleteUserSessions,
  createEmailToken,
  consumeEmailToken,
  verifyPassword,
  getRequestUser,
  findOrCreateUserFromFirebase,
  tokenFromRequest,
  publicUser,
  COOKIE_NAME,
} from '../auth.js';
import { verifyFirebaseIdToken } from '../firebase.js';
import { sendVerifyEmail, sendResetEmail } from '../email.js';

const APP_BASE_URL = (process.env.APP_BASE_URL || 'https://profconq.com').replace(/\/$/, '');
const SESSION_TTL_DAYS = Number(process.env.SESSION_TTL_DAYS || 30);
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const VERIFY_TTL = 24 * 60 * 60 * 1000;
const RESET_TTL = 60 * 60 * 1000;

function normEmail(v) {
  return String(v || '').trim().toLowerCase();
}

function setSessionCookie(reply, token) {
  reply.setCookie(COOKIE_NAME, token, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    path: '/',
    maxAge: SESSION_TTL_DAYS * 86400,
  });
}

function issueVerification(user, log) {
  const token = createEmailToken(user.id, 'verify', VERIFY_TTL);
  const link = `${APP_BASE_URL}/api/auth/verify?token=${token}`;
  sendVerifyEmail(user.email, link).catch(function (e) { if (log) log.error(e); });
}

export default async function authRoutes(fastify) {
  fastify.post('/api/auth/register', async (req, reply) => {
    const email = normEmail(req.body?.email);
    const password = String(req.body?.password || '');
    if (!EMAIL_RE.test(email)) return reply.code(400).send({ error: 'invalid_email' });
    if (password.length < 8) return reply.code(400).send({ error: 'weak_password' });

    const existing = getUserByEmail(email);
    if (existing) {
      if (!existing.email_verified) {
        issueVerification(existing, req.log);
        return reply.code(409).send({ error: 'email_pending_verification' });
      }
      return reply.code(409).send({ error: 'email_already_registered' });
    }

    const user = createUser(email, password);
    issueVerification(user, req.log);
    return reply.send({ ok: true });
  });

  fastify.get('/api/auth/verify', async (req, reply) => {
    const token = req.query?.token;
    const row = consumeEmailToken(token, 'verify');
    if (!row) return reply.redirect(`${APP_BASE_URL}/login?verified=0`);
    setUserVerified(row.user_id);
    return reply.redirect(`${APP_BASE_URL}/login?verified=1`);
  });

  fastify.post('/api/auth/login', async (req, reply) => {
    const email = normEmail(req.body?.email);
    const password = String(req.body?.password || '');
    const user = getUserByEmail(email);
    if (!user || !verifyPassword(password, user.password_salt, user.password_hash)) {
      return reply.code(401).send({ error: 'invalid_credentials' });
    }
    if (!user.email_verified) {
      return reply.code(403).send({ error: 'not_verified' });
    }
    const { token } = createSession(user.id, req.headers['user-agent']);
    setSessionCookie(reply, token);
    return reply.send({ user: publicUser(user), token });
  });

  fastify.post('/api/auth/firebase', async (req, reply) => {
    const idToken = String(req.body?.idToken || '');
    if (!idToken) return reply.code(400).send({ error: 'missing_id_token' });
    try {
      const decoded = await verifyFirebaseIdToken(idToken);
      const user = findOrCreateUserFromFirebase(decoded);
      const { token } = createSession(user.id, req.headers['user-agent']);
      setSessionCookie(reply, token);
      return reply.send({ user: publicUser(user), token });
    } catch (e) {
      req.log.error(e);
      return reply.code(401).send({ error: 'invalid_firebase_token' });
    }
  });

  fastify.post('/api/auth/logout', async (req, reply) => {
    deleteSession(tokenFromRequest(req));
    reply.clearCookie(COOKIE_NAME, { path: '/' });
    return reply.send({ ok: true });
  });

  fastify.get('/api/auth/me', async (req, reply) => {
    const user = await getRequestUser(req);
    if (!user) return reply.code(401).send({ error: 'unauthorized' });
    return reply.send({ user: publicUser(user) });
  });

  fastify.post('/api/auth/resend-verification', async (req, reply) => {
    const email = normEmail(req.body?.email);
    const user = getUserByEmail(email);
    if (user && !user.email_verified) issueVerification(user, req.log);
    return reply.send({ ok: true });
  });

  fastify.post('/api/auth/forgot-password', async (req, reply) => {
    const email = normEmail(req.body?.email);
    const user = getUserByEmail(email);
    if (user) {
      const token = createEmailToken(user.id, 'reset', RESET_TTL);
      sendResetEmail(user.email, `${APP_BASE_URL}/reset?token=${token}`).catch(function (e) { req.log.error(e); });
    }
    return reply.send({ ok: true });
  });

  fastify.post('/api/auth/reset-password', async (req, reply) => {
    const token = req.body?.token;
    const password = String(req.body?.password || '');
    if (password.length < 8) return reply.code(400).send({ error: 'weak_password' });
    const row = consumeEmailToken(token, 'reset');
    if (!row) return reply.code(400).send({ error: 'invalid_token' });
    const user = getUserById(row.user_id);
    if (!user) return reply.code(400).send({ error: 'invalid_token' });
    setUserPassword(user.id, password);
    if (!user.email_verified) setUserVerified(user.id);
    deleteUserSessions(user.id);
    return reply.send({ ok: true });
  });
}
