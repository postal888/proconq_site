#!/usr/bin/env python3
"""Patch remaining hardcoded RU strings: directional sync, alerts, vocab empty states."""
from __future__ import annotations

from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
DIR = Path('/var/www/proficonq/tutor-app/patches')
SYNC_STRINGS = DIR / 'website-i18n-sync-strings.js'

REPLACEMENTS: list[tuple[str, str]] = [
    ("showToast('Войдите в аккаунт')", "showToast(t('sync.signInFirst'))"),
    (
        "showToast('С телефона добавлено ' + merged.added + ' слов (на сайте: ' + words.length + ')')",
        "showToast(tf('sync.pullAdded', { added: merged.added, total: words.length }))",
    ),
    ("showToast('Новых слов с телефона нет')", "showToast(t('sync.pullNoNew'))"),
    ("showToast('Не удалось загрузить слова с сервера')", "showToast(t('sync.pullFailed'))"),
    (
        "showToast('В облако добавлено ' + merged.added + ' слов для приложения (всего: ' + merged.words.length + ')')",
        "showToast(tf('sync.pushAdded', { added: merged.added, total: merged.words.length }))",
    ),
    (
        "showToast('Все слова с сайта уже в облаке (' + merged.words.length + ')')",
        "showToast(tf('sync.pushAllInCloud', { total: merged.words.length }))",
    ),
    ("showToast('Не удалось отправить словарь в облако')", "showToast(t('sync.pushFailed'))"),
    (
        "alert('Заполни слово и перевод!')",
        "alert(t('vocab.needWordTranslation'))",
    ),
    (
        "alert('Выбери тип слова')",
        "alert(t('vocab.pickWordType'))",
    ),
    (
        "grid.innerHTML = `<div class=\"empty-state\" style=\"grid-column:1/-1\">"
        "<i data-lucide=\"search-x\"></i><h3>Слов не найдено</h3>"
        "<p>Попробуй другой запрос или добавь новое слово.</p></div>`;",
        "grid.innerHTML = `<div class=\"empty-state\" style=\"grid-column:1/-1\">"
        "<i data-lucide=\"search-x\"></i><h3>${t('vocab.noWordsFound')}</h3>"
        "<p>${t('vocab.tryOtherQuery')}</p></div>`;",
    ),
    (
        "grid.innerHTML = `<div class=\"empty-state\" style=\"grid-column:1/-1\">"
        "<i data-lucide=\"book-open\"></i><h3>Словарь пуст</h3>"
        "<p>Добавьте первое слово — кнопкой ниже или через «Добавить слово» в шапке.</p>"
        "<button type=\"button\" class=\"btn btn-primary\" onclick=\"openAddWord()\">"
        "<i data-lucide=\"plus\"></i> Добавить слово</button></div>`;",
        "grid.innerHTML = `<div class=\"empty-state\" style=\"grid-column:1/-1\">"
        "<i data-lucide=\"book-open\"></i><h3>${t('vocab.emptyTitle')}</h3>"
        "<p>${t('vocab.emptyHint')}</p>"
        "<button type=\"button\" class=\"btn btn-primary\" onclick=\"openAddWord()\">"
        "<i data-lucide=\"plus\"></i> ${t('vocab.emptyAddBtn')}</button></div>`;",
    ),
    (
        "<i data-lucide=\"plus\"></i> Добавить слово</button></div>');",
        "<i data-lucide=\"plus\"></i> ' + t('vocab.emptyAddBtn') + '</button></div>');",
    ),
    (
        "showToast('Не больше ' + TEXTGEN_MAX + ' слов за раз')",
        "showToast(tf('textgen.maxWords', { max: TEXTGEN_MAX }))",
    ),
]

SYNC_START = "// Injected into UI_STRINGS (ru / en / pt) — sync mirror"
SYNC_END_MARKERS = (
    "})();\n\nfunction t(key)",
    "})();\n\n})();\n\nfunction t(key)",
)


def refresh_sync_strings(html: str) -> str:
    if SYNC_START not in html:
        return html
    block = SYNC_STRINGS.read_text(encoding='utf-8').rstrip() + '\n\n'
    i = html.find(SYNC_START)
    j = -1
    for marker in SYNC_END_MARKERS:
        j = html.find(marker, i)
        if j >= 0:
            j += len("})();")
            break
    if j < i:
        return html
    return html[:i] + block + html[j:]


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = refresh_sync_strings(html)
    print('Refreshed sync i18n strings block')

    n = 0
    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            n += 1
            print('Replaced:', old[:60].replace('\n', ' '))

    # Replace embedded directional-sync.js if whole file was injected earlier
    ds = (DIR / 'website-directional-sync.js').read_text(encoding='utf-8')
    marker = 'async function syncVocabPullFromMobile()'
    if marker in html and "showToast(t('sync.pullNoNew'))" not in html:
        # Replace function pair only
        start = html.find('function vocabNormalizeKey(w)')
        end = html.find('\nlet videoCards = [];')
        if start > 0 and end > start and 'syncVocabPullFromMobile' in html[start:end]:
            html = html[:start] + ds + '\n' + html[end:]
            print('Replaced directional-sync JS block')
            n += 1

    INDEX.write_text(html, encoding='utf-8')
    print(f'Done ({n} replacements), patched', INDEX)


if __name__ == '__main__':
    main()
