#!/usr/bin/env python3
"""Patch live website: promo codes + dynamic word limits."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PATCH_DIR = Path('/var/www/proficonq/tutor-app/patches')
WORD_LIMIT_JS = PATCH_DIR / 'website-word-limit.js'
PROMO_JS = PATCH_DIR / 'website-promo.js'
MARKER = 'profile-word-limit-row'


def inject_js(html: str, js_path: Path, anchor: str, marker: str) -> str:
    if marker in html:
        return html
    js = js_path.read_text(encoding='utf-8')
    if anchor not in html:
        raise SystemExit(f'Anchor not found for {js_path.name}: {anchor!r}')
    return html.replace(anchor, js + '\n' + anchor, 1)


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')

    # Replace old word-limit helper if present (upgrade in place)
    old_limit_start = 'var FREE_VOCAB_WORD_LIMIT = 10;'
    if old_limit_start in html and 'vocabEffectiveLimit' not in html:
        html = inject_js(
            html,
            WORD_LIMIT_JS,
            old_limit_start,
            'vocabEffectiveLimit',
        )
    elif 'vocabEffectiveLimit' not in html:
        html = inject_js(
            html,
            WORD_LIMIT_JS,
            'function vocabInsertNewWord(payload) {',
            'vocabEffectiveLimit',
        )

    if 'function redeemPromoCode()' not in html:
        html = inject_js(
            html,
            PROMO_JS,
            'function profileRenderAccount() {',
            'function redeemPromoCode()',
        )

    account_card = (
        '            <div class="profile-account-row">\n'
        '              <div>\n'
        '                <div class="profile-account-email" id="profile-account-email">—</div>\n'
        '                <div class="profile-account-plan" id="profile-account-plan"></div>\n'
        '              </div>\n'
        '              <button type="button" class="btn btn-ghost btn-sm" onclick="authLogout()">'
    )
    promo_html = (
        '            <div class="profile-account-row">\n'
        '              <div>\n'
        '                <div class="profile-account-email" id="profile-account-email">—</div>\n'
        '                <div class="profile-account-plan" id="profile-account-plan"></div>\n'
        '                <div id="profile-word-limit-row" class="profile-setting-desc" style="margin-top:8px"></div>\n'
        '              </div>\n'
        '              <button type="button" class="btn btn-ghost btn-sm" onclick="authLogout()">'
    )
    if MARKER not in html and account_card in html:
        html = html.replace(account_card, promo_html, 1)

    promo_block = (
        '            <div class="profile-promo-block" id="profile-promo-block" style="margin-top:14px">\n'
        '              <div class="profile-setting-label" data-i18n="promo.section">Promo code</div>\n'
        '              <div style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap">\n'
        '                <input type="text" id="profile-promo-code" class="input" '
        'placeholder="FRIEND100" style="flex:1;min-width:120px;text-transform:uppercase" '
        'data-i18n-placeholder="promo.placeholder">\n'
        '                <button type="button" class="btn btn-primary btn-sm" onclick="redeemPromoCode()" '
        'data-i18n="promo.redeem">Apply</button>\n'
        '              </div>\n'
        '              <p class="profile-setting-desc" id="profile-promo-msg" style="margin-top:6px"></p>\n'
        '            </div>\n'
        '          </div>\n'
        '\n\n          \n          \n          \n          <div class="profile-section-title" data-i18n="sync.section">Sync</div>'
    )
    sync_anchor = (
        '          </div>\n'
        '\n\n          \n          \n          \n          <div class="profile-section-title" data-i18n="sync.section">Sync</div>'
    )
    if 'profile-promo-block' not in html and sync_anchor in html:
        html = html.replace(sync_anchor, promo_block, 1)

    profile_render_tail = "    planEl.textContent = label;\n  }\n}"
    profile_render_new = (
        "    planEl.textContent = label;\n  }\n"
        "  profileRenderWordLimit();\n}"
    )
    if 'profileRenderWordLimit();' not in html and profile_render_tail in html:
        html = html.replace(profile_render_tail, profile_render_new, 1)

    auth_me_old = (
        "async function authMe() {\n"
        "  try {\n"
        "    var r = await authApi('/api/auth/me');\n"
        "    if (r.ok) { var d = await r.json(); return d.user || null; }\n"
        "  } catch (e) {}\n"
        "  return null;\n"
        "}"
    )
    auth_me_new = (
        "async function authMe() {\n"
        "  try {\n"
        "    var r = await authApi('/api/auth/me');\n"
        "    if (r.ok) {\n"
        "      var d = await r.json();\n"
        "      var u = d.user || null;\n"
        "      if (u && typeof u.wordCount !== 'number' && typeof words !== 'undefined') {\n"
        "        u.wordCount = words.length;\n"
        "      }\n"
        "      return u;\n"
        "    }\n"
        "  } catch (e) {}\n"
        "  return null;\n"
        "}"
    )
    if auth_me_old in html:
        html = html.replace(auth_me_old, auth_me_new, 1)

    i18n_ru = "'vocab.wordLimitToast': 'Лимит {limit} слов (бесплатно). Удалите лишние или оформите Premium.',"
    i18n_ru_promo = (
        "'vocab.wordLimitToast': 'Лимит {limit} слов. Удалите лишние или введите промокод.',\n"
        "      'promo.section': 'Промокод',\n"
        "      'promo.placeholder': 'FRIEND100',\n"
        "      'promo.redeem': 'Применить',\n"
        "      'promo.enterCode': 'Введите промокод',\n"
        "      'promo.applying': 'Применяем…',\n"
        "      'promo.success': 'Лимит увеличен до {limit} слов',\n"
        "      'promo.unlimited': 'Premium — без лимита слов',\n"
        "      'promo.wordUsage': 'Слов в словаре: {count} / {limit}',\n"
        "      'promo.error.generic': 'Не удалось применить промокод',\n"
        "      'promo.error.invalid_code': 'Промокод не найден',\n"
        "      'promo.error.already_redeemed': 'Вы уже использовали этот промокод',\n"
        "      'promo.error.code_exhausted': 'Промокод больше недоступен',\n"
        "      'promo.error.already_premium': 'У вас уже Premium',\n"
        "      'promo.error.missing_code': 'Введите промокод',"
    )
    if "'promo.section'" not in html and i18n_ru in html:
        html = html.replace(i18n_ru, i18n_ru_promo, 1)

    i18n_en = "'vocab.wordLimitToast': 'Limit of {limit} words (free). Remove extras or get Premium.',"
    i18n_en_promo = (
        "'vocab.wordLimitToast': 'Limit of {limit} words. Remove extras or enter a promo code.',\n"
        "      'promo.section': 'Promo code',\n"
        "      'promo.placeholder': 'FRIEND100',\n"
        "      'promo.redeem': 'Apply',\n"
        "      'promo.enterCode': 'Enter a promo code',\n"
        "      'promo.applying': 'Applying…',\n"
        "      'promo.success': 'Word limit increased to {limit}',\n"
        "      'promo.unlimited': 'Premium — unlimited words',\n"
        "      'promo.wordUsage': 'Dictionary words: {count} / {limit}',\n"
        "      'promo.error.generic': 'Could not apply promo code',\n"
        "      'promo.error.invalid_code': 'Promo code not found',\n"
        "      'promo.error.already_redeemed': 'You already used this promo code',\n"
        "      'promo.error.code_exhausted': 'This promo code is no longer available',\n"
        "      'promo.error.already_premium': 'You already have Premium',\n"
        "      'promo.error.missing_code': 'Enter a promo code',"
    )
    if i18n_en in html:
        html = html.replace(i18n_en, i18n_en_promo, 1)

    i18n_pt = "'vocab.wordLimitToast': 'Limite de {limit} palavras (grátis). Remova extras ou assine Premium.',"
    i18n_pt_promo = (
        "'vocab.wordLimitToast': 'Limite de {limit} palavras. Remova extras ou use um código promocional.',\n"
        "      'promo.section': 'Código promocional',\n"
        "      'promo.placeholder': 'FRIEND100',\n"
        "      'promo.redeem': 'Aplicar',\n"
        "      'promo.enterCode': 'Digite o código',\n"
        "      'promo.applying': 'Aplicando…',\n"
        "      'promo.success': 'Limite aumentado para {limit} palavras',\n"
        "      'promo.unlimited': 'Premium — palavras ilimitadas',\n"
        "      'promo.wordUsage': 'Palavras no dicionário: {count} / {limit}',\n"
        "      'promo.error.generic': 'Não foi possível aplicar o código',\n"
        "      'promo.error.invalid_code': 'Código não encontrado',\n"
        "      'promo.error.already_redeemed': 'Você já usou este código',\n"
        "      'promo.error.code_exhausted': 'Este código não está mais disponível',\n"
        "      'promo.error.already_premium': 'Você já tem Premium',\n"
        "      'promo.error.missing_code': 'Digite o código',"
    )
    if i18n_pt in html:
        html = html.replace(i18n_pt, i18n_pt_promo, 1)

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
