#!/usr/bin/env python3
"""Show clear message when registering with an already-used email."""
from __future__ import annotations

from pathlib import Path

INDEX = Path('/var/www/proficonq/tutor-app/dist/index.html')

OLD_REGISTER = """async function authSubmitRegister(ev) {
  ev.preventDefault();
  var email = document.getElementById('auth-reg-email').value.trim();
  var password = document.getElementById('auth-reg-password').value;
  if (password.length < 8) { authSetMsg(t('auth.msgWeakPassword'), 'error'); return false; }
  try {
    var r = await authApi('/api/auth/register', { method: 'POST', body: JSON.stringify({ email: email, password: password }) });
    if (r.ok) { authShow('pending'); authSetMsg(t('auth.msgRegistered'), 'ok'); window.__authPendingEmail = email; }
    else authSetMsg(t('auth.msgError'), 'error');
  } catch (e) { authSetMsg(t('auth.msgError'), 'error'); }
  return false;
}"""

NEW_REGISTER = """async function authSubmitRegister(ev) {
  ev.preventDefault();
  var email = document.getElementById('auth-reg-email').value.trim();
  var password = document.getElementById('auth-reg-password').value;
  if (password.length < 8) { authSetMsg(t('auth.msgWeakPassword'), 'error'); return false; }
  try {
    var r = await authApi('/api/auth/register', { method: 'POST', body: JSON.stringify({ email: email, password: password }) });
    if (r.ok) { authShow('pending'); authSetMsg(t('auth.msgRegistered'), 'ok'); window.__authPendingEmail = email; return false; }
    var err = await r.json().catch(function () { return {}; });
    if (err.error === 'email_already_registered') authSetMsg(t('auth.msgEmailAlreadyRegistered'), 'error');
    else if (err.error === 'email_pending_verification') authSetMsg(t('auth.msgEmailPendingVerification'), 'error');
    else if (err.error === 'weak_password') authSetMsg(t('auth.msgWeakPassword'), 'error');
    else if (err.error === 'invalid_email') authSetMsg(t('auth.msgInvalidEmail'), 'error');
    else authSetMsg(t('auth.msgError'), 'error');
  } catch (e) { authSetMsg(t('auth.msgError'), 'error'); }
  return false;
}"""

I18N_INSERT = """    'auth.msgEmailAlreadyRegistered': 'Этот email уже зарегистрирован. Войдите в аккаунт.',
    'auth.msgEmailPendingVerification': 'Этот email уже зарегистрирован. Подтвердите почту — мы отправили письмо повторно.',
    'auth.msgInvalidEmail': 'Некорректный email.',
"""

I18N_INSERT_EN = """    'auth.msgEmailAlreadyRegistered': 'This email is already registered. Sign in to your account.',
    'auth.msgEmailPendingVerification': 'This email is already registered. Check your inbox — we sent the verification email again.',
    'auth.msgInvalidEmail': 'Invalid email address.',
"""

I18N_INSERT_PT = """    'auth.msgEmailAlreadyRegistered': 'Este email já está registado. Entre na sua conta.',
    'auth.msgEmailPendingVerification': 'Este email já está registado. Verifique a caixa de entrada — reenviámos o email de confirmação.',
    'auth.msgInvalidEmail': 'Email inválido.',
"""


def main() -> None:
    html = INDEX.read_text(encoding='utf-8')
    if OLD_REGISTER in html:
        html = html.replace(OLD_REGISTER, NEW_REGISTER, 1)
        print('Patched authSubmitRegister')
    elif 'auth.msgEmailAlreadyRegistered' in html:
        print('authSubmitRegister already patched')
    else:
        raise SystemExit('authSubmitRegister block not found')

    if "'auth.msgEmailAlreadyRegistered':" not in html:
        html = html.replace(
            "'auth.msgResetDone': 'Пароль изменён. Войдите с новым паролем.', 'auth.msgError': 'Что-то пошло не так. Попробуйте ещё раз.', 'auth.msgWeakPassword': 'Пароль слишком короткий (мин. 8 символов).',",
            "'auth.msgResetDone': 'Пароль изменён. Войдите с новым паролем.', 'auth.msgError': 'Что-то пошло не так. Попробуйте ещё раз.', 'auth.msgWeakPassword': 'Пароль слишком короткий (мин. 8 символов).',\n" + I18N_INSERT.strip(),
            1,
        )
        html = html.replace(
            "'auth.msgResetDone': 'Password changed. Sign in with your new password.', 'auth.msgError': 'Something went wrong. Please try again.', 'auth.msgWeakPassword': 'Password too short (min 8 characters).',",
            "'auth.msgResetDone': 'Password changed. Sign in with your new password.', 'auth.msgError': 'Something went wrong. Please try again.', 'auth.msgWeakPassword': 'Password too short (min 8 characters).',\n" + I18N_INSERT_EN.strip(),
            1,
        )
        html = html.replace(
            "'auth.msgResetDone': 'Palavra-passe alterada. Inicie sessão com a nova.', 'auth.msgError': 'Algo correu mal. Tente novamente.', 'auth.msgWeakPassword': 'Palavra-passe demasiado curta (mín. 8 caracteres).',",
            "'auth.msgResetDone': 'Palavra-passe alterada. Inicie sessão com a nova.', 'auth.msgError': 'Algo correu mal. Tente novamente.', 'auth.msgWeakPassword': 'Palavra-passe demasiado curta (mín. 8 caracteres).',\n" + I18N_INSERT_PT.strip(),
            1,
        )
        print('Added i18n strings')

    INDEX.write_text(html, encoding='utf-8')
    print('Patched', INDEX)


if __name__ == '__main__':
    main()
