import { getRequestUser } from '../auth.js';
import { db } from '../db.js';
import { effectiveWordLimit, vocabularyWordCount } from '../wordLimit.js';

const ALLOWED_KEYS = new Set([
  'vocabulary',
  'programs',
  'program_progress',
  'activity',
  'settings',
  'fle_plan_track',
  'fle_study_log',
]);

export default async function syncRoutes(fastify) {
  fastify.addHook('preHandler', async (req, reply) => {
    const user = await getRequestUser(req);
    if (!user) return reply.code(401).send({ error: 'unauthorized' });
    req.user = user;
  });

  fastify.get('/api/sync', async (req) => {
    const rows = db
      .prepare('SELECT key, json, version, updated_at FROM user_data WHERE user_id = ?')
      .all(req.user.id);
    const keys = {};
    for (const r of rows) {
      keys[r.key] = { json: JSON.parse(r.json), version: r.version, updatedAt: r.updated_at };
    }
    return { keys };
  });

  fastify.get('/api/sync/:key', async (req, reply) => {
    const key = req.params.key;
    if (!ALLOWED_KEYS.has(key)) return reply.code(400).send({ error: 'bad_key' });
    const r = db
      .prepare('SELECT json, version, updated_at FROM user_data WHERE user_id = ? AND key = ?')
      .get(req.user.id, key);
    if (!r) return reply.code(204).send();
    return { json: JSON.parse(r.json), version: r.version, updatedAt: r.updated_at };
  });

  fastify.put('/api/sync/:key', async (req, reply) => {
    const key = req.params.key;
    if (!ALLOWED_KEYS.has(key)) return reply.code(400).send({ error: 'bad_key' });
    if (!req.body || req.body.json === undefined) {
      return reply.code(400).send({ error: 'missing_json' });
    }

    const limit = effectiveWordLimit(req.user);
    if (key === 'vocabulary' && limit != null) {
      const count = vocabularyWordCount(req.body.json);
      if (count > limit) {
        return reply.code(402).send({
          error: 'word_limit',
          count,
          limit,
          wordLimit: limit,
        });
      }
    }

    const now = Date.now();
    const jsonStr = JSON.stringify(req.body.json);
    const existing = db
      .prepare('SELECT version FROM user_data WHERE user_id = ? AND key = ?')
      .get(req.user.id, key);
    const version = (existing ? existing.version : 0) + 1;
    db.prepare(
      `INSERT INTO user_data (user_id, key, json, version, updated_at)
       VALUES (?, ?, ?, ?, ?)
       ON CONFLICT(user_id, key) DO UPDATE SET
         json = excluded.json,
         version = excluded.version,
         updated_at = excluded.updated_at`,
    ).run(req.user.id, key, jsonStr, version, now);
    return {
      ok: true,
      version,
      updatedAt: now,
      wordCount: key === 'vocabulary' ? vocabularyWordCount(req.body.json) : undefined,
      wordLimit: limit,
    };
  });
}
