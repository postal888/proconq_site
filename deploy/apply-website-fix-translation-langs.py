#!/usr/bin/env python3
"""Re-inject missing translation language handler functions."""
from __future__ import annotations

from pathlib import Path

DIR = Path(__file__).parent
INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
JS = DIR / 'website-translation-langs.js'
FN_MARKER = 'function profileSetTranslationFromLang'


def inject_js(html: str) -> str:
    if FN_MARKER in html:
        print('Handler functions already present')
        return html
    if 'onclick="profileSetTranslationFromLang(0)"' not in html:
        raise SystemExit('Translation lang HTML not found — run apply-website-translation-langs.py first')
    anchor = 'function profileSubtitleCodeToLang(code) {'
    if anchor not in html:
        raise SystemExit('profileSubtitleCodeToLang not found')
    block = JS.read_text(encoding='utf-8')
    i = html.find(anchor)
    j = html.find('\n}', i)
    if j < 0:
        raise SystemExit('profileSubtitleCodeToLang end not found')
    j = html.find('\n', j + 2)
    print('Injecting translation lang handlers')
    return html[:j] + '\n' + block + html[j:]


def fix_profile_set_subtitle_lang(html: str) -> str:
    old = """function profileSetSubtitleLang(code) {
  __profileSubtitleLang = Math.max(0, Math.min(3, code | 0));
  profileSaveSubtitleLang();
  profileSyncChipRow('profile-translation-from-chips', __profileSubtitleLang);
  profileSyncChipRow('profile-translation-to-chips', __profileTranslationTargetLang);
  profileSyncYtLangSelect();
  if (__ytCurrentVid) void fetchAndRenderTranscript(__ytCurrentVid);
}"""
    new = """function profileSetSubtitleLang(code) {
  profileSetTranslationFromLang(code);
}"""
    if old in html:
        html = html.replace(old, new, 1)
        print('Fixed profileSetSubtitleLang wrapper')
    elif 'function profileSetSubtitleLang(code) {\n  profileSetTranslationFromLang(code);' in html:
        print('profileSetSubtitleLang already a wrapper')
    else:
        print('WARN: unexpected profileSetSubtitleLang — check manually')
    return html


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = inject_js(html)
    html = fix_profile_set_subtitle_lang(html)
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
