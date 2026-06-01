#!/usr/bin/env python3
"""Add sync/vocab i18n keys, tf() helper, and refresh mirror-sync profile HTML on profconq site."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
DIR = Path('/var/www/proficonq/tutor-app/patches')
TF = DIR / 'website-i18n-tf-helper.js'
STRINGS = DIR / 'website-i18n-sync-strings.js'
PROFILE = DIR / 'website-mirror-sync-profile.html'
MIRROR_JS = DIR / 'website-mirror-sync.js'
WORD_LIMIT_JS = DIR / 'website-word-limit.js'


def replace_block(text: str, start_marker: str, end_before: str, new_content: str) -> str:
    i = text.find(start_marker)
    if i < 0:
        return text
    j = text.find(end_before, i)
    if j < 0:
        return text
    return text[:i] + new_content + text[j:]


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')

    if 'function tf(key, params)' not in html:
        anchor = 'function t(key) {'
        tf = TF.read_text(encoding='utf-8')
        html = html.replace(anchor, tf + anchor, 1)
        print('Added tf() helper')

    if "'sync.section'" not in html:
        anchor = 'function t(key) {'
        block = STRINGS.read_text(encoding='utf-8')
        # run after UI_STRINGS is defined — inject before t()
        ui_end = html.find('function t(key)')
        if ui_end < 0:
            raise SystemExit('t() not found')
        html = html[:ui_end] + block + '\n' + html[ui_end:]
        print('Added sync i18n strings')

    # Replace mirror-sync JS block
    start = "var SYNC_PRIMARY_KEY = 'profconq_sync_primary_v1';"
    end = 'let videoCards = [];'
    if start in html:
        new_js = MIRROR_JS.read_text(encoding='utf-8')
        html = replace_block(html, start, end, new_js)
        print('Updated mirror-sync JS')

    # Replace word-limit block if present
    wl_start = 'var FREE_VOCAB_WORD_LIMIT = 10;'
    if wl_start in html:
        wl_end = 'let videoCards = [];'
        # only if word limit is immediately before videoCards — find next function after vocabShowWordLimitToast
        idx = html.find(wl_start)
        idx_end = html.find('\nlet videoCards', idx)
        if idx_end > idx:
            html = html[:idx] + WORD_LIMIT_JS.read_text(encoding='utf-8') + html[idx_end:]
            print('Updated word-limit JS')

    # Replace profile sync HTML (Russian or English patch)
    for old_start in (
        '<div class="profile-section-title">Синхронизация</div>',
        '<div class="profile-section-title" data-i18n="sync.section">',
    ):
        if old_start in html:
            i = html.find(old_start)
            j = html.find('<div class="profile-section-title" data-i18n="profile.statsSection">', i)
            if j > i:
                profile = PROFILE.read_text(encoding='utf-8')
                html = html[:i] + profile + html[j:]
                print('Updated profile sync HTML')
            break

    if 'syncUpdatePrimaryUi();\n  logoAlignArrowWhenReady();' not in html:
        html = html.replace(
            'async function startAppAfterAuth() {\n  logoAlignArrowWhenReady();',
            'async function startAppAfterAuth() {\n  syncUpdatePrimaryUi();\n  logoAlignArrowWhenReady();',
            1,
        )

    # Refresh hints when language changes
    if 'syncUpdatePrimaryUi();' not in html.split('function applyUiLanguage')[1][:800]:
        html = html.replace(
            '  profileSyncSettingsUi();\n  profileRenderStats();',
            '  profileSyncSettingsUi();\n  try { syncUpdatePrimaryUi(); } catch (e) {}\n  profileRenderStats();',
            1,
        )

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
