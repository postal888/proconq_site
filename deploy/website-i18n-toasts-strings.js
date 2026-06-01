// Toast + error messages — merged into UI_STRINGS at runtime
(function () {
  if (typeof UI_STRINGS === 'undefined') return;
  var extra = { ru: {}, en: {}, pt: {} };
    extra.ru['sync.signInFirst'] = 'Войдите в аккаунт';
    extra.en['sync.signInFirst'] = 'Sign in to your account';
    extra.pt['sync.signInFirst'] = 'Entre na sua conta';
    extra.ru['toast.alreadyInDictionary'] = 'Уже в словаре';
    extra.en['toast.alreadyInDictionary'] = 'Already in dictionary';
    extra.pt['toast.alreadyInDictionary'] = 'Já no dicionário';
    extra.ru['toast.alreadyInDictionaryCount'] = 'Уже есть в словаре ({count})';
    extra.en['toast.alreadyInDictionaryCount'] = 'Already in dictionary ({count})';
    extra.pt['toast.alreadyInDictionaryCount'] = 'Já no dicionário ({count})';
    extra.ru['toast.audioDownloaded'] = 'Аудиофайл скачан';
    extra.en['toast.audioDownloaded'] = 'Audio file downloaded';
    extra.pt['toast.audioDownloaded'] = 'Áudio baixado';
    extra.ru['toast.cardPickError'] = 'Ошибка выбора карточки: {message}';
    extra.en['toast.cardPickError'] = 'Card selection error: {message}';
    extra.pt['toast.cardPickError'] = 'Erro ao escolher cartão: {message}';
    extra.ru['toast.checkFieldsAndAdd'] = 'Проверь поля и нажми «Добавить»';
    extra.en['toast.checkFieldsAndAdd'] = 'Check fields and tap «Add»';
    extra.pt['toast.checkFieldsAndAdd'] = 'Verifique os campos e toque em «Adicionar»';
    extra.ru['toast.checkFragments'] = 'Отметьте фрагменты галочками';
    extra.en['toast.checkFragments'] = 'Check fragments with boxes';
    extra.pt['toast.checkFragments'] = 'Marque os trechos';
    extra.ru['toast.checkRowsInColumn'] = 'Отметьте строки галочкой в колонке №';
    extra.en['toast.checkRowsInColumn'] = 'Check rows in the № column';
    extra.pt['toast.checkRowsInColumn'] = 'Marque as linhas na coluna №';
    extra.ru['toast.clickEnterLinkOrRefresh'] = 'Нажмите «Ввести ссылку…» или обновите страницу';
    extra.en['toast.clickEnterLinkOrRefresh'] = 'Tap «Enter link…» or refresh the page';
    extra.pt['toast.clickEnterLinkOrRefresh'] = 'Toque em «Inserir link…» ou atualize a página';
    extra.ru['toast.commentEmpty'] = 'Комментарий пуст';
    extra.en['toast.commentEmpty'] = 'Comment is empty';
    extra.pt['toast.commentEmpty'] = 'Comentário vazio';
    extra.ru['toast.copied'] = 'Скопировано';
    extra.en['toast.copied'] = 'Copied';
    extra.pt['toast.copied'] = 'Copiado';
    extra.ru['toast.downloadVideoFirst'] = 'Сначала скачайте видео в Downloads';
    extra.en['toast.downloadVideoFirst'] = 'Download the video to Downloads first';
    extra.pt['toast.downloadVideoFirst'] = 'Baixe o vídeo para Downloads primeiro';
    extra.ru['toast.downloadsOpenFailedYoutube'] = 'Не удалось открыть Downloads-файл — переключено на YouTube';
    extra.en['toast.downloadsOpenFailedYoutube'] = 'Could not open Downloads file — switched to YouTube';
    extra.pt['toast.downloadsOpenFailedYoutube'] = 'Falha ao abrir Downloads — mudou para YouTube';
    extra.ru['toast.emptyTranslationRetry'] = 'Пустой ответ — попробуйте ещё раз';
    extra.en['toast.emptyTranslationRetry'] = 'Empty response — try again';
    extra.pt['toast.emptyTranslationRetry'] = 'Resposta vazia — tente de novo';
    extra.ru['toast.enterWordOrPhrasePt'] = 'Сначала введите слово или фразу (PT)';
    extra.en['toast.enterWordOrPhrasePt'] = 'Enter a word or phrase (PT) first';
    extra.pt['toast.enterWordOrPhrasePt'] = 'Digite uma palavra ou frase (PT) primeiro';
    extra.ru['toast.errorWithMessage'] = 'Ошибка: {message}';
    extra.en['toast.errorWithMessage'] = 'Error: {message}';
    extra.pt['toast.errorWithMessage'] = 'Erro: {message}';
    extra.ru['toast.exportExcel'] = '{msg} (откройте в Excel)';
    extra.en['toast.exportExcel'] = '{msg} (open in Excel)';
    extra.pt['toast.exportExcel'] = '{msg} (abra no Excel)';
    extra.ru['toast.fileSaveError'] = 'Ошибка сохранения файла';
    extra.en['toast.fileSaveError'] = 'Could not save file';
    extra.pt['toast.fileSaveError'] = 'Não foi possível salvar o arquivo';
    extra.ru['toast.folderCreated'] = 'Папка создана: {name}';
    extra.en['toast.folderCreated'] = 'Folder created: {name}';
    extra.pt['toast.folderCreated'] = 'Pasta criada: {name}';
    extra.ru['toast.generateFailed'] = 'Не удалось сгенерировать';
    extra.en['toast.generateFailed'] = 'Generation failed';
    extra.pt['toast.generateFailed'] = 'Falha na geração';
    extra.ru['toast.hideDemoBookHint'] = 'Эту запись можно скрыть, удалив файл из public/books';
    extra.en['toast.hideDemoBookHint'] = 'Hide this entry by removing the file from public/books';
    extra.pt['toast.hideDemoBookHint'] = 'Oculte removendo o arquivo de public/books';
    extra.ru['toast.highlightBrowserColor'] = 'Подчёркнуто (цвет браузера — выберите фрагмент в одном абзаце)';
    extra.en['toast.highlightBrowserColor'] = 'Highlighted (browser color — select within one paragraph)';
    extra.pt['toast.highlightBrowserColor'] = 'Destacado (cor do navegador — um parágrafo)';
    extra.ru['toast.highlightTryOneParagraph'] = 'Не удалось (попробуйте фрагмент внутри одного абзаца)';
    extra.en['toast.highlightTryOneParagraph'] = 'Failed (try a fragment within one paragraph)';
    extra.pt['toast.highlightTryOneParagraph'] = 'Falhou (tente um trecho em um parágrafo)';
    extra.ru['toast.highlighted'] = 'Подчёркнуто';
    extra.en['toast.highlighted'] = 'Highlighted';
    extra.pt['toast.highlighted'] = 'Destacado';
    extra.ru['toast.historyCleared'] = 'История роликов очищена';
    extra.en['toast.historyCleared'] = 'Watch history cleared';
    extra.pt['toast.historyCleared'] = 'Histórico de vídeos limpo';
    extra.ru['toast.holdFieldToPaste'] = 'Удерживайте поле → Вставить';
    extra.en['toast.holdFieldToPaste'] = 'Hold the field → Paste';
    extra.pt['toast.holdFieldToPaste'] = 'Segure o campo → Colar';
    extra.ru['toast.imageSaved'] = 'Картинка сохранена';
    extra.en['toast.imageSaved'] = 'Image saved';
    extra.pt['toast.imageSaved'] = 'Imagem salva';
    extra.ru['toast.importedCount'] = 'Импортировано: {n}';
    extra.en['toast.importedCount'] = 'Imported: {n}';
    extra.pt['toast.importedCount'] = 'Importado: {n}';
    extra.ru['toast.listCleared'] = 'Список очищен';
    extra.en['toast.listCleared'] = 'List cleared';
    extra.pt['toast.listCleared'] = 'Lista limpa';
    extra.ru['toast.loadVideoWithSubtitles'] = 'Сначала загрузите ролик с субтитрами';
    extra.en['toast.loadVideoWithSubtitles'] = 'Load a video with subtitles first';
    extra.pt['toast.loadVideoWithSubtitles'] = 'Carregue um vídeo com legendas primeiro';
    extra.ru['toast.minTwoChars'] = 'Введите не менее 2 символов';
    extra.en['toast.minTwoChars'] = 'Enter at least 2 characters';
    extra.pt['toast.minTwoChars'] = 'Digite pelo menos 2 caracteres';
    extra.ru['toast.mp3FailedUseWebm'] = 'MP3 не получился — скачайте «Как записано» (WebM/M4A)';
    extra.en['toast.mp3FailedUseWebm'] = 'MP3 failed — download «As recorded» (WebM/M4A)';
    extra.pt['toast.mp3FailedUseWebm'] = 'MP3 falhou — baixe «Como gravado» (WebM/M4A)';
    extra.ru['toast.mp3Saved'] = 'MP3 сохранён';
    extra.en['toast.mp3Saved'] = 'MP3 saved';
    extra.pt['toast.mp3Saved'] = 'MP3 salvo';
    extra.ru['toast.networkError'] = 'Сеть';
    extra.en['toast.networkError'] = 'Network error';
    extra.pt['toast.networkError'] = 'Erro de rede';
    extra.ru['toast.networkOfflineSubtitles'] = 'Сеть недоступна: загружена офлайн-копия субтитров';
    extra.en['toast.networkOfflineSubtitles'] = 'Offline: loaded cached subtitles';
    extra.pt['toast.networkOfflineSubtitles'] = 'Sem rede: legendas offline carregadas';
    extra.ru['toast.noDownloadsForVideoYoutube'] = 'Для этого ролика нет Downloads-видео — переключено на YouTube';
    extra.en['toast.noDownloadsForVideoYoutube'] = 'No Downloads video for this clip — switched to YouTube';
    extra.pt['toast.noDownloadsForVideoYoutube'] = 'Sem vídeo em Downloads — mudou para YouTube';
    extra.ru['toast.noRowsToExport'] = 'Нет строк для экспорта';
    extra.en['toast.noRowsToExport'] = 'No rows to export';
    extra.pt['toast.noRowsToExport'] = 'Nenhuma linha para exportar';
    extra.ru['toast.noSubtitlesLoadTrack'] = 'Нет субтитров — загрузите дорожку';
    extra.en['toast.noSubtitlesLoadTrack'] = 'No subtitles — load a track';
    extra.pt['toast.noSubtitlesLoadTrack'] = 'Sem legendas — carregue uma faixa';
    extra.ru['toast.noWordsForFilter'] = 'Нет слов по текущему фильтру';
    extra.en['toast.noWordsForFilter'] = 'No words for current filter';
    extra.pt['toast.noWordsForFilter'] = 'Nenhuma palavra neste filtro';
    extra.ru['toast.noteFileSaved'] = 'Файл заметки сохранён';
    extra.en['toast.noteFileSaved'] = 'Note file saved';
    extra.pt['toast.noteFileSaved'] = 'Arquivo de nota salvo';
    extra.ru['toast.nothingToAdd'] = 'Нечего добавлять';
    extra.en['toast.nothingToAdd'] = 'Nothing to add';
    extra.pt['toast.nothingToAdd'] = 'Nada para adicionar';
    extra.ru['toast.offlineCopySaveFailed'] = 'Не удалось сохранить офлайн-копию';
    extra.en['toast.offlineCopySaveFailed'] = 'Could not save offline copy';
    extra.pt['toast.offlineCopySaveFailed'] = 'Não foi possível salvar cópia offline';
    extra.ru['toast.openBookWaitText'] = 'Откройте книгу и дождитесь текста';
    extra.en['toast.openBookWaitText'] = 'Open a book and wait for text';
    extra.pt['toast.openBookWaitText'] = 'Abra um livro e aguarde o texto';
    extra.ru['toast.openYoutubeVideoFirst'] = 'Сначала откройте ролик YouTube';
    extra.en['toast.openYoutubeVideoFirst'] = 'Open a YouTube video first';
    extra.pt['toast.openYoutubeVideoFirst'] = 'Abra um vídeo do YouTube primeiro';
    extra.ru['toast.pasteYoutubeLink'] = 'Вставьте ссылку YouTube';
    extra.en['toast.pasteYoutubeLink'] = 'Paste a YouTube link';
    extra.pt['toast.pasteYoutubeLink'] = 'Cole um link do YouTube';
    extra.ru['toast.phraseCopyDisabled'] = 'Копирование фраз отключено в профиле';
    extra.en['toast.phraseCopyDisabled'] = 'Phrase copy disabled in profile';
    extra.pt['toast.phraseCopyDisabled'] = 'Cópia de frases desativada no perfil';
    extra.ru['toast.phraseSaved'] = 'Фраза сохранена';
    extra.en['toast.phraseSaved'] = 'Phrase saved';
    extra.pt['toast.phraseSaved'] = 'Frase salva';
    extra.ru['toast.pickAtLeastOneWord'] = 'Выбери хотя бы одно слово';
    extra.en['toast.pickAtLeastOneWord'] = 'Select at least one word';
    extra.pt['toast.pickAtLeastOneWord'] = 'Selecione pelo menos uma palavra';
    extra.ru['toast.proxyBlockedByServer'] = 'Прокси заблокирован настройкой сервера';
    extra.en['toast.proxyBlockedByServer'] = 'Proxy blocked by server settings';
    extra.pt['toast.proxyBlockedByServer'] = 'Proxy bloqueado pelo servidor';
    extra.ru['toast.proxyOff'] = 'выключен';
    extra.en['toast.proxyOff'] = 'disabled';
    extra.pt['toast.proxyOff'] = 'desativado';
    extra.ru['toast.proxyOn'] = 'включён';
    extra.en['toast.proxyOn'] = 'enabled';
    extra.pt['toast.proxyOn'] = 'ativado';
    extra.ru['toast.proxySaved'] = 'Сохранено прокси: {info}';
    extra.en['toast.proxySaved'] = 'Proxy saved: {info}';
    extra.pt['toast.proxySaved'] = 'Proxy salvo: {info}';
    extra.ru['toast.proxyToggleFailed'] = 'Не удалось переключить прокси';
    extra.en['toast.proxyToggleFailed'] = 'Could not toggle proxy';
    extra.pt['toast.proxyToggleFailed'] = 'Não foi possível alternar o proxy';
    extra.ru['toast.proxyWebshare'] = 'Прокси Webshare {state}';
    extra.en['toast.proxyWebshare'] = 'Webshare proxy {state}';
    extra.pt['toast.proxyWebshare'] = 'Proxy Webshare {state}';
    extra.ru['toast.recordButtonError'] = 'Ошибка кнопки записи — обновите страницу';
    extra.en['toast.recordButtonError'] = 'Record button error — refresh the page';
    extra.pt['toast.recordButtonError'] = 'Erro no botão de gravação — atualize a página';
    extra.ru['toast.recordContextFailed'] = 'Не удалось активировать запись (аудио-контекст). Обновите страницу и попробуйте снова.';
    extra.en['toast.recordContextFailed'] = 'Could not activate recording. Refresh and try again.';
    extra.pt['toast.recordContextFailed'] = 'Não foi possível ativar gravação. Atualize e tente de novo.';
    extra.ru['toast.recordError'] = 'Ошибка записи';
    extra.en['toast.recordError'] = 'Recording error';
    extra.pt['toast.recordError'] = 'Erro de gravação';
    extra.ru['toast.recordFileBuildFailed'] = 'Не удалось собрать файл записи';
    extra.en['toast.recordFileBuildFailed'] = 'Could not build recording file';
    extra.pt['toast.recordFileBuildFailed'] = 'Não foi possível montar o arquivo';
    extra.ru['toast.recordSoundFirst'] = 'Сначала запишите звук';
    extra.en['toast.recordSoundFirst'] = 'Record audio first';
    extra.pt['toast.recordSoundFirst'] = 'Grave o áudio primeiro';
    extra.ru['toast.recordStartFailed'] = 'Не удалось начать запись';
    extra.en['toast.recordStartFailed'] = 'Could not start recording';
    extra.pt['toast.recordStartFailed'] = 'Não foi possível iniciar a gravação';
    extra.ru['toast.renamed'] = 'Переименовано: {title}';
    extra.en['toast.renamed'] = 'Renamed: {title}';
    extra.pt['toast.renamed'] = 'Renomeado: {title}';
    extra.ru['toast.selectFragmentInSubtitles'] = 'Выделите фрагмент в субтитрах';
    extra.en['toast.selectFragmentInSubtitles'] = 'Select a fragment in subtitles';
    extra.pt['toast.selectFragmentInSubtitles'] = 'Selecione um trecho nas legendas';
    extra.ru['toast.selectPhraseInSubtitles'] = 'Выделите фразу в субтитрах';
    extra.en['toast.selectPhraseInSubtitles'] = 'Select a phrase in subtitles';
    extra.pt['toast.selectPhraseInSubtitles'] = 'Selecione uma frase nas legendas';
    extra.ru['toast.selectText'] = 'Выделите текст';
    extra.en['toast.selectText'] = 'Select some text';
    extra.pt['toast.selectText'] = 'Selecione o texto';
    extra.ru['toast.selectVerbTypeFirst'] = 'Сначала выберите тип «Глагол»';
    extra.en['toast.selectVerbTypeFirst'] = 'Select type «Verb» first';
    extra.pt['toast.selectVerbTypeFirst'] = 'Selecione o tipo «Verbo» primeiro';
    extra.ru['toast.selectionOutsideBook'] = 'Выделение вне текста книги';
    extra.en['toast.selectionOutsideBook'] = 'Selection outside book text';
    extra.pt['toast.selectionOutsideBook'] = 'Seleção fora do texto do livro';
    extra.ru['toast.subtitlesSavedOffline'] = 'Субтитры сохранены офлайн';
    extra.en['toast.subtitlesSavedOffline'] = 'Subtitles saved offline';
    extra.pt['toast.subtitlesSavedOffline'] = 'Legendas salvas offline';
    extra.ru['toast.textAddedToComment'] = 'Текст добавлен в комментарий';
    extra.en['toast.textAddedToComment'] = 'Text added to comment';
    extra.pt['toast.textAddedToComment'] = 'Texto adicionado ao comentário';
    extra.ru['toast.translationEmpty'] = 'Перевод не может быть пустым';
    extra.en['toast.translationEmpty'] = 'Translation cannot be empty';
    extra.pt['toast.translationEmpty'] = 'A tradução não pode estar vazia';
    extra.ru['toast.translationError'] = 'Ошибка перевода';
    extra.en['toast.translationError'] = 'Translation error';
    extra.pt['toast.translationError'] = 'Erro de tradução';
    extra.ru['toast.translationRequiredExampleLater'] = 'Укажите перевод; пояснение в «Пример» можно добавить позже';
    extra.en['toast.translationRequiredExampleLater'] = 'Enter translation; you can add notes in «Example» later';
    extra.pt['toast.translationRequiredExampleLater'] = 'Informe a tradução; exemplo pode vir depois';
    extra.ru['toast.verbFormHintFailed'] = 'Не удалось подставить: нужна одна форма с окончанием -ar, -er или -ir (или введите инфинитив вручную)';
    extra.en['toast.verbFormHintFailed'] = 'Could not fill: need -ar, -er or -ir form (or enter infinitive manually)';
    extra.pt['toast.verbFormHintFailed'] = 'Não foi possível preencher: forma -ar, -er ou -ir';
    extra.ru['toast.verbNeedsInfinitive'] = 'Для глагола укажите инфинитив';
    extra.en['toast.verbNeedsInfinitive'] = 'Verb requires infinitive';
    extra.pt['toast.verbNeedsInfinitive'] = 'Para verbo, informe o infinitivo';
    extra.ru['toast.videoDurationMismatch'] = 'Внимание: длительность видео не совпадает с субтитрами';
    extra.en['toast.videoDurationMismatch'] = 'Warning: video duration does not match subtitles';
    extra.pt['toast.videoDurationMismatch'] = 'Aviso: duração do vídeo não coincide com legendas';
    extra.ru['toast.videoSaveFailed'] = 'Не удалось сохранить видео';
    extra.en['toast.videoSaveFailed'] = 'Could not save video';
    extra.pt['toast.videoSaveFailed'] = 'Não foi possível salvar o vídeo';
    extra.ru['toast.videoSavedOffline'] = 'Видео скачано и сохранено офлайн';
    extra.en['toast.videoSavedOffline'] = 'Video downloaded and saved offline';
    extra.pt['toast.videoSavedOffline'] = 'Vídeo baixado e salvo offline';
    extra.ru['toast.videoStartedUnmute'] = 'Видео запущено — при необходимости включите звук в плеере';
    extra.en['toast.videoStartedUnmute'] = 'Video started — unmute in the player if needed';
    extra.pt['toast.videoStartedUnmute'] = 'Vídeo iniciado — ative o som no player se necessário';
    extra.ru['toast.vocabServerSaveFailed'] = 'Не удалось сохранить словарь на сервере';
    extra.en['toast.vocabServerSaveFailed'] = 'Could not save dictionary to server';
    extra.pt['toast.vocabServerSaveFailed'] = 'Não foi possível salvar o dicionário no servidor';
    extra.ru['toast.wordAdded'] = 'Слово добавлено';
    extra.en['toast.wordAdded'] = 'Word added';
    extra.pt['toast.wordAdded'] = 'Palavra adicionada';
    extra.ru['toast.wordAddedToDictionary'] = '«{word}» добавлено в словарь';
    extra.en['toast.wordAddedToDictionary'] = '«{word}» added to dictionary';
    extra.pt['toast.wordAddedToDictionary'] = '«{word}» adicionado ao dicionário';
    extra.ru['toast.wordEmpty'] = 'Слово не может быть пустым';
    extra.en['toast.wordEmpty'] = 'Word cannot be empty';
    extra.pt['toast.wordEmpty'] = 'A palavra não pode estar vazia';
    extra.ru['toast.wordMoved'] = 'Слово перемещено в «{folder}»';
    extra.en['toast.wordMoved'] = 'Word moved to «{folder}»';
    extra.pt['toast.wordMoved'] = 'Palavra movida para «{folder}»';
    extra.ru['vocab.needWordTranslation'] = 'Заполни слово и перевод!';
    extra.en['vocab.needWordTranslation'] = 'Enter word and translation';
    extra.pt['vocab.needWordTranslation'] = 'Informe palavra e tradução';
    extra.ru['vocab.placeholderExample'] = 'Пример (опц.)';
    extra.en['vocab.placeholderExample'] = 'Example (optional)';
    extra.pt['vocab.placeholderExample'] = 'Exemplo (opc.)';
    extra.ru['vocab.placeholderTranslation'] = 'Перевод';
    extra.en['vocab.placeholderTranslation'] = 'Translation';
    extra.pt['vocab.placeholderTranslation'] = 'Tradução';
    extra.ru['vocab.placeholderWord'] = 'Слово (PT)';
    extra.en['vocab.placeholderWord'] = 'Word (source)';
    extra.pt['vocab.placeholderWord'] = 'Palavra (origem)';
    extra.ru['vocab.quickAddBtn'] = 'Добавить';
    extra.en['vocab.quickAddBtn'] = 'Add';
    extra.pt['vocab.quickAddBtn'] = 'Adicionar';
    extra.ru['vocab.quickRowTitle'] = 'Новая строка';
    extra.en['vocab.quickRowTitle'] = 'New row';
    extra.pt['vocab.quickRowTitle'] = 'Nova linha';
    extra.ru['vocab.tag.adjetivo'] = 'Прил.';
    extra.en['vocab.tag.adjetivo'] = 'Adj.';
    extra.pt['vocab.tag.adjetivo'] = 'Adj.';
    extra.ru['vocab.tag.frase'] = 'Фраза';
    extra.en['vocab.tag.frase'] = 'Phrase';
    extra.pt['vocab.tag.frase'] = 'Frase';
    extra.ru['vocab.tag.geral'] = 'Общее';
    extra.en['vocab.tag.geral'] = 'General';
    extra.pt['vocab.tag.geral'] = 'Geral';
    extra.ru['vocab.tag.substantivo'] = 'Сущ.';
    extra.en['vocab.tag.substantivo'] = 'Noun';
    extra.pt['vocab.tag.substantivo'] = 'Substantivo';
    extra.ru['vocab.tag.verbo'] = 'Глагол';
    extra.en['vocab.tag.verbo'] = 'Verb';
    extra.pt['vocab.tag.verbo'] = 'Verbo';
  ['ru', 'en', 'pt'].forEach(function (lang) {
    if (UI_STRINGS[lang]) Object.assign(UI_STRINGS[lang], extra[lang]);
  });
})();

