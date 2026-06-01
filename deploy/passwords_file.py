"""Read credentials from E:/GIT/passwords.txt (or PASSWORDS_FILE env)."""
from __future__ import annotations

import os
import re
from pathlib import Path

DEFAULT_PASSWORDS_FILE = Path('E:/GIT/passwords.txt')


def passwords_file_path() -> Path:
    override = os.environ.get('PASSWORDS_FILE', '').strip()
    if override:
        return Path(override)
    return DEFAULT_PASSWORDS_FILE


def read_profconq_admin_credentials() -> tuple[str, str]:
    path = passwords_file_path()
    if not path.exists():
        raise FileNotFoundError(f'Passwords file not found: {path}')

    text = path.read_text(encoding='utf-8')
    if 'profconq' not in text.lower() and 'admin panel' not in text.lower():
        raise ValueError(f'profconq admin section not found in {path}')

    login = None
    password = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        login_match = re.match(r'^Login:\s*(.+)$', line, re.IGNORECASE)
        pass_match = re.match(r'^Pass:\s*(.+)$', line, re.IGNORECASE)
        if login_match:
            login = login_match.group(1).strip()
        if pass_match:
            password = pass_match.group(1).strip()

    if not login or not password:
        raise ValueError(f'Login/Pass not found in {path}')

    return login, password
