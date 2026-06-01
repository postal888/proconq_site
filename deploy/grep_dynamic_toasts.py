#!/usr/bin/env python3
import re
from pathlib import Path
h = Path('/var/www/proficonq/tutor-app/dist/index.html').read_text(encoding='utf-8')
idx = h.find('В словарь')
if idx >= 0:
    print(repr(h[idx:idx+180]))
for pat in [r"showToast\('Не больше[^;]{0,120}"]:
    for m in re.finditer(pat, h):
        print(m.group(0)[:200])
