#!/usr/bin/env python3
"""Generate website-i18n-toasts-strings.js from toast message catalog."""
from __future__ import annotations

import json
import re
from pathlib import Path

# ru text -> (key, en, pt)
CATALOG: dict[str, tuple[str, str, str]] = {
    'Подчёркнуто': ('toast.highlighted', 'Highlighted', 'Destacado'),
    'Скопировано': ('toast.copied', 'Copied', 'Copiado'),
    'MP3 сохранён': ('toast.mp3Saved', 'MP3 saved', 'MP3 salvo'),
    'Ошибка записи': ('toast.recordError', 'Recording error', 'Erro de gravação'),
    'Уже в словаре': ('toast.alreadyInDictionary', 'Already in dictionary', 'Já no dicionário'),
    'Список очищен': ('toast.listCleared', 'List cleared', 'Lista limpa'),
    'Выделите текст': ('toast.selectText', 'Select some text', 'Selecione o texto'),
    'Слово добавлено': ('toast.wordAdded', 'Word added', 'Palavra adicionada'),
    'Фраза сохранена': ('toast.phraseSaved', 'Phrase saved', 'Frase salva'),
    'Аудиофайл скачан': ('toast.audioDownloaded', 'Audio file downloaded', 'Áudio baixado'),
    'Нечего добавлять': ('toast.nothingToAdd', 'Nothing to add', 'Nada para adicionar'),
    'Комментарий пуст': ('toast.commentEmpty', 'Comment is empty', 'Comentário vazio'),
    'Картинка сохранена': ('toast.imageSaved', 'Image saved', 'Imagem salva'),
    'Сначала запишите звук': ('toast.recordSoundFirst', 'Record audio first', 'Grave o áudio primeiro'),
    'Файл заметки сохранён': ('toast.noteFileSaved', 'Note file saved', 'Arquivo de nota salvo'),
    'Нет строк для экспорта': ('toast.noRowsToExport', 'No rows to export', 'Nenhuma linha para exportar'),
    'Вставьте ссылку YouTube': ('toast.pasteYoutubeLink', 'Paste a YouTube link', 'Cole um link do YouTube'),
    'История роликов очищена': ('toast.historyCleared', 'Watch history cleared', 'Histórico de vídeos limpo'),
    'Укажите слово и перевод': ('vocab.needWordTranslation', 'Enter word and translation', 'Informe palavra e tradução'),
    'Заполни слово и перевод!': ('vocab.needWordTranslation', 'Enter word and translation', 'Informe palavra e tradução'),
    'Войдите в аккаунт': ('sync.signInFirst', 'Sign in to your account', 'Entre na sua conta'),
    'Ошибка сохранения файла': ('toast.fileSaveError', 'Could not save file', 'Não foi possível salvar o arquivo'),
    'Не удалось начать запись': ('toast.recordStartFailed', 'Could not start recording', 'Não foi possível iniciar a gravação'),
    'Субтитры сохранены офлайн': ('toast.subtitlesSavedOffline', 'Subtitles saved offline', 'Legendas salvas offline'),
    'Выбери хотя бы одно слово': ('toast.pickAtLeastOneWord', 'Select at least one word', 'Selecione pelo menos uma palavra'),
    'Выделите фразу в субтитрах': ('toast.selectPhraseInSubtitles', 'Select a phrase in subtitles', 'Selecione uma frase nas legendas'),
    'Выделение вне текста книги': ('toast.selectionOutsideBook', 'Selection outside book text', 'Seleção fora do texto do livro'),
    'Слово не может быть пустым': ('toast.wordEmpty', 'Word cannot be empty', 'A palavra não pode estar vazia'),
    'Удерживайте поле → Вставить': ('toast.holdFieldToPaste', 'Hold the field → Paste', 'Segure o campo → Colar'),
    'Введите не менее 2 символов': ('toast.minTwoChars', 'Enter at least 2 characters', 'Digite pelo menos 2 caracteres'),
    'Отметьте фрагменты галочками': ('toast.checkFragments', 'Check fragments with boxes', 'Marque os trechos'),
    'Текст добавлен в комментарий': ('toast.textAddedToComment', 'Text added to comment', 'Texto adicionado ao comentário'),
    'Нет слов по текущему фильтру': ('toast.noWordsForFilter', 'No words for current filter', 'Nenhuma palavra neste filtro'),
    'Перевод не может быть пустым': ('toast.translationEmpty', 'Translation cannot be empty', 'A tradução não pode estar vazia'),
    'Сначала выберите тип «Глагол»': ('toast.selectVerbTypeFirst', 'Select type «Verb» first', 'Selecione o tipo «Verbo» primeiro'),
    'Для глагола укажите инфинитив': ('toast.verbNeedsInfinitive', 'Verb requires infinitive', 'Para verbo, informe o infinitivo'),
    'Выделите фрагмент в субтитрах': ('toast.selectFragmentInSubtitles', 'Select a fragment in subtitles', 'Selecione um trecho nas legendas'),
    'Не удалось переключить прокси': ('toast.proxyToggleFailed', 'Could not toggle proxy', 'Não foi possível alternar o proxy'),
    'Сначала откройте ролик YouTube': ('toast.openYoutubeVideoFirst', 'Open a YouTube video first', 'Abra um vídeo do YouTube primeiro'),
    'Не удалось собрать файл записи': ('toast.recordFileBuildFailed', 'Could not build recording file', 'Não foi possível montar o arquivo'),
    'Проверь поля и нажми «Добавить»': ('toast.checkFieldsAndAdd', 'Check fields and tap «Add»', 'Verifique os campos e toque em «Adicionar»'),
    'Видео скачано и сохранено офлайн': ('toast.videoSavedOffline', 'Video downloaded and saved offline', 'Vídeo baixado e salvo offline'),
    'Пустой ответ — попробуйте ещё раз': ('toast.emptyTranslationRetry', 'Empty response — try again', 'Resposta vazia — tente de novo'),
    'Не удалось сохранить офлайн-копию': ('toast.offlineCopySaveFailed', 'Could not save offline copy', 'Não foi possível salvar cópia offline'),
    'Откройте книгу и дождитесь текста': ('toast.openBookWaitText', 'Open a book and wait for text', 'Abra um livro e aguarde o texto'),
    'Нет субтитров — загрузите дорожку': ('toast.noSubtitlesLoadTrack', 'No subtitles — load a track', 'Sem legendas — carregue uma faixa'),
    'Сначала скачайте видео в Downloads': ('toast.downloadVideoFirst', 'Download the video to Downloads first', 'Baixe o vídeo para Downloads primeiro'),
    'Копирование фраз отключено в профиле': ('toast.phraseCopyDisabled', 'Phrase copy disabled in profile', 'Cópia de frases desativada no perfil'),
    'Сначала введите слово или фразу (PT)': ('toast.enterWordOrPhrasePt', 'Enter a word or phrase (PT) first', 'Digite uma palavra ou frase (PT) primeiro'),
    'Сначала загрузите ролик с субтитрами': ('toast.loadVideoWithSubtitles', 'Load a video with subtitles first', 'Carregue um vídeo com legendas primeiro'),
    'Отметьте строки галочкой в колонке №': ('toast.checkRowsInColumn', 'Check rows in the № column', 'Marque as linhas na coluna №'),
    'Прокси заблокирован настройкой сервера': ('toast.proxyBlockedByServer', 'Proxy blocked by server settings', 'Proxy bloqueado pelo servidor'),
    'Не удалось сохранить словарь на сервере': ('toast.vocabServerSaveFailed', 'Could not save dictionary to server', 'Não foi possível salvar o dicionário no servidor'),
    'Ошибка кнопки записи — обновите страницу': ('toast.recordButtonError', 'Record button error — refresh the page', 'Erro no botão de gravação — atualize a página'),
    'Нажмите «Ввести ссылку…» или обновите страницу': ('toast.clickEnterLinkOrRefresh', 'Tap «Enter link…» or refresh the page', 'Toque em «Inserir link…» ou atualize a página'),
    'Сеть недоступна: загружена офлайн-копия субтитров': ('toast.networkOfflineSubtitles', 'Offline: loaded cached subtitles', 'Sem rede: legendas offline carregadas'),
    'Эту запись можно скрыть, удалив файл из public/books': ('toast.hideDemoBookHint', 'Hide this entry by removing the file from public/books', 'Oculte removendo o arquivo de public/books'),
    'MP3 не получился — скачайте «Как записано» (WebM/M4A)': ('toast.mp3FailedUseWebm', 'MP3 failed — download «As recorded» (WebM/M4A)', 'MP3 falhou — baixe «Como gravado» (WebM/M4A)'),
    'Не удалось (попробуйте фрагмент внутри одного абзаца)': ('toast.highlightTryOneParagraph', 'Failed (try a fragment within one paragraph)', 'Falhou (tente um trecho em um parágrafo)'),
    'Внимание: длительность видео не совпадает с субтитрами': ('toast.videoDurationMismatch', 'Warning: video duration does not match subtitles', 'Aviso: duração do vídeo não coincide com legendas'),
    'Видео запущено — при необходимости включите звук в плеере': ('toast.videoStartedUnmute', 'Video started — unmute in the player if needed', 'Vídeo iniciado — ative o som no player se necessário'),
    'Укажите перевод; пояснение в «Пример» можно добавить позже': ('toast.translationRequiredExampleLater', 'Enter translation; you can add notes in «Example» later', 'Informe a tradução; exemplo pode vir depois'),
    'Не удалось открыть Downloads-файл — переключено на YouTube': ('toast.downloadsOpenFailedYoutube', 'Could not open Downloads file — switched to YouTube', 'Falha ao abrir Downloads — mudou para YouTube'),
    'Для этого ролика нет Downloads-видео — переключено на YouTube': ('toast.noDownloadsForVideoYoutube', 'No Downloads video for this clip — switched to YouTube', 'Sem vídeo em Downloads — mudou para YouTube'),
    'Подчёркнуто (цвет браузера — выберите фрагмент в одном абзаце)': ('toast.highlightBrowserColor', 'Highlighted (browser color — select within one paragraph)', 'Destacado (cor do navegador — um parágrafo)'),
    'Не удалось активировать запись (аудио-контекст). Обновите страницу и попробуйте снова.': ('toast.recordContextFailed', 'Could not activate recording. Refresh and try again.', 'Não foi possível ativar gravação. Atualize e tente de novo.'),
    'Не удалось подставить: нужна одна форма с окончанием -ar, -er или -ir (или введите инфинитив вручную)': ('toast.verbFormHintFailed', 'Could not fill: need -ar, -er or -ir form (or enter infinitive manually)', 'Não foi possível preencher: forma -ar, -er ou -ir'),
    'Ошибка перевода': ('toast.translationError', 'Translation error', 'Erro de tradução'),
    'Сеть': ('toast.networkError', 'Network error', 'Erro de rede'),
}

