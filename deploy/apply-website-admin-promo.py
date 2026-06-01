#!/usr/bin/env python3
"""Patch live website: admin promo panel."""
from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')
PATCH_DIR = Path('/var/www/proficonq/tutor-app/patches')
ADMIN_JS = PATCH_DIR / 'website-admin-promo.js'


def inject_js(html: str) -> str:
    if 'function initAdminView()' in html:
        return html
    js = ADMIN_JS.read_text(encoding='utf-8')
    anchor = 'function initProfileView() {'
    if anchor not in html:
        raise SystemExit('initProfileView anchor not found')
    return html.replace(anchor, js + '\n' + anchor, 1)


def inject_css(html: str) -> str:
    if '.admin-promo-table' in html:
        return html
    css = """
.admin-page{max-width:min(920px,100%);display:flex;flex-direction:column;gap:var(--space-3);padding-bottom:var(--space-6)}
.admin-promo-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:var(--space-3);margin-top:var(--space-2)}
.admin-promo-form .input,.admin-promo-form .btn{width:100%}
.admin-promo-table{width:100%;border-collapse:collapse;font-size:var(--text-sm)}
.admin-promo-table th,.admin-promo-table td{padding:10px 8px;border-bottom:1px solid var(--color-border);text-align:left;vertical-align:top}
.admin-promo-table th{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--color-text-faint)}
.admin-promo-label{font-size:11px;color:var(--color-text-muted);margin-top:4px}
.admin-empty{color:var(--color-text-muted);text-align:center}
.admin-promo-msg.is-ok{color:var(--color-primary)}
.admin-promo-msg.is-error{color:var(--color-danger,#e5484d)}
"""
    return html.replace('</style>', css + '\n</style>', 1)


def inject_nav(html: str) -> str:
    if 'id="nav-admin"' in html:
        return html
    anchor = (
        '        <button class="nav-item nav-item-main" data-view="profile" onclick="navigate(\'profile\',this)">\n'
        '          <i data-lucide="user"></i> <span data-i18n="nav.profile">Profile</span>\n'
        '        </button>'
    )
    block = (
        '        <button class="nav-item nav-item-main" data-view="profile" onclick="navigate(\'profile\',this)">\n'
        '          <i data-lucide="user"></i> <span data-i18n="nav.profile">Profile</span>\n'
        '        </button>\n'
        '        <button class="nav-item nav-item-main" data-view="admin" id="nav-admin" onclick="navigate(\'admin\',this)" hidden>\n'
        '          <i data-lucide="shield"></i> <span data-i18n="nav.admin">Admin</span>\n'
        '        </button>'
    )
    if anchor in html:
        html = html.replace(anchor, block, 1)
    return html


def inject_view(html: str) -> str:
    if 'id="view-admin"' in html:
        return html
    anchor = '      <div class="view" id="view-profile">'
    block = (
        '      <div class="view" id="view-admin">\n'
        '        <div class="admin-page">\n'
        '          <div class="profile-brand">\n'
        '            <div class="profile-brand-title"><span class="profile-brand-p">A</span>dmin</div>\n'
        '            <div class="profile-brand-tagline" data-i18n="admin.subtitle">Promo codes</div>\n'
        '          </div>\n'
        '          <div class="profile-section-title" data-i18n="admin.promo.createSection">Create promo code</div>\n'
        '          <div class="profile-card">\n'
        '            <form class="admin-promo-form" onsubmit="return adminCreatePromoCode(event)">\n'
        '              <label class="profile-setting-block">\n'
        '                <div class="profile-setting-label" data-i18n="admin.promo.generate">Generate random code</div>\n'
        '                <label class="profile-switch"><input type="checkbox" id="admin-promo-generate" checked onchange="adminSyncGenerateUi()"><span class="profile-switch-slider"></span></label>\n'
        '              </label>\n'
        '              <label class="profile-setting-block" id="admin-promo-prefix-wrap">\n'
        '                <div class="profile-setting-label" data-i18n="admin.promo.prefix">Prefix</div>\n'
        '                <input class="input" id="admin-promo-prefix" value="PQ" maxlength="8">\n'
        '              </label>\n'
        '              <label class="profile-setting-block" id="admin-promo-code-wrap" style="display:none">\n'
        '                <div class="profile-setting-label" data-i18n="admin.promo.code">Code</div>\n'
        '                <input class="input" id="admin-promo-code" placeholder="MYFRIEND2026" maxlength="32">\n'
        '              </label>\n'
        '              <label class="profile-setting-block">\n'
        '                <div class="profile-setting-label" data-i18n="admin.promo.wordLimit">Word limit</div>\n'
        '                <input class="input" id="admin-promo-limit" type="number" min="1" value="100" required>\n'
        '              </label>\n'
        '              <label class="profile-setting-block">\n'
        '                <div class="profile-setting-label" data-i18n="admin.promo.maxRedemptions">Max uses (optional)</div>\n'
        '                <input class="input" id="admin-promo-max" type="number" min="1" placeholder="∞">\n'
        '              </label>\n'
        '              <label class="profile-setting-block" style="grid-column:1/-1">\n'
        '                <div class="profile-setting-label" data-i18n="admin.promo.label">Note (optional)</div>\n'
        '                <input class="input" id="admin-promo-label" placeholder="For Anna">\n'
        '              </label>\n'
        '              <div style="grid-column:1/-1;display:flex;gap:8px;align-items:center;flex-wrap:wrap">\n'
        '                <button type="submit" class="btn btn-primary btn-sm"><i data-lucide="plus"></i> <span data-i18n="admin.promo.createBtn">Create</span></button>\n'
        '                <button type="button" class="btn btn-ghost btn-sm" onclick="adminLoadPromoCodes()"><i data-lucide="refresh-cw"></i> <span data-i18n="admin.promo.refresh">Refresh</span></button>\n'
        '              </div>\n'
        '            </form>\n'
        '            <p class="profile-setting-desc admin-promo-msg" id="admin-promo-msg"></p>\n'
        '          </div>\n'
        '          <div class="profile-section-title" data-i18n="admin.promo.listSection">All promo codes</div>\n'
        '          <div class="profile-card" style="overflow:auto">\n'
        '            <table class="admin-promo-table">\n'
        '              <thead><tr>\n'
        '                <th data-i18n="admin.promo.colCode">Code</th>\n'
        '                <th data-i18n="admin.promo.colLimit">Limit</th>\n'
        '                <th data-i18n="admin.promo.colMax">Max</th>\n'
        '                <th data-i18n="admin.promo.colUsed">Used</th>\n'
        '                <th data-i18n="admin.promo.colStatus">Status</th>\n'
        '                <th></th>\n'
        '              </tr></thead>\n'
        '              <tbody id="admin-promo-table-body"><tr><td colspan="6" class="admin-empty">…</td></tr></tbody>\n'
        '            </table>\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>\n\n'
        '      <div class="view" id="view-profile">'
    )
    return html.replace(anchor, block, 1)


