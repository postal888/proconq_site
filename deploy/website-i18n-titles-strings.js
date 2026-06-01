(function () {
  if (typeof UI_STRINGS === 'undefined') return;
  var extra = {
    ru: {
      'ui.title.undoDelete': 'Вернуть удалённое слово',
      'ui.title.vocabFontSize': 'Размер шрифта в таблице и карточках',
      'ui.title.vocabFont': 'Начертание',
      'ui.title.speakSelected': 'Сначала отметьте строки галочкой в колонке №',
      'ui.title.stopTts': 'Остановить озвучку',
      'ui.title.ytLang': 'Предпочитаемый язык дорожки',
      'ui.title.hoverTranslate': 'Источник перевода слова по наведению',
      'ui.title.autoTranslate': 'Подставить перевод через API (как субтитры)',
    },
    en: {
      'ui.title.undoDelete': 'Restore deleted word',
      'ui.title.vocabFontSize': 'Font size in table and cards',
      'ui.title.vocabFont': 'Typeface',
      'ui.title.speakSelected': 'Select rows with the checkbox in the # column first',
      'ui.title.stopTts': 'Stop speech',
      'ui.title.ytLang': 'Preferred subtitle track language',
      'ui.title.hoverTranslate': 'Hover word translation source',
      'ui.title.autoTranslate': 'Fill translation via API (like subtitles)',
    },
    pt: {
      'ui.title.undoDelete': 'Restaurar palavra excluída',
      'ui.title.vocabFontSize': 'Tamanho da fonte na tabela e cartões',
      'ui.title.vocabFont': 'Fonte',
      'ui.title.speakSelected': 'Marque as linhas com a caixa na coluna №',
      'ui.title.stopTts': 'Parar áudio',
      'ui.title.ytLang': 'Idioma preferido da faixa de legendas',
      'ui.title.hoverTranslate': 'Fonte da tradução ao passar o mouse',
      'ui.title.autoTranslate': 'Preencher tradução via API (como legendas)',
    },
  };
  ['ru', 'en', 'pt'].forEach(function (lang) {
    Object.keys(extra[lang]).forEach(function (key) {
      UI_STRINGS[lang][key] = extra[lang][key];
    });
  });
})();
