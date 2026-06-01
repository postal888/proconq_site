
var FREE_VOCAB_WORD_LIMIT = 10;

function vocabEffectiveLimit() {
  if (window.__authUser && window.__authUser.plan === 'premium') return Infinity;
  var custom = window.__authUser && window.__authUser.wordLimit;
  if (typeof custom === 'number' && custom > 0) return custom;
  return FREE_VOCAB_WORD_LIMIT;
}

function vocabCanAddMoreWords() {
  if (window.__authUser && window.__authUser.plan === 'premium') return true;
  return words.length < vocabEffectiveLimit();
}

function vocabShowWordLimitToast() {
  showToast(tf('vocab.wordLimitToast', { limit: vocabEffectiveLimit() }));
}
