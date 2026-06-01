
var __adminPromoCodes = [];

function adminIsUser() {
  return !!(window.__authUser && window.__authUser.isAdmin);
}

function adminUpdateNavVisibility() {
  var nav = document.getElementById('nav-admin');
  if (nav) nav.hidden = !adminIsUser();
}

function adminFormatDate(ts) {
  if (!ts) return '—';
  try { return new Date(ts).toLocaleDateString(); } catch (e) { return '—'; }
}

function adminSetMsg(text, kind) {
  var el = document.getElementById('admin-promo-msg');
  if (!el) return;
  el.textContent = text || '';
  el.className = 'profile-setting-desc admin-promo-msg' + (kind ? (' is-' + kind) : '');
}

function adminRenderPromoTable() {
  var body = document.getElementById('admin-promo-table-body');
  if (!body) return;
  if (!__adminPromoCodes.length) {
    body.innerHTML = '<tr><td colspan="6" class="admin-empty">' + t('admin.promo.empty') + '</td></tr>';
    return;
  }
  body.innerHTML = __adminPromoCodes.map(function (row) {
    var max = row.maxRedemptions == null ? '∞' : row.maxRedemptions;
    var status = row.active ? t('admin.promo.active') : t('admin.promo.inactive');
    var toggleLabel = row.active ? t('admin.promo.deactivate') : t('admin.promo.activate');
    var label = row.label ? ('<div class="admin-promo-label">' + escapeHtml(row.label) + '</div>') : '';
    return '<tr>' +
      '<td><strong>' + escapeHtml(row.code) + '</strong>' + label + '</td>' +
      '<td>' + row.wordLimit + '</td>' +
      '<td>' + max + '</td>' +
      '<td>' + row.redemptionCount + '</td>' +
      '<td>' + status + '</td>' +
      '<td><button type="button" class="btn btn-ghost btn-sm" onclick="adminTogglePromoCode(\'' +
        escapeHtml(row.code) + '\',' + (row.active ? 'false' : 'true') + ')">' + toggleLabel + '</button></td>' +
      '</tr>';
  }).join('');
}

async function adminLoadPromoCodes() {
  if (!adminIsUser()) return;
  adminSetMsg(t('admin.promo.loading'), '');
  try {
    var r = await authApi('/api/admin/promo-codes');
    if (r.status === 403) {
      adminSetMsg(t('admin.forbidden'), 'error');
      return;
    }
    if (!r.ok) throw new Error('load failed');
    var data = await r.json();
    __adminPromoCodes = data.codes || [];
    adminRenderPromoTable();
    adminSetMsg('', '');
  } catch (e) {
    adminSetMsg(t('admin.promo.loadError'), 'error');
  }
}

async function adminCreatePromoCode(ev) {
  if (ev) ev.preventDefault();
  if (!adminIsUser()) return false;
  var generate = !!(document.getElementById('admin-promo-generate') && document.getElementById('admin-promo-generate').checked);
  var code = (document.getElementById('admin-promo-code') && document.getElementById('admin-promo-code').value || '').trim();
  var wordLimit = Number(document.getElementById('admin-promo-limit') && document.getElementById('admin-promo-limit').value);
  var maxRaw = document.getElementById('admin-promo-max') && document.getElementById('admin-promo-max').value;
  var label = (document.getElementById('admin-promo-label') && document.getElementById('admin-promo-label').value || '').trim();
  var prefix = (document.getElementById('admin-promo-prefix') && document.getElementById('admin-promo-prefix').value || 'PQ').trim();

  if (!wordLimit || wordLimit <= 0) {
    adminSetMsg(t('admin.promo.invalidLimit'), 'error');
    return false;
  }
  if (!generate && !code) {
    adminSetMsg(t('admin.promo.enterCode'), 'error');
    return false;
  }

  adminSetMsg(t('admin.promo.creating'), '');
  try {
    var payload = {
      wordLimit: wordLimit,
      generate: generate,
      prefix: prefix,
      label: label || null,
    };
    if (!generate) payload.code = code;
    if (maxRaw !== '' && maxRaw != null) payload.maxRedemptions = Number(maxRaw);

    var r = await authApi('/api/admin/promo-codes', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    var data = await r.json().catch(function () { return {}; });
    if (!r.ok) {
      adminSetMsg(data.message || t('admin.promo.createError'), 'error');
      return false;
    }
    adminSetMsg(tf('admin.promo.created', { code: data.code || '' }), 'ok');
    if (document.getElementById('admin-promo-code')) document.getElementById('admin-promo-code').value = '';
    if (document.getElementById('admin-promo-label')) document.getElementById('admin-promo-label').value = '';
    await adminLoadPromoCodes();
  } catch (e) {
    adminSetMsg(t('admin.promo.createError'), 'error');
  }
  return false;
}

async function adminTogglePromoCode(code, active) {
  if (!adminIsUser()) return;
  try {
    var r = await authApi('/api/admin/promo-codes/' + encodeURIComponent(code) + '/toggle', {
      method: 'POST',
      body: JSON.stringify({ active: !!active }),
    });
    if (!r.ok) throw new Error('toggle failed');
    await adminLoadPromoCodes();
  } catch (e) {
    adminSetMsg(t('admin.promo.toggleError'), 'error');
  }
}

function adminSyncGenerateUi() {
  var generate = !!(document.getElementById('admin-promo-generate') && document.getElementById('admin-promo-generate').checked);
  var codeWrap = document.getElementById('admin-promo-code-wrap');
  var prefixWrap = document.getElementById('admin-promo-prefix-wrap');
  if (codeWrap) codeWrap.style.display = generate ? 'none' : '';
  if (prefixWrap) prefixWrap.style.display = generate ? '' : 'none';
}

function initAdminView() {
  adminUpdateNavVisibility();
  if (!adminIsUser()) return;
  adminSyncGenerateUi();
  adminLoadPromoCodes();
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
