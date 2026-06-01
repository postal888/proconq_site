#!/usr/bin/env python3
"""Remove Spanish (ES), keep PT/EN/RU only, wire dynamic study-language labels."""
from __future__ import annotations

import re
from pathlib import Path

DIR = Path(__file__).parent
INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PROFILE = DIR / 'website-translation-langs-profile.html'
LANG_JS = DIR / 'website-study-lang-labels.js'
LANG_I18N = DIR / 'website-study-lang-labels-i18n.js'
TRANSLATION_JS = DIR / 'website-translation-langs.js'


def replace_profile_block(html: str) -> str:
    starts = [
        '<div class="profile-setting-label" data-i18n="profile.subtitleLang">',
        '<div class="profile-setting-label" data-i18n="profile.translationLangs">',
    ]
    start = -1
    for s in starts:
        start = html.find(s)
        if start >= 0:
            break
    if start < 0:
        print('Profile translation block not found — skipping HTML replace')
        return html
    block_start = html.rfind('<div class="profile-setting-block">', 0, start)
    block_end = html.find('<div class="profile-setting-divider"></div>', start)
    if block_start < 0 or block_end < 0:
        print('Profile block boundaries not found')
        return html
    return html[:block_start] + PROFILE.read_text(encoding='utf-8') + html[block_end:]


def patch_codes_and_clamp(html: str) -> str:
    html = html.replace(
        "var PROFILE_SUBTITLE_LANG_CODES = ['pt', 'en', 'ru', 'es'];",
        "var PROFILE_SUBTITLE_LANG_CODES = ['pt', 'en', 'ru'];",
    )
    html = html.replace('Math.min(3, code | 0)', 'Math.min(2, code | 0)')
    html = html.replace(
        "if (raw === '0' || raw === '1' || raw === '2' || raw === '3') __profileSubtitleLang = parseInt(raw, 10);",
        "if (raw === '0' || raw === '1' || raw === '2') __profileSubtitleLang = parseInt(raw, 10);",
    )
    html = html.replace(
        "if (tgt === '0' || tgt === '1' || tgt === '2' || tgt === '3') __profileTranslationTargetLang = parseInt(tgt, 10);",
        "if (tgt === '0' || tgt === '1' || tgt === '2') __profileTranslationTargetLang = parseInt(tgt, 10);",
    )
    anchor = '  try {\n    var sf = parseInt(localStorage.getItem(SUBTITLE_FONT_KEY), 10);'
    clamp = (
        '  __profileSubtitleLang = Math.max(0, Math.min(2, __profileSubtitleLang | 0));\n'
        '  __profileTranslationTargetLang = Math.max(0, Math.min(2, __profileTranslationTargetLang | 0));\n'
    )
    if clamp.strip() not in html and anchor in html:
        html = html.replace(anchor, clamp + anchor, 1)
    return html


def remove_es_yt_lang(html: str) -> str:
    return re.sub(
        r'\s*<option value="es">Español</option>\s*',
        '\n',
        html,
        count=1,
    )


def patch_vocab_labels(html: str) -> str:
    old = "t('vocab.colWord'), t('vocab.colTranslation')"
    new = 'vocabColWordLabel(), vocabColTranslationLabel()'
    if old in html:
        html = html.replace(old, new)
    return html


def patch_programs_dir(html: str) -> str:
    old = """    var dirLabel = reversed
      ? (t('programs.dirRuPt') || 'RU → PT')
      : (t('programs.dirPtRu') || 'PT → RU');"""
    new = """    var dirLabel = reversed ? studyDirLabelReversed() : studyDirLabelForward();"""
    if old in html:
        return html.replace(old, new)
    if 'studyDirLabelForward()' in html:
        print('Programs dir already patched')
    else:
        print('WARN: programs dir block not found')
    return html


def patch_apply_ui_language(html: str) -> str:
    old = """  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    var key = el.getAttribute('data-i18n');
    if (!key) return;
    el.textContent = t(key);
  });"""
    new = """  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    if (el.hasAttribute('data-study-lang')) return;
    var key = el.getAttribute('data-i18n');
    if (!key) return;
    el.textContent = t(key);
  });
  try { profileRefreshStudyLangUi(); } catch (eStudy) {}"""
    if 'profileRefreshStudyLangUi()' in html.split('function applyUiLanguage')[1][:600]:
        return html
    if old not in html:
        print('WARN: applyUiLanguage block not found')
        return html
    return html.replace(old, new, 1)