# Dynamic message keys (used with tf)
DYNAMIC_KEYS = {
    'toast.folderCreated': {
        'ru': 'Папка создана: {name}',
        'en': 'Folder created: {name}',
        'pt': 'Pasta criada: {name}',
    },
    'toast.renamed': {
        'ru': 'Переименовано: {title}',
        'en': 'Renamed: {title}',
        'pt': 'Renomeado: {title}',
    },
    'toast.wordMoved': {
        'ru': 'Слово перемещено в «{folder}»',
        'en': 'Word moved to «{folder}»',
        'pt': 'Palavra movida para «{folder}»',
    },
    'toast.wordAddedToDictionary': {
        'ru': '«{word}» добавлено в словарь',
        'en': '«{word}» added to dictionary',
        'pt': '«{word}» adicionado ao dicionário',
    },
    'toast.proxySaved': {
        'ru': 'Сохранено прокси: {info}',
        'en': 'Proxy saved: {info}',
        'pt': 'Proxy salvo: {info}',
    },
    'toast.proxyWebshare': {
        'ru': 'Прокси Webshare {state}',
        'en': 'Webshare proxy {state}',
        'pt': 'Proxy Webshare {state}',
    },
    'toast.exportExcel': {
        'ru': '{msg} (откройте в Excel)',
        'en': '{msg} (open in Excel)',
        'pt': '{msg} (abra no Excel)',
    },
    'toast.alreadyInDictionaryCount': {
        'ru': 'Уже есть в словаре ({count})',
        'en': 'Already in dictionary ({count})',
        'pt': 'Já no dicionário ({count})',
    },
    'toast.importedCount': {
        'ru': 'Импортировано: {n}',
        'en': 'Imported: {n}',
        'pt': 'Importado: {n}',
    },
    'toast.cardPickError': {
        'ru': 'Ошибка выбора карточки: {message}',
        'en': 'Card selection error: {message}',
        'pt': 'Erro ao escolher cartão: {message}',
    },
    'toast.errorWithMessage': {
        'ru': 'Ошибка: {message}',
        'en': 'Error: {message}',
        'pt': 'Erro: {message}',
    },
    'vocab.placeholderWord': {
        'ru': 'Слово (PT)',
        'en': 'Word (source)',
        'pt': 'Palavra (origem)',
    },
    'vocab.placeholderTranslation': {
        'ru': 'Перевод',
        'en': 'Translation',
        'pt': 'Tradução',
    },
    'vocab.placeholderExample': {
        'ru': 'Пример (опц.)',
        'en': 'Example (optional)',
        'pt': 'Exemplo (opc.)',
    },
    'vocab.quickAddBtn': {
        'ru': 'Добавить',
        'en': 'Add',
        'pt': 'Adicionar',
    },
    'vocab.quickRowTitle': {
        'ru': 'Новая строка',
        'en': 'New row',
        'pt': 'Nova linha',
    },
    'vocab.tag.geral': {'ru': 'Общее', 'en': 'General', 'pt': 'Geral'},
    'vocab.tag.substantivo': {'ru': 'Сущ.', 'en': 'Noun', 'pt': 'Substantivo'},
    'vocab.tag.verbo': {'ru': 'Глагол', 'en': 'Verb', 'pt': 'Verbo'},
    'vocab.tag.adjetivo': {'ru': 'Прил.', 'en': 'Adj.', 'pt': 'Adj.'},
    'vocab.tag.frase': {'ru': 'Фраза', 'en': 'Phrase', 'pt': 'Frase'},
}

