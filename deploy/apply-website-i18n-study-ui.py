#!/usr/bin/env python3
"""Dynamic study-lang UI (textgen, books, voice, TTS) + voice i18n + data-i18n-title."""
from __future__ import annotations

import re
from pathlib import Path

DIR = Path(__file__).parent
INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
LABELS_JS = DIR / 'website-study-lang-labels.js'
LABELS_I18N = DIR / 'website-study-lang-labels-i18n.js'
VOICE_JS = DIR / 'website-study-lang-voice.js'
TITLES_I18N = DIR / 'website-i18n-titles-strings.js'


def replace_block(html: str, start_marker: str, end_marker: str, new_block: str) -> str:
    i = html.find(start_marker)
    if i < 0:
        return html
    j = html.find(end_marker, i + len(start_marker))
    if j < 0:
        return html
    return html[:i] + new_block + html[j:]


def refresh_study_labels(html: str) -> str:
    block = LABELS_JS.read_text(encoding='utf-8')
    start = 'function studyLangShort(code) {'
    end = '\nfunction profileSubtitleLangToCode(n) {'
    if start not in html:
        raise SystemExit('studyLangShort not found')
    return replace_block(html, start, end, block.rstrip() + '\n\n', )


def refresh_study_i18n(html: str) -> str:
    block = LABELS_I18N.read_text(encoding='utf-8')
    start = "(function () {\n  if (typeof UI_STRINGS === 'undefined') return;\n  var extra = {"
    # find the study.lang.pt block specifically
    idx = html.find("'study.lang.pt'")
    if idx < 0:
        raise SystemExit('study.lang.pt i18n not found')
    i = html.rfind('(function () {', 0, idx)
    j = html.find('})();', idx)
    if i < 0 or j < 0:
        raise SystemExit('study i18n IIFE bounds not found')
    j = html.find('\n', j + 5)
    return html[:i] + block.rstrip() + '\n' + html[j:]


def patch_html_elements(html: str) -> str:
    html = html.replace(
        '<div class="textgen-out-head"><span>Португальский</span>',
        '<div class="textgen-out-head"><span data-study-lang="sourceCol">Portuguese</span>',
    )
    html = html.replace(
        '<div class="textgen-out-head"><span>Перевод (RU)</span>',
        '<div class="textgen-out-head"><span data-study-lang="translationCol">Translation</span>',
    )
    html = html.replace(
        '<div class="books-panel-h">Перевод (RU)</div>',
        '<div class="books-panel-h" data-study-lang="translationCol">Translation</div>',
    )
    html = html.replace(
        'id="voice-mic-pt" onclick="startVoiceField(\'pt\', event)" title="Голосом (португальский)"',
        'id="voice-mic-source" onclick="startVoiceField(\'source\', event)" title="Voice"',
    )
    html = html.replace(
        'id="voice-mic-ru" onclick="startVoiceField(\'ru\', event)" title="Голосом (русский)"',
        'id="voice-mic-target" onclick="startVoiceField(\'target\', event)" title="Voice"',
    )
    old_fc = (
        '<button type="button" class="fc-tts-btn fc-tts-wide" title="Португальский: пример или слово" '
        'onclick="event.stopPropagation(); speakFlashcardPortuguese(\'example\')"><i data-lucide="volume-2"></i> PT</button>\n'
        '                    <button type="button" class="fc-tts-btn fc-tts-wide" title="Перевод по-русски" '
        'onclick="event.stopPropagation(); speakFlashcardRussian()"><i data-lucide="volume-2"></i> RU</button>'
    )
    new_fc = (
        '<button type="button" class="fc-tts-btn fc-tts-wide" id="fc-tts-source" title="TTS source" '
        'onclick="event.stopPropagation(); speakFlashcardPortuguese(\'example\')">'
        '<i data-lucide="volume-2"></i> <span data-study-lang="sourceShort">PT</span></button>\n'
        '                    <button type="button" class="fc-tts-btn fc-tts-wide" id="fc-tts-target" title="TTS target" '
        'onclick="event.stopPropagation(); speakFlashcardRussian()">'
        '<i data-lucide="volume-2"></i> <span data-study-lang="targetShort">RU</span></button>'
    )
    if old_fc in html:
        html = html.replace(old_fc, new_fc)
    return html


