
// Card / subtitle — two language pickers
(function () {
  if (typeof UI_STRINGS === 'undefined') return;
  var extra = {
    ru: {
      'profile.translationLangsHint': 'Выберите 2 языка.',
    },
    en: {
      'profile.translationLangsHint': 'Choose 2 languages.',
    },
    pt: {
      'profile.translationLangsHint': 'Escolha 2 idiomas.',
    },
  };
  ['ru', 'en', 'pt'].forEach(function (lang) {
    if (UI_STRINGS[lang]) Object.assign(UI_STRINGS[lang], extra[lang]);
  });
})();
