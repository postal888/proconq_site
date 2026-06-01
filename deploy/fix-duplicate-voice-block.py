#!/usr/bin/env python3
"""Remove duplicate speakFlashcard/startVoiceField block injected before speechSynthesis."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')

DUP_START = "function speakFlashcardPortuguese(mode) {\n  speakFlashcardForSide('source', mode);\n}\n\nfunction speakFlashcardRussian()"
DUP_END = "\nif (window.speechSynthesis) {"


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    i = html.find(DUP_START)
    if i < 0:
        print('Duplicate block not found — already clean')
        return
    j = html.find(DUP_END, i)
    if j < 0:
        raise SystemExit('End marker not found')
    html = html[:i] + html[j:]
    INDEX.write_text(html, encoding='utf-8')
    print('Removed duplicate flashcard/voice block')


if __name__ == '__main__':
    main()