def inject_voice_handlers(html: str) -> str:
    raw = VOICE_JS.read_text(encoding='utf-8')
    helpers_end = raw.find('function speakFlashcardPortuguese(mode)')
    helpers = raw[:helpers_end].rstrip() + '\n\n'
    fc_block = raw[helpers_end:].rstrip() + '\n\n'

    if 'function studySpeechLocale(code)' not in html:
        anchor = 'function speakFlashcardPortuguese(mode) {'
        if anchor not in html:
            raise SystemExit('speakFlashcardPortuguese not found')
        html = html.replace(anchor, helpers + anchor, 1)
        print('Injected speech helpers')

    fc_start = 'function speakFlashcardPortuguese(mode) {'
    fc_end = '\nif (window.speechSynthesis) {'
    fc_only_end = "function speakFlashcardRussian() {\n  speakFlashcardForSide('target');\n}\n"
    if fc_start in html and 'function speakFlashcardForSide(side, mode)' not in html.split(fc_start)[1][:200]:
        fc_block_trimmed = fc_block.split("function startVoiceField(langKey, ev) {")[0]
        html = replace_block(html, fc_start, fc_end, fc_block_trimmed, )
        print('Replaced flashcard speech handlers')

    sv_start = 'function startVoiceField(langKey, ev) {'
    sv_end = '\nfunction startVoicePhraseBoth(ev) {'
    if sv_start in html and 'studyVoiceFieldKind(langKey)' not in html.split(sv_start)[1][:300]:
        # extract startVoiceField from voice js
        sv_block_start = raw.find(sv_start)
        sv_block = raw[sv_block_start:].rstrip() + '\n'
        html = replace_block(html, sv_start, sv_end, sv_block, )
        print('Replaced startVoiceField')
    return html


def patch_start_voice_if_left(html: str) -> str:
    return html


def patch_copy_toast(html: str) -> str:
    old = "showToast('Скопировано')"
    new = "showToast(t('toast.copied') || 'Copied')"
    return html.replace(old, new)


def patch_apply_ui_language(html: str) -> str:
    needle = "  try { profileRefreshStudyLangUi(); } catch (eStudy) {}"
    extra = """
  document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
    var key = el.getAttribute('data-i18n-title');
    if (key) el.title = t(key);
  });"""
    if '[data-i18n-title]' in html.split('function applyUiLanguage')[1][:800]:
        return html
    if needle not in html:
        print('WARN: applyUiLanguage needle not found')
        return html
    return html.replace(needle, extra + '\n' + needle, 1)


def inject_titles_i18n(html: str) -> str:
    if 'ui.title.undoDelete' in html:
        print('Title i18n already injected')
        return html
    block = TITLES_I18N.read_text(encoding='utf-8')
    anchor = 'function t(key) {'
    if anchor not in html:
        raise SystemExit('t() not found')
    return html.replace(anchor, block + '\n' + anchor, 1)


def patch_title_attrs(html: str) -> str:
    pairs = [
        ('id="undo-delete-btn"', 'data-i18n-title="ui.title.undoDelete"'),
        ('id="vocab-font-size-select"', 'data-i18n-title="ui.title.vocabFontSize"'),
        ('id="vocab-font-family-select"', 'data-i18n-title="ui.title.vocabFont"'),
        ('id="vocab-table-speak-btn"', 'data-i18n-title="ui.title.speakSelected"'),
        ('id="vocab-table-stop-tts-btn"', 'data-i18n-title="ui.title.stopTts"'),
        ('id="yt-lang"', 'data-i18n-title="ui.title.ytLang"'),
        ('id="hover-translate-source"', 'data-i18n-title="ui.title.hoverTranslate"'),
        ('id="addword-auto-translation-btn"', 'data-i18n-title="ui.title.autoTranslate"'),
    ]
    for needle, attr in pairs:
        if attr in html:
            continue
        idx = html.find(needle)
        if idx < 0:
            continue
        tag_start = html.rfind('<', 0, idx)
        tag_end = html.find('>', idx)
        if tag_start < 0 or tag_end < 0:
            continue
        tag = html[tag_start:tag_end + 1]
        if attr in tag:
            continue
        html = html[:tag_end] + ' ' + attr + html[tag_end:]
    return html


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = refresh_study_labels(html)
    html = refresh_study_i18n(html)
    html = patch_html_elements(html)
    html = inject_voice_handlers(html)
    html = patch_start_voice_if_left(html)
    html = patch_copy_toast(html)
    html = inject_titles_i18n(html)
    html = patch_title_attrs(html)
    html = patch_apply_ui_language(html)
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
