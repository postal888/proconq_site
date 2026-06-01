#!/usr/bin/env python3
"""Remove embedded admin panel from main SPA index.html."""
from pathlib import Path
import re

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    original = html

    # Remove standalone admin view block.
    html = re.sub(
        r'\s*<div class="view" id="view-admin">.*?</div>\s*(?=<div class="view" id="view-profile">)',
        '\n',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove nav-admin button if present.
    html = re.sub(
        r'\s*<button class="nav-item nav-item-main" data-view="admin" id="nav-admin"[^>]*>.*?</button>',
        '',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove injected admin JS block up to initProfileView.
    html = re.sub(
        r'\nvar __adminPromoCodes = \[\];.*?function initAdminView\(\) \{.*?\n\}\n\n(?=function initProfileView\(\))',
        '\n',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove admin routes.
    html = html.replace("  '/admin':              'admin',\n", '')
    html = html.replace("  'admin':          '/admin',\n", '')

    # Remove admin hooks.
    html = html.replace('  initAdminView();\n', '')
    html = html.replace('      adminUpdateNavVisibility();\n', '')
    html = html.replace(
        '  if (viewId === "admin" && !adminIsUser()) { showToast(t("admin.forbidden")); return; }\n',
        '',
    )
    html = html.replace(
        "  if (viewId === 'admin') { initAdminView(); try { lucide.createIcons(); } catch (e) {} }\n  ",
        '',
    )

    # Remove admin-only CSS if present.
    html = re.sub(r'\.admin-page\{[^}]+\}\n?', '', html)
    html = re.sub(r'\.admin-promo-[^{]+\{[^}]+\}\n?', '', html)
    html = re.sub(r'\.admin-empty\{[^}]+\}\n?', '', html)

    if html == original:
        print('No embedded admin blocks found (already clean?)')
    else:
        INDEX.write_text(html, encoding='utf-8')
        print('Cleaned main SPA:', INDEX)


if __name__ == '__main__':
    main()
