#!/usr/bin/env python3
"""Deploy promo-code API patch to production server."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / 'proficonq-api-patch'
REMOTE = '/var/www/proficonq-api'

FILES = [
    'src/db.js',
    'src/wordLimit.js',
    'src/promo.js',
    'src/auth.js',
    'src/server.js',
    'src/routes/sync.js',
    'src/routes/promo.js',
    'scripts/seed-promo-codes.js',
]


def main() -> None:
    for rel in FILES:
        local = PATCH / rel
        if not local.exists():
            raise SystemExit(f'Missing patch file: {local}')
        remote = f'{REMOTE}/{rel}'
        subprocess.run(
            ['scp', str(local), f'tsc-server:{remote}'],
            check=True,
        )
        print('Uploaded', rel)

    subprocess.run(
        [
            'ssh', 'tsc-server',
            f'cd {REMOTE} && node scripts/seed-promo-codes.js && pm2 restart proficonq-api',
        ],
        check=True,
    )
    print('Seeded promo codes and restarted proficonq-api')


if __name__ == '__main__':
    main()