def inject_routes(html: str) -> str:
    route_anchor = "  '/profile/settings':   'profile',"
    route_block = (
        "  '/profile/settings':   'profile',\n"
        "  '/admin':              'admin',"
    )
    if "'/admin'" not in html and route_anchor in html:
        html = html.replace(route_anchor, route_block, 1)

    view_anchor = "  'profile':        '/profile',"
    view_block = (
        "  'profile':        '/profile',\n"
        "  'admin':          '/admin',"
    )
    if "'admin':" not in html and view_anchor in html:
        html = html.replace(view_anchor, view_block, 1)
    return html


def inject_hooks(html: str) -> str:
    start_anchor = '  applyUiLanguage();\n}'
    start_block = (
        '  applyUiLanguage();\n'
        '  initAdminView();\n'
        '}'
    )
    if 'initAdminView();' not in html and start_anchor in html:
        html = html.replace(start_anchor, start_block, 1)

    login_anchor = '      window.__authUser = d.user;\n      hideAuthScreen();\n      await startAppAfterAuth();'
    login_block = (
        '      window.__authUser = d.user;\n'
        '      adminUpdateNavVisibility();\n'
        '      hideAuthScreen();\n'
        '      await startAppAfterAuth();'
    )
    if login_anchor in html:
        html = html.replace(login_anchor, login_block, 1)

    nav_anchor = 'function navigate(viewId, el, fromRouter) {'
    nav_block = (
        'function navigate(viewId, el, fromRouter) {\n'
        '  if (viewId === "admin" && !adminIsUser()) { showToast(t("admin.forbidden")); return; }'
    )
    if 'viewId === "admin"' not in html and nav_anchor in html:
        html = html.replace(nav_anchor, nav_block, 1)

    admin_nav_load = "  if (viewId === 'admin') { initAdminView(); try { lucide.createIcons(); } catch (e) {} }"
    nav_end = '  syncMobileNavToggleUi();'
    if admin_nav_load not in html and nav_end in html:
        html = html.replace(nav_end, admin_nav_load + '\n  ' + nav_end, 1)

    return html