(function () {
  if (typeof UI_STRINGS === 'undefined') return;
  window.TOAST_BY_RU = {
    'Не удалось подставить: нужна одна форма с окончанием -ar, -er или -ir (или введите инфинитив вручную)': 'toast.verbFormHintFailed',
    'Не удалось активировать запись (аудио-контекст). Обновите страницу и попробуйте снова.': 'toast.recordContextFailed',
    'Подчёркнуто (цвет браузера — выберите фрагмент в одном абзаце)': 'toast.highlightBrowserColor',
    'Для этого ролика нет Downloads-видео — переключено на YouTube': 'toast.noDownloadsForVideoYoutube',
    'Укажите перевод; пояснение в «Пример» можно добавить позже': 'toast.translationRequiredExampleLater',
    'Не удалось открыть Downloads-файл — переключено на YouTube': 'toast.downloadsOpenFailedYoutube',
    'Видео запущено — при необходимости включите звук в плеере': 'toast.videoStartedUnmute',
    'Внимание: длительность видео не совпадает с субтитрами': 'toast.videoDurationMismatch',
    'MP3 не получился — скачайте «Как записано» (WebM/M4A)': 'toast.mp3FailedUseWebm',
    'Не удалось (попробуйте фрагмент внутри одного абзаца)': 'toast.highlightTryOneParagraph',
    'Эту запись можно скрыть, удалив файл из public/books': 'toast.hideDemoBookHint',
    'Сеть недоступна: загружена офлайн-копия субтитров': 'toast.networkOfflineSubtitles',
    'Нажмите «Ввести ссылку…» или обновите страницу': 'toast.clickEnterLinkOrRefresh',
    'Ошибка кнопки записи — обновите страницу': 'toast.recordButtonError',
    'Не удалось сохранить словарь на сервере': 'toast.vocabServerSaveFailed',
    'Прокси заблокирован настройкой сервера': 'toast.proxyBlockedByServer',
    'Копирование фраз отключено в профиле': 'toast.phraseCopyDisabled',
    'Сначала введите слово или фразу (PT)': 'toast.enterWordOrPhrasePt',
    'Сначала загрузите ролик с субтитрами': 'toast.loadVideoWithSubtitles',
    'Отметьте строки галочкой в колонке №': 'toast.checkRowsInColumn',
    'Сначала скачайте видео в Downloads': 'toast.downloadVideoFirst',
    'Пустой ответ — попробуйте ещё раз': 'toast.emptyTranslationRetry',
    'Не удалось сохранить офлайн-копию': 'toast.offlineCopySaveFailed',
    'Откройте книгу и дождитесь текста': 'toast.openBookWaitText',
    'Нет субтитров — загрузите дорожку': 'toast.noSubtitlesLoadTrack',
    'Видео скачано и сохранено офлайн': 'toast.videoSavedOffline',
    'Проверь поля и нажми «Добавить»': 'toast.checkFieldsAndAdd',
    'Сначала откройте ролик YouTube': 'toast.openYoutubeVideoFirst',
    'Не удалось собрать файл записи': 'toast.recordFileBuildFailed',
    'Сначала выберите тип «Глагол»': 'toast.selectVerbTypeFirst',
    'Для глагола укажите инфинитив': 'toast.verbNeedsInfinitive',
    'Выделите фрагмент в субтитрах': 'toast.selectFragmentInSubtitles',
    'Не удалось переключить прокси': 'toast.proxyToggleFailed',
    'Отметьте фрагменты галочками': 'toast.checkFragments',
    'Текст добавлен в комментарий': 'toast.textAddedToComment',
    'Нет слов по текущему фильтру': 'toast.noWordsForFilter',
    'Перевод не может быть пустым': 'toast.translationEmpty',
    'Удерживайте поле → Вставить': 'toast.holdFieldToPaste',
    'Введите не менее 2 символов': 'toast.minTwoChars',
    'Выделите фразу в субтитрах': 'toast.selectPhraseInSubtitles',
    'Выделение вне текста книги': 'toast.selectionOutsideBook',
    'Слово не может быть пустым': 'toast.wordEmpty',
    'Не удалось сохранить видео': 'toast.videoSaveFailed',
    'Субтитры сохранены офлайн': 'toast.subtitlesSavedOffline',
    'Выбери хотя бы одно слово': 'toast.pickAtLeastOneWord',
    'Заполни слово и перевод!': 'vocab.needWordTranslation',
    'Не удалось начать запись': 'toast.recordStartFailed',
    'Не удалось сгенерировать': 'toast.generateFailed',
    'Вставьте ссылку YouTube': 'toast.pasteYoutubeLink',
    'История роликов очищена': 'toast.historyCleared',
    'Укажите слово и перевод': 'vocab.needWordTranslation',
    'Ошибка сохранения файла': 'toast.fileSaveError',
    'Нет строк для экспорта': 'toast.noRowsToExport',
    'Сначала запишите звук': 'toast.recordSoundFirst',
    'Файл заметки сохранён': 'toast.noteFileSaved',
    'Картинка сохранена': 'toast.imageSaved',
    'Войдите в аккаунт': 'sync.signInFirst',
    'Аудиофайл скачан': 'toast.audioDownloaded',
    'Нечего добавлять': 'toast.nothingToAdd',
    'Комментарий пуст': 'toast.commentEmpty',
    'Слово добавлено': 'toast.wordAdded',
    'Фраза сохранена': 'toast.phraseSaved',
    'Ошибка перевода': 'toast.translationError',
    'Выделите текст': 'toast.selectText',
    'Ошибка записи': 'toast.recordError',
    'Уже в словаре': 'toast.alreadyInDictionary',
    'Список очищен': 'toast.listCleared',
    'MP3 сохранён': 'toast.mp3Saved',
    'Подчёркнуто': 'toast.highlighted',
    'Скопировано': 'toast.copied',
    'Сеть': 'toast.networkError',
  };
})();

function translateToastLiteral(msg) {
  if (!msg || typeof msg !== 'string') return msg;
  try {
    if (window.TOAST_BY_RU && window.TOAST_BY_RU[msg]) return t(window.TOAST_BY_RU[msg]);
  } catch (e) {}
  return msg;
}
