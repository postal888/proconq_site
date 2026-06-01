#!/usr/bin/env node
/**
 * Create or update promo codes.
 *
 * Usage:
 *   node scripts/manage-promo-codes.js FRIEND100 100
 *   node scripts/manage-promo-codes.js VIP500 500 --max 50 --label "Launch batch"
 */
import { seedPromoCode } from '../src/promo.js';
import { db } from '../src/db.js';

function parseArgs(argv) {
  const positional = [];
  const opts = { maxRedemptions: null, label: null };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--max') {
      opts.maxRedemptions = Number(argv[++i]);
    } else if (arg === '--label') {
      opts.label = argv[++i];
    } else if (arg === '--list') {
      opts.list = true;
    } else {
      positional.push(arg);
    }
  }
  return { positional, opts };
}

const { positional, opts } = parseArgs(process.argv);

if (opts.list) {
  const rows = db.prepare(
    'SELECT code, word_limit, max_redemptions, redemption_count, active, label FROM promo_codes ORDER BY code',
  ).all();
  console.table(rows);
  process.exit(0);
}

const [code, limitRaw] = positional;
if (!code || !limitRaw) {
  console.error('Usage: node scripts/manage-promo-codes.js CODE WORD_LIMIT [--max N] [--label text]');
  console.error('       node scripts/manage-promo-codes.js --list');
  process.exit(1);
}

const wordLimit = Number(limitRaw);
if (!Number.isFinite(wordLimit) || wordLimit <= 0) {
  console.error('WORD_LIMIT must be a positive number');
  process.exit(1);
}

const saved = seedPromoCode(code, wordLimit, {
  maxRedemptions: opts.maxRedemptions,
  label: opts.label,
});
console.log(`Saved promo code ${saved} -> ${wordLimit} words`);
