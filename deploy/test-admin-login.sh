#!/bin/bash
set -euo pipefail
COOKIE=/tmp/pq-admin-cookie.txt
rm -f "$COOKIE"
curl -s -c "$COOKIE" -X POST http://127.0.0.1:4100/api/admin/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"'"${ADMIN_PASS}"'"}'
echo
curl -s -b "$COOKIE" http://127.0.0.1:4100/api/admin/me
echo
curl -s -o /dev/null -w 'ADMIN_PAGE:%{http_code}\n' https://profconq.com/admin/
curl -s https://profconq.com/ | grep -c view-admin || true
