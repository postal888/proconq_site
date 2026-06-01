#!/usr/bin/env python3
from pathlib import Path

p = Path('/var/www/proficonq/tutor-app/dist/index.html')
h = p.read_text(encoding='utf-8')
h = h.replace(
    "if (!pattern || pattern === 'study.placeholderWord') return studyPlaceholderWord() || short;",
    "if (!pattern || pattern === 'study.placeholderWord') return t('vocab.placeholderWord') || short;",
)
h = h.replace(
    "if (!pattern || pattern === 'study.placeholderTranslation') return studyPlaceholderTranslation() || short;",
    "if (!pattern || pattern === 'study.placeholderTranslation') return t('vocab.placeholderTranslation') || short;",
)
p.write_text(h, encoding='utf-8')
print('fixed placeholder recursion')
