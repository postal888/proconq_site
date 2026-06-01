#!/usr/bin/env python3
"""Inject toast i18n: UI_STRINGS keys, translateToastLiteral map, patch showToast, dynamic replacements."""
from __future__ import annotations

import json
from pathlib import Path

DIR = Path(__file__).parent
INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
TOASTS_JS = DIR / 'website-i18n-toasts-strings.js'
META = DIR / 'website-i18n-toasts-meta.json'
MARKER = 'translateToastLiteral'


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    meta = json.loads(META.read_text(encoding='utf-8'))

    anchor = 'function showToast(msg) {'
    block = TOASTS_JS.read_text(encoding='utf-8')
    toast_start = '// Toast + error messages'
    if toast_start in html and anchor in html:
        i = html.find(toast_start)
        j = html.find(anchor)
        if i >= 0 and j > i:
            html = html[:i] + block + html[j:]
            print('Refreshed toast i18n block')
    elif MARKER not in html:
        if anchor not in html:
            raise SystemExit('showToast not found')
        html = html.replace(anchor, block + anchor, 1)
        html = html.replace(
            'function showToast(msg) {\n  const t = document.createElement',
            'function showToast(msg) {\n  if (typeof msg === \'string\') msg = translateToastLiteral(msg);\n  const t = document.createElement',
            1,
        )
        print('Injected toast i18n + patched showToast')

    for old, new in meta['dynamic_replacements']:
        if old in html:
            html = html.replace(old, new)
            print('Replaced dynamic:', old[:50])

    # Duplicate hardcoded word limit in main file
    old_limit = (
        "showToast('Лимит ' + FREE_VOCAB_WORD_LIMIT + "
        "' слов (бесплатно). Удалите лишние или оформите Premium.')"
    )
    if old_limit in html:
        html = html.replace(old_limit, 'vocabShowWordLimitToast()')
        print('Fixed inline word limit toast')

    if "showToast(e.message || 'Ошибка перевода')" in html:
        html = html.replace(
            "showToast(e.message || 'Ошибка перевода')",
            "showToast(e.message ? translateToastLiteral(e.message) : t('toast.translationError'))",
        )

    for old, new in [
        ("alert('Заполни слово и перевод!')", "alert(t('vocab.needWordTranslation'))"),
        ("alert('Выбери тип слова')", "alert(t('vocab.pickWordType'))"),
    ]:
        if old in html:
            html = html.replace(old, new)
            print('Replaced alert:', old)

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
