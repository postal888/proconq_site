#!/usr/bin/env python3
"""Remove demo vocabulary seed and bundled books from profconq website dist."""
from __future__ import annotations

import re
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')

    # Empty vocab seed array (keep name for minimal diff)
    html, n_seed = re.subn(
        r"const DEFAULT_VOCAB_SEED = \[[\s\S]*?\];",
        "const DEFAULT_VOCAB_SEED = [];",
        html,
        count=1,
    )
    if n_seed:
        print('Cleared DEFAULT_VOCAB_SEED')

    html = html.replace(
        "if (r.status === 204) { words = DEFAULT_VOCAB_SEED.slice(); recomputeNextIdFromWords(); return; }",
        "if (r.status === 204) { words = []; recomputeNextIdFromWords(); return; }",
    )
    html = html.replace(
        "  words = DEFAULT_VOCAB_SEED.slice();\n  recomputeNextIdFromWords();",
        "  words = [];\n  recomputeNextIdFromWords();",
    )
    print('loadVocabularyFromServer uses empty list when no data')

    # Bundled books catalog
    html, n_cat = re.subn(
        r"function booksDefaultCatalog\(\) \{\s*return \[[\s\S]*?\];\s*\}",
        "function booksDefaultCatalog() {\n  return [];\n}",
        html,
        count=1,
    )
    if n_cat:
        print('Cleared booksDefaultCatalog')

    old_read = """function booksReadCatalog() {
  try {
    var raw = localStorage.getItem(BOOKS_CATALOG_KEY);
    if (!raw) return booksDefaultCatalog();
    var arr = JSON.parse(raw);
    if (!Array.isArray(arr) || !arr.length) return booksDefaultCatalog();
    var hasBundled = arr.some(function (b) {
      return b.id === 'bundled-capitaes';
    });
    if (!hasBundled) arr = booksDefaultCatalog().concat(arr);
    return arr;
  } catch (e) {
    return booksDefaultCatalog();
  }
}"""

    new_read = """function booksReadCatalog() {
  try {
    var raw = localStorage.getItem(BOOKS_CATALOG_KEY);
    if (!raw) return booksDefaultCatalog();
    var arr = JSON.parse(raw);
    if (!Array.isArray(arr)) return booksDefaultCatalog();
    return arr.filter(function (b) { return b && b.id !== 'bundled-capitaes'; });
  } catch (e) {
    return booksDefaultCatalog();
  }
}"""

    if old_read in html:
        html = html.replace(old_read, new_read)
        print('Updated booksReadCatalog (no auto-inject bundled book)')
    elif "bundled-capitaes" in html and new_read not in html:
        print('WARN: booksReadCatalog pattern not matched — check manually')

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
