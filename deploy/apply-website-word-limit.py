#!/usr/bin/env python3
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
JS = Path('/var/www/proficonq/tutor-app/patches/website-word-limit.js')
MARKER = 'FREE_VOCAB_WORD_LIMIT'


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    if MARKER in html:
        print('Already patched')
        return
    js = JS.read_text(encoding='utf-8')
    anchor = 'function vocabInsertNewWord(payload) {'
    if anchor not in html:
        raise SystemExit('vocabInsertNewWord not found')
    html = html.replace(anchor, js + '\n' + anchor, 1)

    check = (
        '  words.push(Object.assign({\n'
        '    id: nextId++,'
    )
    insert = (
        '  if (!vocabCanAddMoreWords()) {\n'
        '    vocabShowWordLimitToast();\n'
        '    return;\n'
        '  }\n'
        '  words.push(Object.assign({\n'
        '    id: nextId++,'
    )
    if check in html:
        html = html.replace(check, insert, 1)

    save_anchor = "  if (!w || !t) { alert('Заполни слово и перевод!'); return; }"
    save_insert = (
        "  if (!vocabCanAddMoreWords() && !editingId) {\n"
        '    vocabShowWordLimitToast();\n'
        '    return;\n'
        '  }\n'
        "  if (!w || !t) { alert('Заполни слово и перевод!'); return; }"
    )
    if save_anchor in html:
        html = html.replace(save_anchor, save_insert, 1)

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
