#!/usr/bin/env python3
from pathlib import Path
h = Path('/var/www/proficonq/tutor-app/dist/index.html').read_text(encoding='utf-8')
for needle in ['nav-item', 'data-i18n="nav.', 'sidebar-nav', 'loadUiLangPref', 'function t(key)']:
    print(needle, h.count(needle))
# first nav items
idx = h.find('data-i18n="nav.')
while idx != -1 and idx < h.find('</nav>') if '</nav>' in h else True:
    print(h[idx:idx+80].replace('\n',' '))
    idx = h.find('data-i18n="nav.', idx+1)
    if idx > 50000: break