def patch_vocab_form_attrs(html: str) -> str:
    html = html.replace(
        '<label class="form-label" data-i18n="vocab.fieldTranslation">',
        '<label class="form-label" data-study-lang="translation" data-i18n="vocab.fieldTranslation">',
    )
    html = html.replace(
        '<label class="form-label" data-i18n="vocab.fieldInf">',
        '<label class="form-label" data-study-lang="inf" data-i18n="vocab.fieldInf">',
    )
    html = html.replace(
        'data-i18n="vocab.importHint">',
        'data-study-lang="importHint" data-i18n="vocab.importHint">',
    )
    return html


def patch_vocab_quick_row(html: str) -> str:
    old = (
        "placeholder=\"' + t('vocab.placeholderWord') + '\""
    )
    new = (
        "placeholder=\"' + studyPlaceholderWord() + '\""
    )
    if old in html:
        html = html.replace(old, new)
    old2 = (
        "placeholder=\"' + t('vocab.placeholderTranslation') + '\""
    )
    new2 = (
        "placeholder=\"' + studyPlaceholderTranslation() + '\""
    )
    if old2 in html:
        html = html.replace(old2, new2)
    # Undo accidental replace inside studyPlaceholder* definitions
    html = html.replace(
        "if (!pattern || pattern === 'study.placeholderWord') return studyPlaceholderWord() || short;",
        "if (!pattern || pattern === 'study.placeholderWord') return t('vocab.placeholderWord') || short;",
    )
    html = html.replace(
        "if (!pattern || pattern === 'study.placeholderTranslation') return studyPlaceholderTranslation() || short;",
        "if (!pattern || pattern === 'study.placeholderTranslation') return t('vocab.placeholderTranslation') || short;",
    )
    return html


def patch_enter_word_toast(html: str) -> str:
    old = "showToast('Сначала введите слово или фразу (PT)');"
    new = """showToast(
      (t('toast.enterWordOrPhraseFirst') || 'Enter word ({short}) first')
        .replace(/\{short\}/g, studyLangShort(profileTranslationFromCode()))
    );"""
    if old in html:
        html = html.replace(old, new)
    return html


def inject_study_lang_js(html: str) -> str:
    marker = 'function studyLangShort(code)'
    if marker in html:
        print('Study lang labels already injected')
        return html
    block = LANG_JS.read_text(encoding='utf-8')
    anchor = 'function profileSubtitleLangToCode(n) {'
    if anchor not in html:
        raise SystemExit('profileSubtitleLangToCode not found')
    return html.replace(anchor, block + '\n' + anchor, 1)


def inject_study_lang_i18n(html: str) -> str:
    marker = "'study.lang.pt'"
    if marker in html:
        print('Study lang i18n already injected')
        return html
    block = LANG_I18N.read_text(encoding='utf-8')
    anchor = 'function t(key) {'
    if anchor not in html:
        raise SystemExit('t() not found')
    return html.replace(anchor, block + '\n' + anchor, 1)


def refresh_translation_handlers(html: str) -> str:
    """Replace profileSetTranslation* bodies with latest from website-translation-langs.js."""
    start = html.find('function profileSetTranslationFromLang(code) {')
    end = html.find('function profileSetSubtitleLang(code) {')
    if start < 0 or end < 0:
        print('Translation handler block not found')
        return html
    block = TRANSLATION_JS.read_text(encoding='utf-8')
    fn_start = block.find('function profileSetTranslationFromLang(code) {')
    fn_end = block.find('function profileSetSubtitleLang(code) {')
    if fn_start < 0 or fn_end < 0:
        return html
    handlers = block[fn_start:fn_end]
    return html[:start] + handlers + html[end:]


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = replace_profile_block(html)
    html = patch_codes_and_clamp(html)
    html = remove_es_yt_lang(html)
    html = inject_study_lang_i18n(html)
    html = inject_study_lang_js(html)
    html = refresh_translation_handlers(html)
    html = patch_vocab_labels(html)
    html = patch_programs_dir(html)
    html = patch_apply_ui_language(html)
    html = patch_vocab_form_attrs(html)
    html = patch_vocab_quick_row(html)
    html = patch_enter_word_toast(html)
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
