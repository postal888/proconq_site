import { randomBytes } from 'node:crypto';
import { db } from './db.js';
import { getUserById } from './auth.js';
import { effectiveWordLimit, FREE_WORD_LIMIT } from './wordLimit.js';

const CODE_RE = /^[A-Z0-9][A-Z0-9_-]{2,31}$/;

function normalizeCode(raw) {
  return String(raw || '').trim().toUpperCase();
}

function formatPromoRow(row) {
  if (!row) return null;
  return {
    code: row.code,
    wordLimit: row.word_limit,
    maxRedemptions: row.max_redemptions,
    redemptionCount: row.redemption_count,
    active: !!row.active,
    label: row.label || '',
    createdAt: row.created_at,
  };
}

export function generatePromoCode(prefix = 'PQ') {
  const cleanPrefix = normalizeCode(prefix).replace(/[^A-Z0-9]/g, '').slice(0, 8);
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  for (let attempt = 0; attempt < 20; attempt += 1) {
    let suffix = '';
    const bytes = randomBytes(6);
    for (let i = 0; i < 6; i += 1) {
      suffix += alphabet[bytes[i] % alphabet.length];
    }
    const code = `${cleanPrefix || 'PQ'}${suffix}`;
    const exists = db.prepare('SELECT 1 FROM promo_codes WHERE code = ?').get(code);
    if (!exists) return code;
  }
  return null;
}

export function listPromoCodes() {
  const rows = db
    .prepare(
      `SELECT code, word_limit, max_redemptions, redemption_count, active, label, created_at
       FROM promo_codes
       ORDER BY created_at DESC, code ASC`,
    )
    .all();
  return rows.map(formatPromoRow);
}

export function createPromoCode(body) {
  const wordLimit = Number(body.wordLimit);
  if (!Number.isFinite(wordLimit) || wordLimit <= 0) {
    return { error: 'invalid_word_limit', message: 'wordLimit must be a positive number' };
  }

  let code = body.generate ? generatePromoCode(body.prefix || 'PQ') : normalizeCode(body.code);
  if (!code) return { error: 'could_not_generate_code', message: 'Could not generate unique code' };
  if (!body.generate && !code) {
    return { error: 'missing_code', message: 'Promo code is required' };
  }
  if (!CODE_RE.test(code)) {
    return {
      error: 'invalid_code',
      message: 'Code must be 3-32 chars: letters, digits, _ or -',
    };
  }

  const maxRedemptions = body.maxRedemptions == null || body.maxRedemptions === ''
    ? null
    : Number(body.maxRedemptions);
  if (maxRedemptions != null && (!Number.isFinite(maxRedemptions) || maxRedemptions <= 0)) {
    return { error: 'invalid_max_redemptions', message: 'maxRedemptions must be positive' };
  }

  const label = body.label ? String(body.label).trim().slice(0, 120) : null;
  const now = Date.now();
  const existing = db.prepare('SELECT code FROM promo_codes WHERE code = ?').get(code);
  if (existing) return { error: 'code_exists', message: 'Promo code already exists' };

  db.prepare(
    `INSERT INTO promo_codes (code, word_limit, max_redemptions, redemption_count, active, label, created_at)
     VALUES (?, ?, ?, 0, 1, ?, ?)`,
  ).run(code, wordLimit, maxRedemptions, label, now);

  return { ok: true, code };
}

export function updatePromoCode(rawCode, body) {
  const code = normalizeCode(rawCode);
  const row = db.prepare('SELECT * FROM promo_codes WHERE code = ?').get(code);
  if (!row) return { error: 'not_found', message: 'Promo code not found' };

  const wordLimit = body.wordLimit == null ? row.word_limit : Number(body.wordLimit);
  if (!Number.isFinite(wordLimit) || wordLimit <= 0) {
    return { error: 'invalid_word_limit', message: 'wordLimit must be a positive number' };
  }

  const maxRedemptions = body.maxRedemptions === undefined
    ? row.max_redemptions
    : (body.maxRedemptions == null || body.maxRedemptions === ''
      ? null
      : Number(body.maxRedemptions));
  if (maxRedemptions != null && (!Number.isFinite(maxRedemptions) || maxRedemptions <= 0)) {
    return { error: 'invalid_max_redemptions', message: 'maxRedemptions must be positive' };
  }

  const label = body.label === undefined
    ? row.label
    : (body.label ? String(body.label).trim().slice(0, 120) : null);

  db.prepare(
    `UPDATE promo_codes
     SET word_limit = ?, max_redemptions = ?, label = ?
     WHERE code = ?`,
  ).run(wordLimit, maxRedemptions, label, code);

  return { ok: true, code };
}

export function setPromoCodeActive(rawCode, active) {
  const code = normalizeCode(rawCode);
  const row = db.prepare('SELECT code FROM promo_codes WHERE code = ?').get(code);
  if (!row) return { error: 'not_found' };
  db.prepare('UPDATE promo_codes SET active = ? WHERE code = ?').run(active ? 1 : 0, code);
  return { ok: true, code, active: !!active };
}

export function redeemPromoCode(userId, rawCode) {
  const code = normalizeCode(rawCode);
  if (!code) return { error: 'missing_code' };

  const promo = db
    .prepare('SELECT * FROM promo_codes WHERE code = ? AND active = 1')
    .get(code);
  if (!promo) return { error: 'invalid_code' };

  if (promo.max_redemptions != null && promo.redemption_count >= promo.max_redemptions) {
    return { error: 'code_exhausted' };
  }

  const already = db
    .prepare('SELECT 1 FROM promo_redemptions WHERE user_id = ? AND code = ?')
    .get(userId, promo.code);
  if (already) return { error: 'already_redeemed' };

  const user = getUserById(userId);
  if (!user) return { error: 'invalid_user' };
  if (user.plan === 'premium') return { error: 'already_premium' };

  const now = Date.now();
  const apply = db.transaction(() => {
    db.prepare(
      'INSERT INTO promo_redemptions (user_id, code, redeemed_at) VALUES (?, ?, ?)',
    ).run(userId, promo.code, now);
    db.prepare(
      'UPDATE promo_codes SET redemption_count = redemption_count + 1 WHERE code = ?',
    ).run(promo.code);
    const currentLimit = user.word_limit != null && user.word_limit > 0
      ? user.word_limit
      : FREE_WORD_LIMIT;
    const newLimit = Math.max(currentLimit, promo.word_limit);
    db.prepare('UPDATE users SET word_limit = ?, updated_at = ? WHERE id = ?').run(
      newLimit,
      now,
      userId,
    );
  });
  apply();

  const updated = getUserById(userId);
  return {
    ok: true,
    wordLimit: effectiveWordLimit(updated),
    code: promo.code,
  };
}

export function seedPromoCode(code, wordLimit, opts = {}) {
  const normalized = normalizeCode(code);
  const now = Date.now();
  db.prepare(
    `INSERT INTO promo_codes (code, word_limit, max_redemptions, redemption_count, active, label, created_at)
     VALUES (?, ?, ?, 0, 1, ?, ?)
     ON CONFLICT(code) DO UPDATE SET
       word_limit = excluded.word_limit,
       max_redemptions = excluded.max_redemptions,
       active = 1,
       label = excluded.label`,
  ).run(
    normalized,
    wordLimit,
    opts.maxRedemptions ?? null,
    opts.label ?? null,
    now,
  );
  return normalized;
}
