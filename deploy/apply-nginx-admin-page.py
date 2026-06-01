#!/usr/bin/env python3
"""Serve standalone admin page at /admin/."""
from pathlib import Path

CONF = Path('/etc/nginx/sites-enabled/profconq.conf')
MARKER = 'location = /admin {'


def main() -> None:
    text = CONF.read_text(encoding='utf-8')
    if MARKER in text:
        print('Already patched')
        return

    block = """
    location = /admin {
        return 301 /admin/;
    }

    location ^~ /admin/ {
        alias /var/www/proficonq/tutor-app/dist/admin/;
        index index.html;
    }
"""
    anchor = '    location / {'
    if anchor not in text:
        raise SystemExit('location / anchor not found')
    text = text.replace(anchor, block + '\n' + anchor, 1)
    CONF.write_text(text, encoding='utf-8')
    print('Patched', CONF)


if __name__ == '__main__':
    main()
