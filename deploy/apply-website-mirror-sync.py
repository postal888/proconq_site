#!/usr/bin/env python3
"""Replace directional sync UI with mirror toggle + one button on profconq site."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
DIR = Path('/var/www/proficonq/tutor-app/patches')
PROFILE = DIR / 'website-mirror-sync-profile.html'
CSS = DIR / 'website-mirror-sync.css'
JS = DIR / 'website-mirror-sync.js'
MARKER = 'syncMirrorNow'


def remove_block(text: str, start: str, end_before: str) -> str:
    i = text.find(start)
    if i < 0:
        return text
    j = text.find(end_before, i)
    if j < 0:
        return text
    return text[:i] + text[j:]


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    if MARKER in html:
        print('Already patched')
        return

    profile = PROFILE.read_text(encoding='utf-8')
    css = CSS.read_text(encoding='utf-8')
    js = JS.read_text(encoding='utf-8')

    # Remove old directional sync block if present
    old_start = '<div class="profile-section-title">Синхронизация с приложением</div>'
    if old_start in html:
        html = remove_block(
            html,
            old_start,
            '<div class="profile-section-title" data-i18n="profile.statsSection">',
        )

    anchor = '<div class="profile-section-title" data-i18n="profile.statsSection">Statistics</div>'
    if anchor not in html:
        raise SystemExit('Profile anchor not found')
    html = html.replace(anchor, profile + '\n' + anchor, 1)

    style_anchor = '</style>'
    if css.strip() not in html:
        html = html.replace(style_anchor, css + '\n' + style_anchor, 1)

    # Remove old directional JS if present (stop before mirror block)
    old_helpers_start = 'function vocabNormalizeKey(w) {'
    old_helpers_end = "var SYNC_PRIMARY_KEY = 'profconq_sync_primary_v1';"
    i0 = html.find(old_helpers_start)
    i1 = html.find(old_helpers_end)
    if i0 >= 0 and i1 > i0:
        html = html[:i0] + html[i1:]

    for orphan in (
        '/** Button 1: add words that the app uploaded to the cloud into this page. */\nasync \n',
        'async \nvar SYNC_PRIMARY_KEY',
    ):
        html = html.replace(orphan, 'var SYNC_PRIMARY_KEY' if 'SYNC' in orphan else '')

    js_anchor = 'let videoCards = [];'
    if js_anchor not in html:
        raise SystemExit('JS anchor not found')
    html = html.replace(js_anchor, js + '\n' + js_anchor, 1)

    if 'syncUpdatePrimaryUi();\n  logoAlignArrowWhenReady();' not in html:
        html = html.replace(
            'async function startAppAfterAuth() {\n  logoAlignArrowWhenReady();',
            'async function startAppAfterAuth() {\n  syncUpdatePrimaryUi();\n  logoAlignArrowWhenReady();',
            1,
        )

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
