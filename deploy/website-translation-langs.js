
var TRANSLATION_TARGET_LANG_KEY = 'profconq_translation_target_lang_v1';
var __profileTranslationTargetLang = 2;

function profileTranslationTargetLangToCode(n) {
  return PROFILE_SUBTITLE_LANG_CODES[n] || 'ru';
}

function profileTranslationTargetCodeToLang(code) {
  var c = String(code || 'ru').toLowerCase();
  var i = PROFILE_SUBTITLE_LANG_CODES.indexOf(c);
  return i >= 0 ? i : 2;
}

function profileTranslationFromCode() {
  return profileSubtitleLangToCode(__profileSubtitleLang);
}

function profileTranslationToCode() {
  return profileTranslationTargetLangToCode(__profileTranslationTargetLang);
}

function profileTranslationLangPairBody(extra) {
  var body = { fromLang: profileTranslationFromCode(), toLang: profileTranslationToCode() };
  if (extra && typeof extra === 'object') {
    Object.keys(extra).forEach(function (k) { body[k] = extra[k]; });
  }
  return body;
}

function profileMyMemoryLangPair() {
  return profileTranslationFromCode() + '|' + profileTranslationToCode();
}

function profileSaveTranslationTargetLang() {
  try { localStorage.setItem(TRANSLATION_TARGET_LANG_KEY, String(__profileTranslationTargetLang)); } catch (e) {}
}

function profileSetTranslationFromLang(code) {
  __profileSubtitleLang = Math.max(0, Math.min(2, code | 0));
  profileSaveSubtitleLang();
  profileSyncChipRow('profile-translation-from-chips', __profileSubtitleLang);
  profileSyncYtLangSelect();
  try { profileRefreshStudyLangUi(); } catch (e) {}
  if (__ytCurrentVid) void fetchAndRenderTranscript(__ytCurrentVid);
}

function profileSetTranslationTargetLang(code) {
  __profileTranslationTargetLang = Math.max(0, Math.min(2, code | 0));
  profileSaveTranslationTargetLang();
  profileSyncChipRow('profile-translation-to-chips', __profileTranslationTargetLang);
  try { profileRefreshStudyLangUi(); } catch (e) {}
  if (__transcriptTimedLines && __transcriptTimedLines.length) void prefetchTranscriptGloss(__transcriptTimedLines);
}

function profileSetSubtitleLang(code) {
  profileSetTranslationFromLang(code);
}
