#!/usr/bin/env python3
"""Improve vocabulary add UX on profconq website."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PATCH_DIR = Path('/var/www/proficonq/tutor-app/patches')
MARKER = 'function vocabQuickAdd()'


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    if MARKER in html:
        print('Already patched')
        return

    js = (PATCH_DIR / 'website-vocab-add.js').read_text(encoding='utf-8')
    css = (PATCH_DIR / 'website-vocab-add.css').read_text(encoding='utf-8')

    anchor = 'function saveWord() {'
    if anchor not in html:
        raise SystemExit('saveWord not found')
    html = html.replace(anchor, js + '\n' + anchor, 1)

    old_tag_check = "  if (!tag) { alert('Выбери тип слова'); return; }"
    new_tag_check = "  if (!tag) tag = 'geral';"
    if old_tag_check in html:
        html = html.replace(old_tag_check, new_tag_check, 1)

    old_empty = (
        'grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">'
        '<i data-lucide="search-x"></i><h3>Слов не найдено</h3>'
        '<p>Попробуй другой запрос или добавь новое слово.</p></div>`;'
    )
    new_empty = (
        'grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">'
        '<i data-lucide="book-open"></i><h3>Словарь пуст</h3>'
        '<p>Добавьте первое слово — кнопкой ниже или через «Добавить слово» в шапке.</p>'
        '<button type="button" class="btn btn-primary" onclick="openAddWord()">'
        '<i data-lucide="plus"></i> Добавить слово</button></div>`;'
    )
    if old_empty in html:
        html = html.replace(old_empty, new_empty, 1)

    toolbar_anchor = '<button type="button" class="btn btn-secondary btn-sm" id="vocab-import-btn"'
    toolbar_btn = (
        '<button type="button" class="btn btn-primary btn-sm" onclick="openAddWord()">'
        '<i data-lucide="plus"></i> <span data-i18n="vocab.addWord">Добавить слово</span></button>\n          '
    )
    if toolbar_anchor in html and toolbar_btn.strip() not in html:
        html = html.replace(toolbar_anchor, toolbar_btn + toolbar_anchor, 1)

    table_anchor = "  parts.push('</tbody></table>');"
    table_patch = "  parts.push(vocabQuickAddRowHtml());\n  parts.push('</tbody></table>');"
    if table_anchor in html and 'vocabQuickAddRowHtml' not in html:
        html = html.replace(table_anchor, table_patch, 1)

    cards_anchor = "  grid.innerHTML = parts.join('');\n  lucide.createIcons();\n  syncTextgenListIfActive();\n}\n\nfunction filterWords"
    cards_patch = (
        "  parts.push('<div class=\"vocab-add-inline-bar\">"
        "<button type=\"button\" class=\"btn btn-primary btn-sm\" onclick=\"openAddWord()\">"
        "<i data-lucide=\"plus\"></i> Добавить слово</button></div>');\n"
        "  grid.innerHTML = parts.join('');\n  lucide.createIcons();\n  syncTextgenListIfActive();\n}\n\nfunction filterWords"
    )
    if cards_anchor in html and 'vocab-add-inline-bar' not in html:
        html = html.replace(cards_anchor, cards_patch, 1)

    nav_old = "  const addBtn = document.getElementById('add-word-btn');\n  addBtn.style.display"
    nav_new = (
        "  const addBtn = document.getElementById('add-word-btn');\n"
        "  if (addBtn) addBtn.style.display"
    )
    if nav_old in html:
        html = html.replace(nav_old, nav_new, 1)

    if css.strip() not in html:
        html = html.replace('</style>', css + '\n</style>', 1)

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
