#!/usr/bin/env python3
"""Sync profconq admin login/password from E:/GIT/passwords.txt to production."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from passwords_file import read_profconq_admin_credentials

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / 'proficonq-api-patch'
REMOTE = '/var/www/proficonq-api'
REMOTE_PW = '/tmp/profconq-admin-password.txt'


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    username, password = read_profconq_admin_credentials()

    with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False, suffix='.txt') as tmp:
        tmp.write(password)
        local_pw = Path(tmp.name)

    try:
        run(['scp', str(PATCH / 'scripts/set-admin-password.js'), f'tsc-server:{REMOTE}/scripts/'])
        run(['scp', str(local_pw), f'tsc-server:{REMOTE_PW}'])
        run([
            'ssh', 'tsc-server',
            f'cd {REMOTE} && '
            f'node scripts/set-admin-password.js --file={REMOTE_PW} {username} && '
            f'rm -f {REMOTE_PW} && '
            'pm2 restart proficonq-api',
        ])
    finally:
        local_pw.unlink(missing_ok=True)

    print(f'Admin password synced for user: {username}')


if __name__ == '__main__':
    main()
