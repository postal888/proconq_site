/**
 * Verbos — таблицы спряжений и тест (из Port_mob).
 * Данные: /portuprep-verbos-data.json
 */
(function () {
  'use strict';

  var STORAGE_PERSONS = 'portuprep-verbos-persons-v1';
  var STORAGE_VERBS = 'portuprep-verbos-filter-v1';
  var STORAGE_TENSES = 'portuprep-verbos-tenses-v1';

  var PERSON_COL_LABEL = {
    eu: 'eu',
    tu: 'tu',
    voce_ele_ela: 'você',
    nos: 'nós',
    eles_voces: 'vocês',
  };

  var data = null;
  var state = {
    subTab: 'tables',
    personOn: {},
    verbIdsOn: {},
    tenseOn: {},
    quiz: null,
  };

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function verbCardTenseSuffix(verbId, cardId) {
    var prefix = verbId + '-';
    return cardId.indexOf(prefix) === 0 ? cardId.slice(prefix.length) : cardId;
  }

  function stripParenQuePrefix(text) {
    return text.replace(/\(([^)]+)\)\s*/g, function (_, inner) {
      return inner.trim() + ' ';
    }).trim();
  }

  function formatFormaLine(card, key) {
    if (!card.forms) return null;
    var raw = card.forms[key];
    if (raw == null || raw === '') return null;
    var tense = card.tenseLabel.toLowerCase();
    if (tense.indexOf('infinitivo pessoal') >= 0) {
      if (key === 'eu') return null;
      if (key === 'tu') return raw;
      return 'para ' + raw;
    }
    if (tense.indexOf('imperativo') >= 0) {
      if (key === 'voce_ele_ela') return raw + ' você';
      if (key === 'tu') return 'tu ' + raw;
      return raw;
    }
    if (raw.indexOf('(') >= 0 && raw.indexOf('que') >= 0) return stripParenQuePrefix(raw);
    return PERSON_COL_LABEL[key] + ' ' + raw;
  }

  function formaChaveCell(card, personOn) {
    if (card.forms === null) return '—';
    var lines = [];
    for (var i = 0; i < data.personOptions.length; i++) {
      var key = data.personOptions[i].key;
      if (!personOn[key]) continue;
      var line = formatFormaLine(card, key);
      if (line) lines.push(line);
    }
    return lines.length ? lines.join('\n') : '(отметьте хотя бы одно лицо)';
  }

  function exemploCell(card) {
    if (card.forms === null) return card.infoNote || '—';
    return card.exampleEu || '—';
  }

  function exemploHtml(card) {
    var text = exemploCell(card);
    var tip = data.tooltips[card.id];
    if (!tip) return escapeHtml(text);
    var a11y = [text, tip.en, tip.note || ''].filter(Boolean).join('. ');
    return (
      '<span class="verb-exemplo-tip-host" tabindex="0" aria-label="' +
      escapeHtml(a11y) +
      '">' +
      '<span class="verb-exemplo-tip-text">' +
      escapeHtml(text) +
      '</span>' +
      '<span class="verb-exemplo-tip-pop" role="tooltip">' +
      '<span class="verb-exemplo-tip-head">EN</span>' +
      '<span class="verb-exemplo-tip-en">' +
      escapeHtml(tip.en) +
      '</span>' +
      (tip.note
        ? '<span class="verb-exemplo-tip-note">' + escapeHtml(tip.note) + '</span>'
        : '') +
      '</span></span>'
    );
  }

  function defaultPersonSelection() {
    var o = {};
    data.personOptions.forEach(function (p) {
      o[p.key] = p.key !== 'tu';
    });
    return o;
  }

  function defaultTenseSelection() {
    var o = {};
    data.tenseOptions.forEach(function (t) {
      o[t.key] = true;
    });
    return o;
  }

  function loadPrefs() {
    state.personOn = defaultPersonSelection();
    state.tenseOn = defaultTenseSelection();
    state.verbIdsOn = {};
    data.decks.forEach(function (d) {
      state.verbIdsOn[d.id] = true;
    });
    try {
      var p = localStorage.getItem(STORAGE_PERSONS);
      if (p) Object.assign(state.personOn, JSON.parse(p));
      var v = localStorage.getItem(STORAGE_VERBS);
      if (v) Object.assign(state.verbIdsOn, JSON.parse(v));
      var t = localStorage.getItem(STORAGE_TENSES);
      if (t) Object.assign(state.tenseOn, Object.assign(defaultTenseSelection(), JSON.parse(t)));
    } catch (e) {}
  }

  function savePrefs() {
    try {
      localStorage.setItem(STORAGE_PERSONS, JSON.stringify(state.personOn));
      localStorage.setItem(STORAGE_VERBS, JSON.stringify(state.verbIdsOn));
      localStorage.setItem(STORAGE_TENSES, JSON.stringify(state.tenseOn));
    } catch (e) {}
  }

  function rowMatchesTenseFilter(verb, card) {
    var suffix = verbCardTenseSuffix(verb.id, card.id);
    var v = state.tenseOn[suffix];
    return v !== false && (v !== undefined ? v : true);
  }

  function renderFiltersHtml() {
    var persons = data.personOptions
      .map(function (p) {
        return (
          '<label class="verbos-check"><input type="checkbox" data-verbos-person="' +
          p.key +
          '"' +
          (state.personOn[p.key] ? ' checked' : '') +
          '> ' +
          escapeHtml(p.label) +
          '</label>'
        );
      })
      .join('');
    var verbs = data.decks
      .map(function (d) {
        return (
          '<label class="verbos-check verbos-check-verb"><input type="checkbox" data-verbos-verb="' +
          escapeHtml(d.id) +
          '"' +
          (state.verbIdsOn[d.id] ? ' checked' : '') +
          '> ' +
          escapeHtml(d.title) +
          '</label>'
        );
      })
      .join('');
    var tenses = data.tenseOptions
      .map(function (t) {
        return (
          '<label class="verbos-check verbos-check-verb"><input type="checkbox" data-verbos-tense="' +
          escapeHtml(t.key) +
          '"' +
          (state.tenseOn[t.key] !== false ? ' checked' : '') +
          '> ' +
          escapeHtml(t.label) +
          '</label>'
        );
      })
      .join('');
    return (
      '<fieldset class="verbos-fieldset"><legend>Форма — лица</legend><div class="verbos-check-row">' +
      persons +
      '</div></fieldset>' +
      '<fieldset class="verbos-fieldset"><legend>Глаголы</legend>' +
      '<div class="verbos-chip-actions"><button type="button" class="btn btn-ghost btn-sm" data-verbos-all-verbs="1">Все</button>' +
      '<button type="button" class="btn btn-ghost btn-sm" data-verbos-clear-verbs="1">Снять</button></div>' +
      '<div class="verbos-verb-grid">' +
      verbs +
      '</div></fieldset>' +
      '<fieldset class="verbos-fieldset"><legend>Времена / конструкции</legend>' +
      '<div class="verbos-chip-actions"><button type="button" class="btn btn-ghost btn-sm" data-verbos-all-tenses="1">Все</button>' +
      '<button type="button" class="btn btn-ghost btn-sm" data-verbos-clear-tenses="1">Снять</button></div>' +
      '<div class="verbos-verb-grid">' +
      tenses +
      '</div></fieldset>'
    );
  }

  function renderTablesHtml() {
    var visible = data.decks.filter(function (d) {
      return state.verbIdsOn[d.id];
    });
    var hasVerb = visible.length > 0;
    var hasTense = data.tenseOptions.some(function (t) {
      return state.tenseOn[t.key] !== false;
    });
    if (!hasVerb) return '<p class="verbos-warn">Выберите хотя бы один глагол.</p>';
    if (!hasTense) return '<p class="verbos-warn">Отметьте хотя бы одно время.</p>';
    return (
      '<div class="verb-tables-stack">' +
      visible
        .map(function (verb) {
          var rows = verb.cards
            .filter(function (card) {
              return rowMatchesTenseFilter(verb, card);
            })
            .map(function (card) {
              return (
                '<tr><td class="verb-table-tempo">' +
                escapeHtml(card.tenseLabel) +
                '</td><td class="verb-table-forma"><span class="verb-table-forma-inner">' +
                escapeHtml(formaChaveCell(card, state.personOn)) +
                '</span></td><td class="verb-table-exemplo">' +
                exemploHtml(card) +
                '</td></tr>'
              );
            })
            .join('');
          return (
            '<div class="verb-table-block"><h3 class="verb-table-verb-title">' +
            escapeHtml(verb.title) +
            '</h3><p class="verb-table-infinitive mono">' +
            escapeHtml(verb.infinitive) +
            '</p><div class="verb-table-scroll"><table class="verb-table"><thead><tr>' +
            '<th>Время</th><th>Форма</th><th>Пример</th></tr></thead><tbody>' +
            rows +
            '</tbody></table></div></div>'
          );
        })
        .join('') +
      '</div>'
    );
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  function collectQuizSlots() {
    var slots = [];
    data.decks.forEach(function (verb) {
      if (!state.verbIdsOn[verb.id]) return;
      verb.cards.forEach(function (card) {
        if (!card.forms) return;
        data.personOptions.forEach(function (p) {
          if (!state.personOn[p.key]) return;
          var raw = card.forms[p.key];
          if (raw == null || String(raw).trim() === '') return;
          slots.push({ verb: verb, card: card, personKey: p.key, correct: String(raw).trim() });
        });
      });
    });
    return slots;
  }

  function buildQuizItem(slot, poolDecks) {
    var correct = slot.correct;
    var dist = [];
    var sameCard = [];
    if (slot.card.forms) {
      data.personOptions.forEach(function (p) {
        if (p.key === slot.personKey) return;
        var t = slot.card.forms[p.key];
        if (t) {
          var tr = String(t).trim();
          if (tr !== correct) sameCard.push(tr);
        }
      });
    }
    shuffle(sameCard).forEach(function (x) {
      if (dist.length >= 3) return;
      if (dist.indexOf(x) < 0) dist.push(x);
    });
    var allForms = [];
    var seen = {};
    poolDecks.forEach(function (v) {
      v.cards.forEach(function (c) {
        if (!c.forms) return;
        data.personOptions.forEach(function (p) {
          var t = c.forms[p.key];
          if (!t) return;
          var tr = String(t).trim();
          if (!seen[tr]) {
            seen[tr] = true;
            allForms.push(tr);
          }
        });
      });
    });
    shuffle(allForms).forEach(function (x) {
      if (dist.length >= 3) return;
      if (x !== correct && dist.indexOf(x) < 0) dist.push(x);
    });
    var indexed = [{ text: correct, ok: true }].concat(
      dist.slice(0, 3).map(function (t) {
        return { text: t, ok: false };
      }),
    );
    var shuffled = shuffle(indexed);
    var correctIdx = shuffled.findIndex(function (x) {
      return x.ok;
    });
    var personLabel =
      (data.personOptions.find(function (p) {
        return p.key === slot.personKey;
      }) || {}).label || slot.personKey;
    return {
      verbTitle: slot.verb.title,
      tenseLabel: slot.card.tenseLabel,
      personLabel: personLabel,
      infinitive: slot.verb.infinitive,
      shuffledOptions: shuffled.map(function (x) {
        return x.text;
      }),
      correctShuffledIndex: correctIdx,
    };
  }

  function renderTestSetupHtml() {
    var maxPossible = collectQuizSlots().length;
    return (
      '<section class="verbos-test-view">' +
      '<p class="verbos-intro">Выберите глаголы и лица. В каждом вопросе — время и лицо; выберите правильную форму из четырёх.</p>' +
      (state.quiz && state.quiz.setupError
        ? '<p class="verbos-warn">' + escapeHtml(state.quiz.setupError) + '</p>'
        : '') +
      renderFiltersHtml() +
      '<div class="verbos-test-row-num"><label for="verb-test-qty">Число вопросов <span class="test-setup-muted">(макс. ' +
      maxPossible +
      ')</span></label>' +
      '<input id="verb-test-qty" type="number" min="1" max="' +
      Math.max(1, maxPossible) +
      '" value="' +
      (state.quiz ? state.quiz.questionTarget : Math.min(20, maxPossible)) +
      '"></div>' +
      '<p class="verbos-test-slots">Возможных комбинаций: <strong>' +
      maxPossible +
      '</strong></p>' +
      '<button type="button" class="btn btn-primary" data-verbos-start-quiz="1"' +
      (maxPossible === 0 ? ' disabled' : '') +
      '>Начать тест</button></section>'
    );
  }

  function renderTestQuizHtml() {
    var q = state.quiz;
    if (!q || !q.items.length) return '<p class="verbos-warn">Загрузка…</p>';
    if (q.phase === 'done') {
      return (
        '<section class="verbos-test-done"><h2>Тест завершён</h2><p>Результат: <strong>' +
        q.score +
        ' / ' +
        q.items.length +
        '</strong></p>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">' +
        '<button type="button" class="btn btn-ghost btn-sm" data-verbos-back-setup="1">Настройка</button>' +
        '<button type="button" class="btn btn-primary btn-sm" data-verbos-restart-quiz="1">Ещё раз</button></div></section>'
      );
    }
    var cur = q.items[q.idx];
    var opts = cur.shuffledOptions
      .map(function (opt, i) {
        var cls = '';
        if (q.picked !== null) {
          if (i === cur.correctShuffledIndex) cls = ' correct';
          else if (i === q.picked) cls = ' wrong';
        }
        return (
          '<button type="button" class="verbos-quiz-opt' +
          cls +
          '"' +
          (q.picked !== null ? ' disabled' : '') +
          ' data-verbos-pick="' +
          i +
          '">' +
          escapeHtml(opt) +
          '</button>'
        );
      })
      .join('');
    return (
      '<section class="verbos-test-quiz-wrap"><span class="test-kind-chip">' +
      escapeHtml(cur.verbTitle) +
      ' · ' +
      escapeHtml(cur.infinitive) +
      '</span><p class="verbos-test-slots">Вопрос ' +
      (q.idx + 1) +
      ' / ' +
      q.items.length +
      '</p><p class="verbos-test-prompt-lead">Какая форма верна?</p>' +
      '<h2 class="verbos-test-prompt"><span class="verbos-test-tense">' +
      escapeHtml(cur.tenseLabel) +
      '</span><span class="verbos-test-person">Лицо: ' +
      escapeHtml(cur.personLabel) +
      '</span></h2><div class="verbos-quiz-options">' +
      opts +
      '</div><button type="button" class="btn btn-ghost btn-sm" data-verbos-back-setup="1">Выйти</button></section>'
    );
  }

  function render() {
    var root = document.getElementById('verbos-root');
    if (!root || !data) return;
    var tablesPane =
      state.subTab === 'tables'
        ? '<section class="verbos-view"><h2 class="verbos-title">Глаголы и спряжения</h2>' +
          '<p class="verbos-intro">Таблица как в profconq: колонка <strong>Форма</strong> по отмеченным лицам, строки — по отмеченным временам. Наведите на пример — перевод EN.</p>' +
          renderFiltersHtml() +
          renderTablesHtml() +
          '</section>'
        : '';
    var testPane = state.subTab === 'test' ? (state.quiz && state.quiz.phase !== 'setup' ? renderTestQuizHtml() : renderTestSetupHtml()) : '';
    root.innerHTML =
      '<div class="verbos-subtabs">' +
      '<button type="button" class="btn btn-sm ' +
      (state.subTab === 'tables' ? 'btn-primary' : 'btn-ghost') +
      '" data-verbos-subtab="tables">Таблицы</button>' +
      '<button type="button" class="btn btn-sm ' +
      (state.subTab === 'test' ? 'btn-primary' : 'btn-ghost') +
      '" data-verbos-subtab="test">Тест</button>' +
      '</div>' +
      '<div id="verbos-pane-tables">' +
      tablesPane +
      '</div>' +
      '<div id="verbos-pane-test">' +
      testPane +
      '</div>';
    try {
      if (typeof lucide !== 'undefined' && lucide.createIcons) lucide.createIcons({ root: root });
    } catch (e) {}
  }

  function onRootClick(ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    var sub = t.closest('[data-verbos-subtab]');
    if (sub) {
      state.subTab = sub.getAttribute('data-verbos-subtab');
      if (state.subTab === 'test' && !state.quiz) {
        state.quiz = { phase: 'setup', questionTarget: 20, setupError: '', items: [], idx: 0, picked: null, score: 0 };
      }
      render();
      return;
    }
    var personInp = t.closest('[data-verbos-person]');
    if (personInp && personInp.getAttribute('data-verbos-person')) {
      var pk = personInp.getAttribute('data-verbos-person');
      state.personOn[pk] = personInp.checked;
      savePrefs();
      render();
      return;
    }
    var verbInp = t.closest('[data-verbos-verb]');
    if (verbInp && verbInp.getAttribute('data-verbos-verb')) {
      state.verbIdsOn[verbInp.getAttribute('data-verbos-verb')] = verbInp.checked;
      savePrefs();
      render();
      return;
    }
    var tenseInp = t.closest('[data-verbos-tense]');
    if (tenseInp && tenseInp.getAttribute('data-verbos-tense')) {
      state.tenseOn[tenseInp.getAttribute('data-verbos-tense')] = tenseInp.checked;
      savePrefs();
      render();
      return;
    }
    if (t.closest('[data-verbos-all-verbs]')) {
      data.decks.forEach(function (d) {
        state.verbIdsOn[d.id] = true;
      });
      savePrefs();
      render();
      return;
    }
    if (t.closest('[data-verbos-clear-verbs]')) {
      data.decks.forEach(function (d) {
        state.verbIdsOn[d.id] = false;
      });
      savePrefs();
      render();
      return;
    }
    if (t.closest('[data-verbos-all-tenses]')) {
      state.tenseOn = defaultTenseSelection();
      savePrefs();
      render();
      return;
    }
    if (t.closest('[data-verbos-clear-tenses]')) {
      data.tenseOptions.forEach(function (x) {
        state.tenseOn[x.key] = false;
      });
      savePrefs();
      render();
      return;
    }
    if (t.closest('[data-verbos-start-quiz]')) {
      var slots = collectQuizSlots();
      if (!slots.length) {
        state.quiz.setupError = 'Отметьте глаголы и лица с доступными формами.';
        render();
        return;
      }
      var qtyEl = document.getElementById('verb-test-qty');
      var want = qtyEl ? parseInt(qtyEl.value, 10) : 20;
      if (!isFinite(want)) want = 20;
      var n = Math.min(Math.max(1, want), slots.length);
      var pool = data.decks.filter(function (d) {
        return state.verbIdsOn[d.id];
      });
      state.quiz = {
        phase: 'quiz',
        questionTarget: n,
        setupError: '',
        items: shuffle(slots)
          .slice(0, n)
          .map(function (s) {
            return buildQuizItem(s, pool);
          }),
        idx: 0,
        picked: null,
        score: 0,
      };
      render();
      return;
    }
    if (t.closest('[data-verbos-back-setup]')) {
      state.quiz = { phase: 'setup', questionTarget: 20, setupError: '', items: [], idx: 0, picked: null, score: 0 };
      render();
      return;
    }
    if (t.closest('[data-verbos-restart-quiz]')) {
      var btn = document.querySelector('[data-verbos-start-quiz]');
      if (btn) btn.click();
      else {
        state.quiz.phase = 'setup';
        render();
        setTimeout(function () {
          var b2 = document.querySelector('[data-verbos-start-quiz]');
          if (b2) b2.click();
        }, 0);
      }
      return;
    }
    var pickBtn = t.closest('[data-verbos-pick]');
    if (pickBtn && state.quiz && state.quiz.phase === 'quiz' && state.quiz.picked === null) {
      var pi = parseInt(pickBtn.getAttribute('data-verbos-pick'), 10);
      var cur = state.quiz.items[state.quiz.idx];
      state.quiz.picked = pi;
      if (pi === cur.correctShuffledIndex) state.quiz.score++;
      render();
      setTimeout(function () {
        if (!state.quiz) return;
        state.quiz.picked = null;
        if (state.quiz.idx + 1 >= state.quiz.items.length) state.quiz.phase = 'done';
        else state.quiz.idx++;
        render();
      }, 1000);
    }
  }

  function bindRoot() {
    var root = document.getElementById('verbos-root');
    if (!root || root.dataset.bound === '1') return;
    root.dataset.bound = '1';
    root.addEventListener('click', onRootClick);
    root.addEventListener('change', function (ev) {
      var t = ev.target;
      if (t && t.matches && t.matches('[data-verbos-person],[data-verbos-verb],[data-verbos-tense]')) {
        onRootClick(ev);
      }
    });
  }

  async function ensureData() {
    if (data) return data;
    var r = await fetch('/portuprep-verbos-data.json');
    if (!r.ok) throw new Error('HTTP ' + r.status);
    data = await r.json();
    loadPrefs();
    return data;
  }

  window.initVerbosView = async function () {
    var root = document.getElementById('verbos-root');
    if (!root) return;
    bindRoot();
    root.innerHTML = '<p class="verbos-intro">Загрузка глаголов…</p>';
    try {
      await ensureData();
      if (!state.quiz && state.subTab === 'test') {
        state.quiz = { phase: 'setup', questionTarget: 20, setupError: '', items: [], idx: 0, picked: null, score: 0 };
      }
      render();
    } catch (e) {
      root.innerHTML =
        '<p class="verbos-warn">Не удалось загрузить данные глаголов. Запустите: npm run build:verbos-data</p>';
      console.error(e);
    }
  };
})();
