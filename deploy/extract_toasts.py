#!/usr/bin/env python3
import re
import sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding='utf-8')
static = set()
for m in re.finditer(r"showToast\('([^']*)'\)", html):
    s = m.group(1)
    if '+' not in s:
        static.add(s)
for s in sorted(static, key=len):
    print(s)
print('COUNT', len(static), file=sys.stderr)
