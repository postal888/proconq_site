#!/usr/bin/env python3
"""Deploy standalone /admin panel with separate login."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / 'proficonq-api-patch'
REMOTE = '/var/www/proficonq-api'
ADMIN_DIR = '/var/www/proficonq/tutor-app/dist/admin'

API_FILES = [
    'src/admin.js',
    'src/db.js',
    'src/wordLimit.js',
    'src/routes/admin.js',
    'scripts/set-admin-password.js',
]


def run(cmd):
    subprocess.run(cmd, check=True)


def main() -> None:
    run(['ssh', 'tsc-server', f'mkdir -p {ADMIN_DIR}'])

    for rel in API_FILES:
        run(['scp', str(PATCH / rel), f'tsc-server:{REMOTE}/{rel}'])

    run(['scp', str(ROOT / 'admin/index.html'), f'tsc-server:{ADMIN_DIR}/index.html'])
    for script_name in [
        'apply-website-remove-admin-from-main.py',
        'apply-nginx-admin-page.py',
    ]:
        run(['scp', str(ROOT / script_name), f'tsc-server:/tmp/{script_name}'])

#!/usr/bin/env python3
"""Deploy standalone /admin panel with separate login."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / 'proficonq-api-patch'
REMOTE = '/var/www/proficonq-api'
ADMIN_DIR = '/var/www/proficonq/tutor-app/dist/admin'

API_FILES = [
    'src/admin.js',
    'src/db.js',
    'src/wordLimit.js',
    'src/routes/admin.js',
    'scripts/set-admin-password.js',
]


def run(cmd):
    subprocess.run(cmd, check=True)


def main() -> None:
    run(['ssh', 'tsc-server', f'mkdir -p {ADMIN_DIR}'])

    for rel in API_FILES:
        run(['scp', str(PATCH / rel), f'tsc-server:{REMOTE}/{rel}'])

    run(['scp', str(ROOT / 'admin/index.html'), f'tsc-server:{ADMIN_DIR}/index.html'])
    for script_name in [
        'apply-website-remove-admin-from-main.py',
        'apply-nginx-admin-page.py',
    ]:
        run(['scp', str(ROOT / script_name), f'tsc-server:/tmp/{script_name}'])

    run([
        'ssh', 'tsc-server',
        'bash -lc \''
        'python3 /tmp/apply-nginx-admin-page.py && '
        'nginx -t && systemctl reload nginx && '
        'pm2 restart proficonq-api && '
        'python3 /tmp/apply-website-remove-admin-from-main.py'
        '\'',
    ])

    sync = ROOT / 'sync-admin-password.py'
    subprocess.run([sys.executable, str(sync)], check=True)

    print('Standalone admin deployed at https://profconq.com/admin/')


if __name__ == '__main__':
    main()
