import {
  verifyAdminCredentials,
  createAdminSession,
  deleteAdminSession,
  adminTokenFromRequest,
  isAdminRequest,
  ADMIN_COOKIE_NAME,
} from '../admin.js';
import {
  createPromoCode,
  listPromoCodes,
  setPromoCodeActive,
  updatePromoCode,
} from '../promo.js';

const SESSION_TTL_DAYS = Number(process.env.ADMIN_SESSION_TTL_DAYS || 7);

function setAdminCookie(reply, token) {
  reply.setCookie(ADMIN_COOKIE_NAME, token, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    path: '/',
    maxAge: SESSION_TTL_DAYS * 86400,
  });
}

async function requireAdmin(req, reply) {
  if (!isAdminRequest(req)) {
    reply.code(401).send({ error: 'unauthorized' });
    return false;
  }
  return true;
}

export default async function adminRoutes(fastify) {
  fastify.post('/api/admin/login', async (req, reply) => {
    const username = String(req.body?.username || '').trim();
    const password = String(req.body?.password || '');
    if (!verifyAdminCredentials(username, password)) {
      return reply.code(401).send({ error: 'invalid_credentials' });
    }
    const { token } = createAdminSession(req.headers['user-agent']);
    setAdminCookie(reply, token);
    return reply.send({ ok: true, username: process.env.ADMIN_USERNAME || 'admin' });
  });

  fastify.post('/api/admin/logout', async (req, reply) => {
    deleteAdminSession(adminTokenFromRequest(req));
    reply.clearCookie(ADMIN_COOKIE_NAME, { path: '/' });
    return reply.send({ ok: true });
  });

  fastify.get('/api/admin/me', async (req, reply) => {
    if (!isAdminRequest(req)) return reply.code(401).send({ error: 'unauthorized' });
    return reply.send({ ok: true, username: process.env.ADMIN_USERNAME || 'admin' });
  });

  fastify.get('/api/admin/promo-codes', async (req, reply) => {
    if (!(await requireAdmin(req, reply))) return;
    return reply.send({ codes: listPromoCodes() });
  });

  fastify.post('/api/admin/promo-codes', async (req, reply) => {
    if (!(await requireAdmin(req, reply))) return;
    const result = createPromoCode(req.body || {});
    if (result.error) {
      const status = {
        missing_word_limit: 400,
        invalid_word_limit: 400,
        invalid_code: 400,
        code_exists: 409,
        could_not_generate_code: 500,
      }[result.error] || 400;
      return reply.code(status).send({ error: result.error, message: result.message });
    }
    return reply.send({ ok: true, code: result.code });
  });

  fastify.patch('/api/admin/promo-codes/:code', async (req, reply) => {
    if (!(await requireAdmin(req, reply))) return;
    const result = updatePromoCode(req.params.code, req.body || {});
    if (result.error) {
      const status = result.error === 'not_found' ? 404 : 400;
      return reply.code(status).send({ error: result.error, message: result.message });
    }
    return reply.send({ ok: true, code: result.code });
  });

  fastify.post('/api/admin/promo-codes/:code/toggle', async (req, reply) => {
    if (!(await requireAdmin(req, reply))) return;
    const active = req.body?.active;
    if (typeof active !== 'boolean') {
      return reply.code(400).send({ error: 'invalid_active' });
    }
    const result = setPromoCodeActive(req.params.code, active);
    if (result.error) return reply.code(404).send({ error: result.error });
    return reply.send({ ok: true, code: result.code, active: result.active });
  });
}
