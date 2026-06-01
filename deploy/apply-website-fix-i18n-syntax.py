#!/usr/bin/env python3
"""Fix broken JS after i18n patches: stray })(); before t(), ensure applyUiLanguage on boot."""
from __future__ import annotations

import re
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')


def fix_stray_iife_close(html: str) -> str:
    # Duplicate close injected before function t(key) — breaks entire script block.
    bad = "})();\n\n})();\n\nfunction t(key)"
    good = "})();\n\nfunction t(key)"
    if bad in html:
        html = html.replace(bad, good, 1)
        print('Removed stray })(); before t()')
    elif re.search(r"\}\)\(\);\s*\n\s*\}\)\(\);\s*\n\s*function t\(key\)", html):
        html = re.sub(
            r"\}\)\(\);\s*\n\s*\}\)\(\);\s*\n(\s*function t\(key\))",
            r"})();\n\n\1",
            html,
            count=1,
        )
        print('Removed stray })(); (regex)')
    else:
        print('No stray })(); found (already fixed?)')
    return html


def ensure_apply_after_start(html: str) -> str:
    needle = "  try { renderYtHistory(); } catch (e) {}\n  applyYoutubeUrlFromQuery();\n}"
    insert = "  try { renderYtHistory(); } catch (e) {}\n  applyYoutubeUrlFromQuery();\n  applyUiLanguage();\n}"
    if needle in html and insert not in html:
        html = html.replace(needle, insert, 1)
        print('Added applyUiLanguage() to startAppAfterAuth')
    return html


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = fix_stray_iife_close(html)
    html = ensure_apply_after_start(html)
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
