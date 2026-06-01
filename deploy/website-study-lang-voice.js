
function studySpeechLocale(code) {
  var c = String(code || 'pt').toLowerCase();
  if (c === 'en') return 'en-US';
  if (c === 'ru') return 'ru-RU';
  return 'pt-BR';
}

function studyVoiceFieldKind(langKey) {
  if (langKey === 'source' || langKey === 'pt') return 'source';
  return 'target';
}

function studyVoiceTitle(kind) {
  var code = kind === 'source' ? profileTranslationFromCode() : profileTranslationToCode();
  var lang = studyLangDisplayName(code);
  var key = kind === 'source' ? 'study.voiceSource' : 'study.voiceTarget';
  var pattern = t(key);
  if (!pattern || pattern === key) return lang;
  return pattern.replace(/\{lang\}/g, lang).replace(/\{short\}/g, studyLangShort(code));
}

function studyTtsTitle(kind) {
  var code = kind === 'source' ? profileTranslationFromCode() : profileTranslationToCode();
  var key = kind === 'source' ? 'study.ttsSource' : 'study.ttsTarget';
  var pattern = t(key);
  if (!pattern || pattern === key) return studyLangShort(code);
  return pattern.replace(/\{short\}/g, studyLangShort(code)).replace(/\{lang\}/g, studyLangDisplayName(code));
}

function speakFlashcardForSide(side, mode) {
  if (!window.speechSynthesis) return;
  var w = fcQueue[fcIndex];
  if (!w) return;
  speechSynthesis.cancel();
  var isSource = side === 'source';
  var code = isSource ? profileTranslationFromCode() : profileTranslationToCode();
  var text = isSource
    ? ((mode === 'example' && w.example && String(w.example).trim()) ? String(w.example).trim() : String(w.word || '').trim())
    : String(w.translation || '').trim();
  if (!text) return;
  var u = new SpeechSynthesisUtterance(text);
  u.lang = studySpeechLocale(code);
  var v = fcPickVoice(String(code).toLowerCase());
  if (v) u.voice = v;
  u.rate = isSource ? 0.92 : 0.95;
  speechSynthesis.speak(u);
}

function speakFlashcardPortuguese(mode) {
  speakFlashcardForSide('source', mode);
}

function speakFlashcardRussian() {
  speakFlashcardForSide('target');
}

function startVoiceField(langKey, ev) {
  if (ev && ev.preventDefault) ev.preventDefault();
  var C = getSpeechRecognitionCtor();
  if (!C) {
    alert(t('voice.unavailable') || 'Voice input unavailable. Use Chrome or Edge and allow microphone access.');
    return;
  }
  var kind = studyVoiceFieldKind(langKey);
  var code = kind === 'source' ? profileTranslationFromCode() : profileTranslationToCode();
  var btnId = kind === 'source' ? 'voice-mic-source' : 'voice-mic-target';
  var legacyBtnId = kind === 'source' ? 'voice-mic-pt' : 'voice-mic-ru';
  var btn = document.getElementById(btnId) || document.getElementById(legacyBtnId);
  if (__speechRec && __voiceActiveBtn === btn) {
    stopVoiceInput();
    setVoiceStatus('');
    return;
  }
  stopVoiceInput();
  var rec = new C();
  rec.lang = studySpeechLocale(code);
  rec.interimResults = false;
  rec.maxAlternatives = 1;
  rec.continuous = false;
  __speechRec = rec;
  __voiceActiveBtn = btn;
  if (btn) btn.classList.add('recording');
  setVoiceStatus(t('voice.listening') || 'Listening…');

  rec.onresult = function (e) {
    var text = '';
    try {
      text = (e.results[0] && e.results[0][0]) ? e.results[0][0].transcript.trim() : '';
    } catch (err) {}
    if (kind === 'source') document.getElementById('input-word').value = text;
    else document.getElementById('input-translation').value = text;
    setVoiceStatus(t('voice.done') || 'Done. Check and tap Add.');
  };
  rec.onerror = function (e) {
    var err = e.error || '';
    setVoiceStatus(
      err === 'not-allowed'
        ? (t('voice.micDenied') || 'Microphone denied — allow access in site settings.')
        : (t('voice.error') || 'Error: ') + err,
      true,
    );
  };
  rec.onend = function () {
    if (__voiceActiveBtn) __voiceActiveBtn.classList.remove('recording');
    __voiceActiveBtn = null;
    __speechRec = null;
  };
  try { rec.start(); } catch (err) {
    setVoiceStatus(t('voice.startFailed') || 'Could not start voice input.', true);
    if (btn) btn.classList.remove('recording');
    __voiceActiveBtn = null;
    __speechRec = null;
  }
}
