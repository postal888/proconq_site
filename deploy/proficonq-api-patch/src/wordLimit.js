import { db } from './db.js';

export const FREE_WORD_LIMIT = Number(process.env.FREE_WORD_LIMIT || 10);

export function vocabularyWordCount(json) {
  if (!json || !Array.isArray(json.words)) return 0;
  return json.words.length;
}

export function getStoredVocabularyWordCount(userId) {
  const row = db
    .prepare('SELECT json FROM user_data WHERE user_id = ? AND key = ?')
    .get(userId, 'vocabulary');
  if (!row) return 0;
  try {
    return vocabularyWordCount(JSON.parse(row.json));
  } catch {
    return 0;
  }
}

/** @returns {number|null} null = unlimited (premium) */
export function effectiveWordLimit(user) {
  if (!user) return FREE_WORD_LIMIT;
  if (user.plan === 'premium') return null;
  const custom = user.word_limit;
  if (custom != null && custom > 0) return custom;
  return FREE_WORD_LIMIT;
}

export function publicUserWithLimits(user) {
  if (!user) return null;
  const limit = effectiveWordLimit(user);
  return {
    email: user.email,
    plan: user.plan,
    emailVerified: !!user.email_verified,
    wordLimit: limit,
    wordCount: getStoredVocabularyWordCount(user.id),
  };
}
