#!/usr/bin/env python3
"""Replace single YouTube subtitle language with From/To translation language selectors."""
from __future__ import annotations

from pathlib import Path

DIR = Path(__file__).parent
INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PROFILE = DIR / 'website-translation-langs-profile.html'
JS = DIR / 'website-translation-langs.js'
I18N = DIR / 'website-translation-langs-i18n.js'
FN_MARKER = 'function profileSetTranslationFromLang'


def replace_profile_html(html: str) -> str:
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
        raise SystemExit('Profile subtitle/translation block not found')
    # walk back to profile-setting-block
    block_start = html.rfind('<div class="profile-setting-block">', 0, start)
    if block_start < 0:
        raise SystemExit('profile-setting-block start not found')
    block_end = html.find('<div class="profile-setting-divider"></div>', start)
    if block_end < 0:
        raise SystemExit('profile block end not found')
    profile = PROFILE.read_text(encoding='utf-8')
    return html[:block_start] + profile + html[block_end:]


def inject_js(html: str) -> str:
    if FN_MARKER in html:
        print('Translation handlers already injected')
        return html
    anchor = 'function profileSubtitleCodeToLang(code) {'
    if anchor not in html:
        raise SystemExit('profileSubtitleCodeToLang not found')
    block = JS.read_text(encoding='utf-8')
    i = html.find(anchor)
    j = html.find('\n}', i)
    if j < 0:
        raise SystemExit('end of profileSubtitleCodeToLang not found')
    j = html.find('\n', j + 2)
    return html[:j] + '\n' + block + html[j:]


def inject_i18n(html: str) -> str:
    marker = 'profile.translationLangs'
    if marker in html and 'website-translation-langs-i18n' in html:
        return html
    anchor = 'function t(key) {'
    block = I18N.read_text(encoding='utf-8')
    if anchor not in html:
        raise SystemExit('t() not found')
    return html.replace(anchor, block + '\n' + anchor, 1)


def patch_load_prefs(html: str) -> str:
    old = "  try {\n    var sf = parseInt(localStorage.getItem(SUBTITLE_FONT_KEY), 10);"
    insert = (
        "  try {\n"
        "    var tgt = localStorage.getItem(TRANSLATION_TARGET_LANG_KEY);\n"
        "    if (tgt === '0' || tgt === '1' || tgt === '2' || tgt === '3') __profileTranslationTargetLang = parseInt(tgt, 10);\n"
        "    else if (tgt && PROFILE_SUBTITLE_LANG_CODES.indexOf(String(tgt).toLowerCase()) >= 0) __profileTranslationTargetLang = profileTranslationTargetCodeToLang(tgt);\n"
        "  } catch (eTgt) {}\n"
        "  try {\n"
        "    var sf = parseInt(localStorage.getItem(SUBTITLE_FONT_KEY), 10);"
    )
    if 'TRANSLATION_TARGET_LANG_KEY' in html.split('function loadProfilePrefs')[1][:1200]:
        return html
    if old not in html:
        print('WARN: loadProfilePrefs anchor not found')
        return html
    return html.replace(old, insert, 1)


def patch_sync_ui(html: str) -> str:
    html = html.replace(
        "profileSyncChipRow('profile-subtitle-lang-chips', __profileSubtitleLang);",
        "profileSyncChipRow('profile-translation-from-chips', __profileSubtitleLang);\n"
        "  profileSyncChipRow('profile-translation-to-chips', __profileTranslationTargetLang);",
    )
    # Remove duplicate profileSetSubtitleLang body if still old inline version
    old_fn = """function profileSetSubtitleLang(code) {
  __profileSubtitleLang = Math.max(0, Math.min(3, code | 0));
  profileSaveSubtitleLang();
  profileSyncChipRow('profile-subtitle-lang-chips', __profileSubtitleLang);
  profileSyncYtLangSelect();
  if (__ytCurrentVid) void fetchAndRenderTranscript(__ytCurrentVid);
}"""
    if old_fn in html:
        html = html.replace(old_fn, '', 1)
    old_on_yt = "profileSyncChipRow('profile-subtitle-lang-chips', __profileSubtitleLang);"
    html = html.replace(old_on_yt, "profileSyncChipRow('profile-translation-from-chips', __profileSubtitleLang);", 1)
    return html


def patch_settings_keys(html: str) -> str:
    old = "'profconq_subtitle_lang_v1', 'profconq_phrase_copy_v1',"
    new = "'profconq_subtitle_lang_v1', 'profconq_translation_target_lang_v1', 'profconq_phrase_copy_v1',"
    if new in html:
        return html
    return html.replace(old, new, 1)


def patch_api_calls(html: str) -> str:
    reps = [
        ("body: JSON.stringify({ words: [clean] })", "body: JSON.stringify(profileTranslationLangPairBody({ words: [clean] }))"),
        ("body: JSON.stringify({ words: [w] })", "body: JSON.stringify(profileTranslationLangPairBody({ words: [w] }))"),
        ("body: JSON.stringify({ words: batch })", "body: JSON.stringify(profileTranslationLangPairBody({ words: batch }))"),
        ("body: JSON.stringify({ words: uniq })", "body: JSON.stringify(profileTranslationLangPairBody({ words: uniq }))"),
        ("body: JSON.stringify({ words: need.slice(0, 500) })", "body: JSON.stringify(profileTranslationLangPairBody({ words: need.slice(0, 500) }))"),
        (
            "encodeURIComponent(chunk) + '&langpair=pt|ru'",
            "encodeURIComponent(chunk) + '&langpair=' + profileMyMemoryLangPair()",
        ),
        (
            "body: JSON.stringify({ text: text.slice(0, 12000) })",
            "body: JSON.stringify(profileTranslationLangPairBody({ text: text.slice(0, 12000) }))",
        ),
    ]
    for old, new in reps:
        if old in html:
            html = html.replace(old, new)
            print('Patched API call:', old[:50])
    return html


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = replace_profile_html(html)
    print('Updated profile HTML')
    html = inject_js(html)
    print('Injected translation lang JS')
    html = inject_i18n(html)
    print('Injected i18n strings')
    html = patch_load_prefs(html)
    html = patch_sync_ui(html)
    html = patch_settings_keys(html)
    html = patch_api_calls(html)
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
