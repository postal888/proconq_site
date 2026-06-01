#!/usr/bin/env python3
"""Deploy admin promo panel (API + website + nginx)."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / 'proficonq-api-patch'
REMOTE = '/var/www/proficonq-api'
PATCHES = '/var/www/proficonq/tutor-app/patches'

API_FILES = [
    'src/admin.js',
    'src/promo.js',
    'src/wordLimit.js',
    'src/server.js',
    'src/routes/admin.js',
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    for rel in API_FILES:
        run(['scp', str(PATCH / rel), f'tsc-server:{REMOTE}/{rel}'])

    run(['scp', str(ROOT / 'website-admin-promo.js'), f'tsc-server:{PATCHES}/website-admin-promo.js'])
    run(['scp', str(ROOT / 'apply-website-admin-promo.py'), f'tsc-server:{PATCHES}/apply-website-admin-promo.py'])
    run(['scp', str(ROOT / 'apply-nginx-admin-api.py'), f'tsc-server:/tmp/apply-nginx-admin-api.py'])

    run([
        'ssh', 'tsc-server',
        'grep -q "^ADMIN_EMAILS=" /var/www/proficonq-api/.env || '
        'echo "ADMIN_EMAILS=postal8888888@gmail.com" >> /var/www/proficonq-api/.env; '
        'python3 /tmp/apply-nginx-admin-api.py; '
        'nginx -t && systemctl reload nginx; '
        'pm2 restart proficonq-api; '
        'python3 /var/www/proficonq/tutor-app/patches/apply-website-admin-promo.py',
    ])
    print('Admin promo panel deployed')


if __name__ == '__main__':
    main()
