#!/usr/bin/env python3
"""Simplify translation language UI: two pickers, hint 'choose 2 languages'."""
from __future__ import annotations

import re
from pathlib import Path

DIR = Path(__file__).parent
INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PROFILE = DIR / 'website-translation-langs-profile.html'
I18N = DIR / 'website-translation-langs-i18n.js'

HINTS = {
    'ru': 'Выберите 2 языка.',
    'en': 'Choose 2 languages.',
    'pt': 'Escolha 2 idiomas.',
}


def replace_profile_block(html: str) -> str:
    start = html.find('<div class="profile-setting-label" data-i18n="profile.translationLangs">')
    if start < 0:
        raise SystemExit('translation langs block not found')
    block_start = html.rfind('<div class="profile-setting-block">', 0, start)
    block_end = html.find('<div class="profile-setting-divider"></div>', start)
    if block_start < 0 or block_end < 0:
        raise SystemExit('profile block boundaries not found')
    return html[:block_start] + PROFILE.read_text(encoding='utf-8') + html[block_end:]


def patch_hints_in_ui_strings(html: str) -> str:
    reps = [
        ("'profile.translationLangsHint': 'Субтитры YouTube — на языке «С». Перевод при наведении и в словаре — «С» → «На».'", f"'profile.translationLangsHint': '{HINTS['ru']}'"),
        ("'profile.translationLangsHint': 'YouTube subtitles use “From”. Tap-to-translate and dictionary use From → To.'", f"'profile.translationLangsHint': '{HINTS['en']}'"),
        ("'profile.translationLangsHint': 'Legendas do YouTube no idioma «De». Tradução ao passar o mouse e no dicionário: De → Para.'", f"'profile.translationLangsHint': '{HINTS['pt']}'"),
    ]
    for old, new in reps:
        if old in html:
            html = html.replace(old, new, 1)
    html = re.sub(r"\s*'profile\.translationFrom': '[^']*',\n", '\n', html)
    html = re.sub(r"\s*'profile\.translationTo': '[^']*',\n", '\n', html)
    return html


def inject_i18n_override(html: str) -> str:
    marker = '// Card / subtitle — two language pickers'
    block = I18N.read_text(encoding='utf-8')
    if marker in html:
        i = html.find(marker)
        j = html.find('})();', i)
        if j > i:
            j = html.find('\n', j + 4)
            html = html[:i] + block.strip() + '\n\n' + html[j:].lstrip()
            return html
    anchor = 'function t(key) {'
    if anchor not in html:
        return html
    return html.replace(anchor, block + '\n' + anchor, 1)


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = replace_profile_block(html)
    print('Updated profile HTML (two pickers, no From/To labels)')
    html = patch_hints_in_ui_strings(html)
    print('Updated translationLangsHint in UI_STRINGS')
    html = inject_i18n_override(html)
    print('Refreshed i18n override block')
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
