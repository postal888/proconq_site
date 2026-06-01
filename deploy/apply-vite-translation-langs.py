#!/usr/bin/env python3
"""Patch tutor-app vite.config.ts: transcript/book translate accepts fromLang/toLang."""
from __future__ import annotations

from pathlib import Path

VITE = Path('/var/www/proficonq/tutor-app/vite.config.ts')
MARKER = 'function translationLangName(code: string): string'


def main() -> None:
    src = VITE.read_text(encoding='utf-8')
    if MARKER in src:
        print('Already patched')
        return

    helper = """
const TRANSLATION_LANG_NAMES: Record<string, string> = {
  pt: 'Brazilian Portuguese',
  en: 'English',
  ru: 'Russian',
  es: 'Spanish',
}

function normalizeTranslationLang(code: unknown, fallback = 'pt'): string {
  const c = String(code || fallback).toLowerCase()
  return TRANSLATION_LANG_NAMES[c] ? c : fallback
}

function translationLangName(code: string): string {
  return TRANSLATION_LANG_NAMES[normalizeTranslationLang(code)] || code
}

"""

    anchor = 'async function openaiTranslateWords(words: string[], apiKey: string): Promise<Record<string, string>> {'
    if anchor not in src:
        raise SystemExit('openaiTranslateWords not found')
    src = src.replace(anchor, helper + anchor, 1)

    src = src.replace(
        'async function openaiTranslateWords(words: string[], apiKey: string): Promise<Record<string, string>> {',
        'async function openaiTranslateWords(\n  words: string[],\n  apiKey: string,\n  fromLang = \'pt\',\n  toLang = \'ru\',\n): Promise<Record<string, string>> {',
    )

    src = src.replace(
        'const prompt = `Portuguese tokens from subtitles (may be 1 letter, e.g. "e", "a", "o"). Return ONE JSON object ONLY.\n\nRules:\n- Keys MUST be EXACTLY the strings from the Words array below (lowercase). Include EVERY word — do not omit articles, conjunctions, pronouns, or clitics.\n- Values: short Russian gloss (1–7 words).',
        'const fromName = translationLangName(fromLang)\n  const toName = translationLangName(toLang)\n  const prompt = `${fromName} tokens from subtitles (may be 1 letter). Return ONE JSON object ONLY.\n\nRules:\n- Keys MUST be EXACTLY the strings from the Words array below (lowercase). Include EVERY word — do not omit articles, conjunctions, pronouns, or clitics.\n- Values: short ${toName} gloss (1–7 words).',
    )

    src = src.replace(
        "'Reply with a single JSON object only. Each key from the user list must appear exactly once. Values: Russian gloss. No markdown, no code fences.'",
        "'Reply with a single JSON object only. Each key from the user list must appear exactly once. Values: target-language gloss. No markdown, no code fences.'",
    )

    src = src.replace(
        'async function buildGlossWithGapPasses(unique: string[], apiKey: string): Promise<Record<string, string>> {',
        'async function buildGlossWithGapPasses(\n  unique: string[],\n  apiKey: string,\n  fromLang = \'pt\',\n  toLang = \'ru\',\n): Promise<Record<string, string>> {',
    )
    src = src.replace(
        'const part = await openaiTranslateWords(batch, apiKey)',
        'const part = await openaiTranslateWords(batch, apiKey, fromLang, toLang)',
    )
    src = src.replace(
        'const part = await openaiTranslateWords(missing, apiKey)',
        'const part = await openaiTranslateWords(missing, apiKey, fromLang, toLang)',
    )
    src = src.replace(
        'Object.assign(gloss, await openaiTranslateWords(sub, apiKey))',
        'Object.assign(gloss, await openaiTranslateWords(sub, apiKey, fromLang, toLang))',
    )

    src = src.replace(
        'async function openaiTranslateBookPassage(text: string, apiKey: string): Promise<string> {',
        'async function openaiTranslateBookPassage(\n  text: string,\n  apiKey: string,\n  fromLang = \'pt\',\n  toLang = \'ru\',\n): Promise<string> {',
    )
    src = src.replace(
        "'Переводи с бразильского португальского на русский. Сохраняй абзацы и диалоги. Только перевод, без комментариев и кавычек вокруг всего текста.'",
        "'Translate from ' + translationLangName(fromLang) + ' to ' + translationLangName(toLang) + '. Preserve paragraphs and dialogue. Translation only, no commentary.'",
    )

    src = src.replace(
        "let body: { words?: string[] }",
        "let body: { words?: string[]; fromLang?: string; toLang?: string }",
    )
    src = src.replace(
        "body = JSON.parse(rawBody) as { words?: string[] }",
        "body = JSON.parse(rawBody) as { words?: string[]; fromLang?: string; toLang?: string }",
    )
    src = src.replace(
        'const gloss = await buildGlossWithGapPasses(unique, openaiKey)',
        "const fromLang = normalizeTranslationLang(body.fromLang, 'pt')\n        const toLang = normalizeTranslationLang(body.toLang, 'ru')\n        const gloss = await buildGlossWithGapPasses(unique, openaiKey, fromLang, toLang)",
    )

    src = src.replace(
        "let body: { text?: string }",
        "let body: { text?: string; fromLang?: string; toLang?: string }",
    )
    src = src.replace(
        "body = JSON.parse(rawBody) as { text?: string }",
        "body = JSON.parse(rawBody) as { text?: string; fromLang?: string; toLang?: string }",
    )

    # book translate call site
    old_book = "const translation = await openaiTranslateBookPassage(text, openaiKey)"
    if old_book in src:
        src = src.replace(
            old_book,
            "const fromLang = normalizeTranslationLang(body.fromLang, 'pt')\n        const toLang = normalizeTranslationLang(body.toLang, 'ru')\n        const translation = await openaiTranslateBookPassage(text, openaiKey, fromLang, toLang)",
        )

    VITE.write_text(src, encoding='utf-8')
    print('Patched', VITE)


if __name__ == '__main__':
    main()
