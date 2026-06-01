#!/usr/bin/env python3
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')

WRAPPERS = """
function speakFlashcardPortuguese(mode) {
  speakFlashcardForSide('source', mode);
}

function speakFlashcardRussian() {
  speakFlashcardForSide('target');
}

"""


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    if 'function speakFlashcardPortuguese(mode)' in html:
        print('Wrappers already present')
        return
    anchor = '\nif (window.speechSynthesis) {'
    idx = html.find(anchor)
    if idx < 0:
        raise SystemExit('speechSynthesis anchor not found')
    html = html[:idx] + '\n' + WRAPPERS + html[idx:]
    INDEX.write_text(html, encoding='utf-8')
    print('Restored speakFlashcard wrappers')


if __name__ == '__main__':
    main()
