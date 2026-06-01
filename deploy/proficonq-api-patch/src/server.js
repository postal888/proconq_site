import 'dotenv/config';
import Fastify from 'fastify';
import cookie from '@fastify/cookie';
import authRoutes from './routes/auth.js';
import syncRoutes from './routes/sync.js';
import promoRoutes from './routes/promo.js';
import adminRoutes from './routes/admin.js';
import { emailConfigured } from './email.js';

const fastify = Fastify({
  logger: true,
  trustProxy: true,
  bodyLimit: 8 * 1024 * 1024,
});

await fastify.register(cookie);
await fastify.register(authRoutes);
await fastify.register(syncRoutes);
await fastify.register(promoRoutes);
await fastify.register(adminRoutes);

fastify.get('/api/auth/health', async () => ({
  ok: true,
  service: 'proficonq-api',
  emailConfigured: emailConfigured(),
}));

const port = Number(process.env.PORT || 4000);

try {
  await fastify.listen({ host: '127.0.0.1', port });
  if (!emailConfigured()) {
    fastify.log.warn('SMTP not configured — verification/reset links will be logged to stdout (dev mode).');
  }
} catch (err) {
  fastify.log.error(err);
  process.exit(1);
}
