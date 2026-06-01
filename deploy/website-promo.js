
async function redeemPromoCode() {
  var input = document.getElementById('profile-promo-code');
  var msgEl = document.getElementById('profile-promo-msg');
  var code = input && input.value ? input.value.trim() : '';
  if (!code) {
    if (msgEl) msgEl.textContent = t('promo.enterCode');
    return;
  }
  if (!window.__authUser) {
    showToast(t('sync.signInFirst'));
    return;
  }
  if (msgEl) msgEl.textContent = t('promo.applying');
  try {
    var r = await authApi('/api/promo/redeem', {
      method: 'POST',
      body: JSON.stringify({ code: code }),
    });
    var data = await r.json().catch(function () { return {}; });
    if (r.ok && data.user) {
      window.__authUser = data.user;
      if (input) input.value = '';
      if (msgEl) msgEl.textContent = tf('promo.success', { limit: data.user.wordLimit || data.wordLimit });
      profileRenderAccount();
      showToast(tf('promo.success', { limit: data.user.wordLimit || data.wordLimit }));
      return;
    }
    var errKey = 'promo.error.' + (data.error || 'generic');
    var msg = t(errKey);
    if (msg === errKey) msg = t('promo.error.generic');
    if (msgEl) msgEl.textContent = msg;
    showToast(msg);
  } catch (e) {
    if (msgEl) msgEl.textContent = t('promo.error.generic');
    showToast(t('promo.error.generic'));
  }
}

function profileRenderWordLimit() {
  var el = document.getElementById('profile-word-limit-row');
  if (!el) return;
  var u = window.__authUser;
  if (!u) { el.textContent = ''; return; }
  if (u.plan === 'premium') {
    el.textContent = t('promo.unlimited');
    return;
  }
  var limit = (typeof u.wordLimit === 'number' && u.wordLimit > 0) ? u.wordLimit : FREE_VOCAB_WORD_LIMIT;
  var count = typeof u.wordCount === 'number' ? u.wordCount : (typeof words !== 'undefined' ? words.length : 0);
  el.textContent = tf('promo.wordUsage', { count: count, limit: limit });
}
