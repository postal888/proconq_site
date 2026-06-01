
function vocabNormalizeKey(w) {
  return String(w || '').trim().toLowerCase().normalize('NFD').replace(/\p{M}/gu, '');
}

function vocabMergeAppend(baseWords, incomingWords) {
  var byKey = new Map();
  var maxId = 0;
  baseWords.forEach(function (w) {
    var k = vocabNormalizeKey(w.word);
    if (!k) return;
    byKey.set(k, w);
    var id = Number(w.id);
    if (isFinite(id) && id > maxId) maxId = id;
  });
  var nextId = maxId + 1;
  var added = 0;
  incomingWords.forEach(function (w) {
    var k = vocabNormalizeKey(w.word);
    if (!k || byKey.has(k)) return;
    var copy = Object.assign({}, w);
    var id = Number(copy.id);
    if (!isFinite(id) || id <= 0) copy.id = nextId++;
    byKey.set(k, copy);
    added++;
  });
  return {
    words: Array.from(byKey.values()).sort(function (a, b) { return (a.id || 0) - (b.id || 0); }),
    added: added,
  };
}

async function syncVocabFetchServerWords() {
  var r = await fetch('/api/sync/vocabulary', { credentials: 'include' });
  if (r.status === 204) return [];
  if (!r.ok) throw new Error('HTTP ' + r.status);
  var data = await r.json();
  var w = data && data.json && data.json.words;
  return Array.isArray(w) ? w : [];
}

/** Button 1: add words that the app uploaded to the cloud into this page. */
async function syncVocabPullFromMobile() {
  if (!window.__authUser) { showToast(t('sync.signInFirst')); return; }
  try {
    var serverWords = await syncVocabFetchServerWords();
    var merged = vocabMergeAppend(words, serverWords);
    words = merged.words;
    recomputeNextIdFromWords();
    renderVocab();
    updateSidebarCounts();
    try { ytRefreshTranscriptWordClasses(); } catch (e) {}
    schedulePersistVocabulary();
    if (merged.added > 0) {
      showToast(tf('sync.pullAdded', { added: merged.added, total: words.length }));
    } else {
      showToast(t('sync.pullNoNew'));
    }
  } catch (e) {
    console.warn('syncVocabPullFromMobile', e);
    showToast(t('sync.pullFailed'));
  }
}

/** Button 2: merge site words into the cloud so the app can pull them. */
async function syncVocabPushForMobile() {
  if (!window.__authUser) { showToast(t('sync.signInFirst')); return; }
  try {
    var serverWords = await syncVocabFetchServerWords();
    var merged = vocabMergeAppend(serverWords, words);
    var pushR = await fetch('/api/sync/vocabulary', {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ json: { words: merged.words } }),
    });
    if (!pushR.ok) throw new Error('HTTP ' + pushR.status);
    if (merged.added > 0) {
      showToast(tf('sync.pushAdded', { added: merged.added, total: merged.words.length }));
    } else {
      showToast(tf('sync.pushAllInCloud', { total: merged.words.length }));
    }
  } catch (e) {
    console.warn('syncVocabPushForMobile', e);
    showToast(t('sync.pushFailed'));
  }
}
