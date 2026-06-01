#!/usr/bin/env python3
"""Patch profconq tutor-app dist/index.html for directional vocabulary sync."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PROFILE_SNIPPET = Path('/var/www/proficonq/tutor-app/patches/website-directional-sync-profile.html')
JS_SNIPPET = Path('/var/www/proficonq/tutor-app/patches/website-directional-sync.js')

MARKER_PROFILE = 'id="profile-account-plan"'
MARKER_JS = 'let videoCards = [];'
MARKER_ALREADY = 'syncVocabPullFromMobile'


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    if MARKER_ALREADY in html:
        print('Already patched')
        return

    profile = PROFILE_SNIPPET.read_text(encoding='utf-8')
    js = JS_SNIPPET.read_text(encoding='utf-8')

    anchor = '          <div class="profile-section-title" data-i18n="profile.statsSection">Statistics</div>'
    if anchor not in html:
        anchor = '          <div class="profile-section-title" data-i18n="profile.statsSection">'
    if anchor not in html:
        raise SystemExit('Profile stats anchor not found')
    html = html.replace(anchor, profile + '\n' + anchor, 1)

    if MARKER_JS not in html:
        raise SystemExit('JS anchor not found')
    html = html.replace(MARKER_JS, js + '\n' + MARKER_JS, 1)

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
