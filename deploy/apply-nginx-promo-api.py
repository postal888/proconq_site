#!/usr/bin/env python3
"""Add nginx proxy for /api/promo/ -> proficonq-api :4100."""
from pathlib import Path

CONF = Path('/etc/nginx/sites-enabled/profconq.conf')
MARKER = 'location ^~ /api/promo/'


def main() -> None:
    text = CONF.read_text(encoding='utf-8')
    if MARKER in text:
        print('Already patched')
        return

    block = """
    location ^~ /api/promo/ {
        proxy_pass http://127.0.0.1:4100;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
"""
    anchor = '    location ^~ /api/sync {'
    if anchor not in text:
        raise SystemExit('sync location anchor not found')
    text = text.replace(anchor, block + '\n' + anchor, 1)
    CONF.write_text(text, encoding='utf-8')
    print('Patched', CONF)


if __name__ == '__main__':
    main()
