#!/usr/bin/env python3
import re
import sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding='utf-8')
for m in re.finditer(r"showToast\([^)]+\)", html):
    s = m.group(0)
    if '+' in s and "t(" not in s:
        print(s[:120])