DYNAMIC_REPLACEMENTS = [
    ("showToast('Папка создана: ' + name)", "showToast(tf('toast.folderCreated', { name: name }))"),
    ("showToast('Переименовано: ' + newTitle)", "showToast(tf('toast.renamed', { title: newTitle }))"),
    (
        "showToast('Слово перемещено в «' + (newVideoTitle || t('vocab.noFolder')) + '»')",
        "showToast(tf('toast.wordMoved', { folder: newVideoTitle || t('vocab.noFolder') }))",
    ),
    (
        "showToast('«' + popupWord + '» добавлено в словарь')",
        "showToast(tf('toast.wordAddedToDictionary', { word: popupWord }))",
    ),
    (
        "showToast('Сохранено прокси: ' + (d.poolSize || d.count || '?'))",
        "showToast(tf('toast.proxySaved', { info: d.poolSize || d.count || '?' }))",
    ),
    (
        "showToast(__ytWebshareProxyEnabled ? 'Прокси Webshare включён' : 'Прокси Webshare выключен')",
        "showToast(tf('toast.proxyWebshare', { state: __ytWebshareProxyEnabled ? t('toast.proxyOn') : t('toast.proxyOff') }))",
    ),
    (
        "showToast(toastMsg + ' (откройте в Excel)')",
        "showToast(tf('toast.exportExcel', { msg: toastMsg }))",
    ),
    (
        "showToast('Уже есть в словаре (' + skippedDup + ')')",
        "showToast(tf('toast.alreadyInDictionaryCount', { count: skippedDup }))",
    ),
    (
        "showToast((e && e.message) ? e.message : 'Ошибка перевода')",
        "showToast((e && e.message) ? translateToastLiteral(e.message) : t('toast.translationError'))",
    ),
    (
        "showToast(e && e.message ? e.message : 'Сеть')",
        "showToast(e && e.message ? translateToastLiteral(e.message) : t('toast.networkError'))",
    ),
    (
        "showToast(e && e.message ? e.message : 'Не удалось сохранить видео')",
        "showToast(e && e.message ? translateToastLiteral(e.message) : t('toast.videoSaveFailed'))",
    ),
    (
        "showToast(e && e.message ? String(e.message) : 'Не удалось сгенерировать')",
        "showToast(e && e.message ? translateToastLiteral(String(e.message)) : t('toast.generateFailed'))",
    ),
    (
        "showToast('Ошибка выбора карточки: ' + e.message)",
        "showToast(tf('toast.cardPickError', { message: e.message || '' }))",
    ),
    (
        "showToast('Ошибка: ' + e.message)",
        "showToast(tf('toast.errorWithMessage', { message: e.message || '' }))",
    ),
]

