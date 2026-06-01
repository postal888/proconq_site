
var SYNC_PRIMARY_KEY = 'profconq_sync_primary_v1';

function syncGetPrimary() {
  try {
    var v = localStorage.getItem(SYNC_PRIMARY_KEY);
    if (v === 'site') return 'site';
  } catch (e) {}
  return 'app';
}

function syncSetPrimary(mode) {
  if (mode !== 'app' && mode !== 'site') return;
  try { localStorage.setItem(SYNC_PRIMARY_KEY, mode); } catch (e) {}
  syncUpdatePrimaryUi();
}

function syncUpdatePrimaryUi() {
  var mode = syncGetPrimary();
  var appBtn = document.getElementById('sync-primary-app');
  var siteBtn = document.getElementById('sync-primary-site');
  var hint = document.getElementById('sync-primary-hint');
  if (appBtn) appBtn.classList.toggle('is-active', mode === 'app');
  if (siteBtn) siteBtn.classList.toggle('is-active', mode === 'site');
  if (hint) {
    hint.textContent = mode === 'app' ? t('sync.primaryAppHint') : t('sync.primarySiteHint');
  }
}

async function syncMirrorPushToCloud() {
  await fetch('/api/sync/vocabulary', {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ json: { words: words } }),
  });
  await __syncPut('programs', __programs);
  await __syncPut('program_progress', __programProgress);
}

async function syncMirrorPullFromCloud() {
  var r = await fetch('/api/sync/vocabulary', { credentials: 'include' });
  if (r.status === 204) {
    words = [];
  } else if (r.ok) {
    var data = await r.json();
    var w = data && data.json && data.json.words;
    words = Array.isArray(w) ? w : [];
  } else {
    throw new Error('vocabulary HTTP ' + r.status);
  }
  recomputeNextIdFromWords();
  var pr = await authApi('/api/sync/programs');
  if (pr.ok && pr.status !== 204) {
    var pd = await pr.json();
    var pj = pd && pd.json;
    if (Array.isArray(pj)) {
      __programs = pj.map(function (p) { return programsNormalizeProgram(p); });
      programsSave();
    }
  }
  var pp = await authApi('/api/sync/program_progress');
  if (pp.ok && pp.status !== 204) {
    var ppd = await pp.json();
    if (ppd && ppd.json && typeof ppd.json === 'object') {
      __programProgress = ppd.json;
      programsProgressSave();
    }
  }
  renderVocab();
  updateSidebarCounts();
  try { programsLoad(); renderProgramsList(); } catch (e) {}
  try { ytRefreshTranscriptWordClasses(); } catch (e) {}
}

async function syncMirrorNow() {
  if (!window.__authUser) { showToast(t('sync.signInFirst')); return; }
  var mode = syncGetPrimary();
  try {
    if (mode === 'site') {
      await syncMirrorPushToCloud();
      showToast(tf('sync.mirrorPush', { words: words.length, programs: __programs.length }));
    } else {
      await syncMirrorPullFromCloud();
      schedulePersistVocabulary();
      showToast(tf('sync.mirrorPull', { words: words.length, programs: __programs.length }));
    }
  } catch (e) {
    console.warn('syncMirrorNow', e);
    showToast(t('sync.error'));
  }
}