def inject_i18n(html: str) -> str:
    if "'admin.subtitle'" in html:
        return html
    ru_anchor = "      'promo.error.missing_code': 'Введите промокод',"
    ru_block = ru_anchor + """
      'nav.admin': 'Админ',
      'admin.subtitle': 'Промокоды',
      'admin.forbidden': 'Нет доступа',
      'admin.promo.createSection': 'Создать промокод',
      'admin.promo.listSection': 'Все промокоды',
      'admin.promo.generate': 'Сгенерировать случайный код',
      'admin.promo.prefix': 'Префикс',
      'admin.promo.code': 'Код',
      'admin.promo.wordLimit': 'Лимит слов',
      'admin.promo.maxRedemptions': 'Макс. активаций (необяз.)',
      'admin.promo.label': 'Заметка (необяз.)',
      'admin.promo.createBtn': 'Создать',
      'admin.promo.refresh': 'Обновить',
      'admin.promo.empty': 'Промокодов пока нет',
      'admin.promo.loading': 'Загрузка…',
      'admin.promo.creating': 'Создаём…',
      'admin.promo.created': 'Создан код {code}',
      'admin.promo.createError': 'Не удалось создать промокод',
      'admin.promo.loadError': 'Не удалось загрузить список',
      'admin.promo.toggleError': 'Не удалось изменить статус',
      'admin.promo.invalidLimit': 'Укажите лимит слов',
      'admin.promo.enterCode': 'Введите код или включите генерацию',
      'admin.promo.active': 'Активен',
      'admin.promo.inactive': 'Выключен',
      'admin.promo.activate': 'Включить',
      'admin.promo.deactivate': 'Выключить',
      'admin.promo.colCode': 'Код',
      'admin.promo.colLimit': 'Лимит',
      'admin.promo.colMax': 'Макс.',
      'admin.promo.colUsed': 'Исп.',
      'admin.promo.colStatus': 'Статус',"""
    if ru_anchor in html:
        html = html.replace(ru_anchor, ru_block, 1)

    en_anchor = "      'promo.error.missing_code': 'Enter a promo code',"
    en_block = en_anchor + """
      'nav.admin': 'Admin',
      'admin.subtitle': 'Promo codes',
      'admin.forbidden': 'Access denied',
      'admin.promo.createSection': 'Create promo code',
      'admin.promo.listSection': 'All promo codes',
      'admin.promo.generate': 'Generate random code',
      'admin.promo.prefix': 'Prefix',
      'admin.promo.code': 'Code',
      'admin.promo.wordLimit': 'Word limit',
      'admin.promo.maxRedemptions': 'Max uses (optional)',
      'admin.promo.label': 'Note (optional)',
      'admin.promo.createBtn': 'Create',
      'admin.promo.refresh': 'Refresh',
      'admin.promo.empty': 'No promo codes yet',
      'admin.promo.loading': 'Loading…',
      'admin.promo.creating': 'Creating…',
      'admin.promo.created': 'Created code {code}',
      'admin.promo.createError': 'Could not create promo code',
      'admin.promo.loadError': 'Could not load promo codes',
      'admin.promo.toggleError': 'Could not update status',
      'admin.promo.invalidLimit': 'Enter a word limit',
      'admin.promo.enterCode': 'Enter a code or enable generation',
      'admin.promo.active': 'Active',
      'admin.promo.inactive': 'Inactive',
      'admin.promo.activate': 'Activate',
      'admin.promo.deactivate': 'Deactivate',
      'admin.promo.colCode': 'Code',
      'admin.promo.colLimit': 'Limit',
      'admin.promo.colMax': 'Max',
      'admin.promo.colUsed': 'Used',
      'admin.promo.colStatus': 'Status',"""
    if en_anchor in html:
        html = html.replace(en_anchor, en_block, 1)

    pt_anchor = "      'promo.error.missing_code': 'Digite o código',"
    pt_block = pt_anchor + """
      'nav.admin': 'Admin',
      'admin.subtitle': 'Códigos promocionais',
      'admin.forbidden': 'Acesso negado',
      'admin.promo.createSection': 'Criar código',
      'admin.promo.listSection': 'Todos os códigos',
      'admin.promo.generate': 'Gerar código aleatório',
      'admin.promo.prefix': 'Prefixo',
      'admin.promo.code': 'Código',
      'admin.promo.wordLimit': 'Limite de palavras',
      'admin.promo.maxRedemptions': 'Máx. usos (opcional)',
      'admin.promo.label': 'Nota (opcional)',
      'admin.promo.createBtn': 'Criar',
      'admin.promo.refresh': 'Atualizar',
      'admin.promo.empty': 'Nenhum código ainda',
      'admin.promo.loading': 'Carregando…',
      'admin.promo.creating': 'Criando…',
      'admin.promo.created': 'Código criado: {code}',
      'admin.promo.createError': 'Não foi possível criar o código',
      'admin.promo.loadError': 'Não foi possível carregar a lista',
      'admin.promo.toggleError': 'Não foi possível alterar o status',
      'admin.promo.invalidLimit': 'Informe o limite de palavras',
      'admin.promo.enterCode': 'Digite o código ou ative a geração',
      'admin.promo.active': 'Ativo',
      'admin.promo.inactive': 'Inativo',
      'admin.promo.activate': 'Ativar',
      'admin.promo.deactivate': 'Desativar',
      'admin.promo.colCode': 'Código',
      'admin.promo.colLimit': 'Limite',
      'admin.promo.colMax': 'Máx.',
      'admin.promo.colUsed': 'Usos',
      'admin.promo.colStatus': 'Status',"""
    if pt_anchor in html:
        html = html.replace(pt_anchor, pt_block, 1)
    return html


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    html = inject_css(html)
    html = inject_nav(html)
    html = inject_view(html)
    html = inject_routes(html)
    html = inject_js(html)
    html = inject_hooks(html)
    html = inject_i18n(html)
    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