# Add missing static keys
CATALOG.update({
    'Не удалось сохранить видео': ('toast.videoSaveFailed', 'Could not save video', 'Não foi possível salvar o vídeo'),
    'Не удалось сгенерировать': ('toast.generateFailed', 'Generation failed', 'Falha na geração'),
})
DYNAMIC_KEYS['toast.proxyOn'] = {'ru': 'включён', 'en': 'enabled', 'pt': 'ativado'}
DYNAMIC_KEYS['toast.proxyOff'] = {'ru': 'выключен', 'en': 'disabled', 'pt': 'desativado'}

# Remove partial prefix entries that would break matching
for k in list(CATALOG.keys()):
    if k.endswith(': ') or k == 'Лимит ':
        del CATALOG[k]


def slug_escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace("'", "\\'")


def build_strings_js() -> str:
    by_key: dict[str, dict[str, str]] = {}
    for ru, (key, en, pt) in CATALOG.items():
        by_key[key] = {'ru': ru, 'en': en, 'pt': pt}
    for key, langs in DYNAMIC_KEYS.items():
        by_key[key] = langs

    lines = [
        '// Toast + error messages — merged into UI_STRINGS at runtime',
        '(function () {',
        "  if (typeof UI_STRINGS === 'undefined') return;",
        '  var extra = { ru: {}, en: {}, pt: {} };',
    ]
    for key in sorted(by_key.keys()):
        langs = by_key[key]
        for lang in ('ru', 'en', 'pt'):
            val = slug_escape(langs[lang])
            lines.append(f"    extra.{lang}['{key}'] = '{val}';")
    lines += [
        "  ['ru', 'en', 'pt'].forEach(function (lang) {",
        '    if (UI_STRINGS[lang]) Object.assign(UI_STRINGS[lang], extra[lang]);',
        '  });',
        '})();',
        '',
        '(function () {',
        "  if (typeof UI_STRINGS === 'undefined') return;",
        '  window.TOAST_BY_RU = {',
    ]
    for ru, (key, _, _) in sorted(CATALOG.items(), key=lambda x: -len(x[0])):
        lines.append(f"    '{slug_escape(ru)}': '{key}',")
    lines += [
        '  };',
        '})();',
        '',
        'function translateToastLiteral(msg) {',
        "  if (!msg || typeof msg !== 'string') return msg;",
        '  try {',
        '    if (window.TOAST_BY_RU && window.TOAST_BY_RU[msg]) return t(window.TOAST_BY_RU[msg]);',
        '  } catch (e) {}',
        '  return msg;',
        '}',
        '',
    ]
    return '\n'.join(lines)


def main() -> None:
    out = Path(__file__).parent / 'website-i18n-toasts-strings.js'
    out.write_text(build_strings_js(), encoding='utf-8')
    meta = {
        'static_count': len(CATALOG),
        'dynamic_replacements': DYNAMIC_REPLACEMENTS,
    }
    Path(__file__).parent.joinpath('website-i18n-toasts-meta.json').write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print('Wrote', out, 'keys', len(CATALOG))


if __name__ == '__main__':
    main()
