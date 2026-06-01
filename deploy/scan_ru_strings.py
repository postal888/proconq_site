#!/usr/bin/env python3
import re
from pathlib import Path

h = Path('/var/www/proficonq/tutor-app/dist/index.html').read_text(encoding='utf-8')
patterns = [
    (r"showToast\([^)]{0,120}\)", 'showToast'),
    (r"alert\([^)]{0,80}\)", 'alert'),
    (r"confirm\([^)]{0,120}\)", 'confirm'),
    (r'<h3>[^<]*[А-Яа-яЁё][^<]*</h3>', 'h3'),
    (r"placeholder=\"[^\"]*[А-Яа-яЁё][^\"]*\"", 'placeholder'),
    (r"title=\"[^\"]*[А-Яа-яЁё][^\"]*\"", 'title'),
    (r"data-i18n[^>]*>[^<]*[А-Яа-яЁё]", 'data-i18n fallback'),
]
seen = set()
for pat, kind in patterns:
    for m in re.finditer(pat, h):
        s = m.group(0).replace('\n', ' ')
        if s in seen:
            continue
        if 'UI_STRINGS' in s or 'extra.ru' in s:
            continue
        seen.add(s)
        print(kind + ':', s[:140])
