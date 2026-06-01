
function studyLangShort(code) {
  var c = String(code || 'pt').toLowerCase();
  if (c === 'en') return 'EN';
  if (c === 'ru') return 'RU';
  return 'PT';
}

function studyLangDisplayName(code) {
  var c = String(code || 'pt').toLowerCase();
  var key = 'study.lang.' + c;
  var name = t(key);
  return name && name !== key ? name : studyLangShort(c);
}

function studyDirLabel(fromCode, toCode) {
  return studyLangShort(fromCode) + ' \u2192 ' + studyLangShort(toCode);
}

function studyDirLabelForward() {
  return studyDirLabel(profileTranslationFromCode(), profileTranslationToCode());
}

function studyDirLabelReversed() {
  return studyDirLabel(profileTranslationToCode(), profileTranslationFromCode());
}

function studyFieldLabel(kind) {
  var from = profileTranslationFromCode();
  var to = profileTranslationToCode();
  var lang = kind === 'translation' ? studyLangDisplayName(to) : studyLangDisplayName(from);
  var short = kind === 'translation' ? studyLangShort(to) : studyLangShort(from);
  var patternKey = kind === 'translation' ? 'study.fieldTranslation' : (kind === 'inf' ? 'study.fieldInf' : 'study.fieldWord');
  var pattern = t(patternKey);
  if (!pattern || pattern === patternKey) {
    if (kind === 'translation') return (t('vocab.colTranslation') || 'Translation') + ' (' + short + ')';
    return studyLangDisplayName(from) + ' (' + short + ')';
  }
  return pattern.replace(/\{lang\}/g, lang).replace(/\{short\}/g, short);
}

function studyPlaceholderWord() {
  var pattern = t('study.placeholderWord');
  var short = studyLangShort(profileTranslationFromCode());
  if (!pattern || pattern === 'study.placeholderWord') return t('vocab.placeholderWord') || short;
  return pattern.replace(/\{short\}/g, short);
}

function studyPlaceholderTranslation() {
  var pattern = t('study.placeholderTranslation');
  var short = studyLangShort(profileTranslationToCode());
  if (!pattern || pattern === 'study.placeholderTranslation') return t('vocab.placeholderTranslation') || short;
  return pattern.replace(/\{short\}/g, short);
}

function vocabColWordLabel() {
  return studyLangDisplayName(profileTranslationFromCode());
}

function vocabColTranslationLabel() {
  return studyLangDisplayName(profileTranslationToCode());
}

function programsRefreshDirLabel() {
  var span = document.querySelector('.fc-dir-toggle span');
  if (!span) return;
  var reversed = window.__fcDir === 'ru2pt';
  span.textContent = reversed ? studyDirLabelReversed() : studyDirLabelForward();
}

function profileRefreshStudyLangUi() {
  var fromCode = profileTranslationFromCode();
  var toCode = profileTranslationToCode();
  var el = document.getElementById('input-word-label');
  if (el) el.textContent = studyFieldLabel('word');
  document.querySelectorAll('[data-study-lang="translation"]').forEach(function (node) {
    node.textContent = studyFieldLabel('translation');
  });
  document.querySelectorAll('[data-study-lang="translationCol"]').forEach(function (node) {
    node.textContent = studyFieldLabel('translation');
  });
  document.querySelectorAll('[data-study-lang="sourceCol"]').forEach(function (node) {
    node.textContent = studyLangDisplayName(fromCode);
  });
  document.querySelectorAll('[data-study-lang="sourceShort"]').forEach(function (node) {
    node.textContent = studyLangShort(fromCode);
  });
  document.querySelectorAll('[data-study-lang="targetShort"]').forEach(function (node) {
    node.textContent = studyLangShort(toCode);
  });
  var hint = document.querySelector('[data-study-lang="importHint"]');
  if (hint) {
    var fromName = studyLangDisplayName(fromCode);
    var toName = studyLangDisplayName(toCode);
    var fromShort = studyLangShort(fromCode);
    var toShort = studyLangShort(toCode);
    var p = t('study.importHint');
    if (p && p !== 'study.importHint') {
      hint.textContent = p
        .replace(/\{from\}/g, fromName)
        .replace(/\{to\}/g, toName)
        .replace(/\{fromShort\}/g, fromShort)
        .replace(/\{toShort\}/g, toShort);
    }
  }
  document.querySelectorAll('[data-study-lang="inf"]').forEach(function (node) {
    node.textContent = studyFieldLabel('inf');
  });
  ['source', 'target'].forEach(function (kind) {
    var mic = document.getElementById(kind === 'source' ? 'voice-mic-source' : 'voice-mic-target');
    if (mic) mic.title = studyVoiceTitle(kind);
    var tts = document.getElementById(kind === 'source' ? 'fc-tts-source' : 'fc-tts-target');
    if (tts) tts.title = studyTtsTitle(kind);
  });
  try { programsRefreshDirLabel(); } catch (e) {}
  var activeView = document.querySelector('.view.active');
  if (activeView && activeView.id === 'view-vocab' && typeof renderVocab === 'function') renderVocab();
}
