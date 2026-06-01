
function vocabInsertNewWord(payload) {
  var vidNew = __ytCurrentVid || null;
  var vtNew = '';
  if (vidNew) {
    vtNew = (__ytVideoTitle && String(__ytVideoTitle).trim())
      ? String(__ytVideoTitle).trim()
      : ('YouTube · ' + vidNew);
  }
  words.push(Object.assign({
    id: nextId++,
    interval: 1,
    easeFactor: 2.5,
    nextReview: 0,
    reps: 0,
    videoId: vidNew,
    videoTitle: vtNew,
  }, payload));
  renderVocab();
  updateSidebarCounts();
  ytRefreshTranscriptWordClasses();
  refreshVideoDeckChips();
  schedulePersistVocabulary();
  try { renderYtHistory(); } catch (e) {}
}

function vocabQuickAdd() {
  var wEl = document.getElementById('vocab-quick-word');
  var tEl = document.getElementById('vocab-quick-translation');
  if (!wEl || !tEl) return;
  var w = wEl.value.trim();
  var tr = tEl.value.trim();
  if (!w || !tr) {
    showToast(t('vocab.needWordTranslation'));
    wEl.focus();
    return;
  }
  if (!vocabCanAddMoreWords()) {
    vocabShowWordLimitToast();
    return;
  }
  var exEl = document.getElementById('vocab-quick-example');
  var tagEl = document.getElementById('vocab-quick-tag');
  var tag = tagEl ? tagEl.value.trim() : '';
  if (!tag) tag = 'geral';
  var inf = '';
  if (tag === 'verbo') {
    inf = guessPtVerbInfinitivo(w) || '';
  }
  vocabInsertNewWord({
    word: w,
    translation: tr,
    example: exEl ? exEl.value.trim() : '',
    tag: tag,
    img: '',
    infinitivo: inf,
    learnMark: '',
  });
  wEl.value = '';
  tEl.value = '';
  if (exEl) exEl.value = '';
  if (tagEl) tagEl.value = '';
  showToast(t('toast.wordAdded'));
  wEl.focus();
}

function vocabQuickAddKeydown(e) {
  if (e.key !== 'Enter' || e.shiftKey) return;
  if (e.target && e.target.tagName === 'TEXTAREA') return;
  e.preventDefault();
  vocabQuickAdd();
}

function vocabQuickAddRowHtml() {
  return (
    '<tr class="vocab-quick-add-row"><td class="vocab-table-idx" title="' + t('vocab.quickRowTitle') + '">+</td>' +
    '<td class="word-pt"><input type="text" class="form-input" id="vocab-quick-word" placeholder="' + t('vocab.placeholderWord') + '" autocomplete="off" onkeydown="vocabQuickAddKeydown(event)" /></td>' +
    '<td><input type="text" class="form-input" id="vocab-quick-translation" placeholder="' + t('vocab.placeholderTranslation') + '" autocomplete="off" onkeydown="vocabQuickAddKeydown(event)" /></td>' +
    '<td class="vocab-table-col-tag"><select class="form-input vocab-table-editable-select" id="vocab-quick-tag">' +
    '<option value="geral" selected>' + t('vocab.tag.geral') + '</option>' +
    '<option value="substantivo">' + t('vocab.tag.substantivo') + '</option><option value="verbo">' + t('vocab.tag.verbo') + '</option>' +
    '<option value="adjetivo">' + t('vocab.tag.adjetivo') + '</option><option value="frase">' + t('vocab.tag.frase') + '</option>' +
    '</select></td>' +
    '<td class="vocab-table-col-inf"><span style="font-size:10px;color:var(--color-text-faint)">—</span></td>' +
    '<td><input type="text" class="form-input" id="vocab-quick-example" placeholder="' + t('vocab.placeholderExample') + '" autocomplete="off" onkeydown="vocabQuickAddKeydown(event)" /></td>' +
    '<td class="vocab-table-actions"><button type="button" class="btn btn-primary btn-sm" onclick="vocabQuickAdd()"><i data-lucide="plus"></i> ' + t('vocab.quickAddBtn') + '</button></td></tr>'
  );
}
