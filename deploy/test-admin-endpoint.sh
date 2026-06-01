#!/bin/bash
# Quick smoke test for admin API (requires valid session cookie in PQ_SESSION env)
BASE="${1:-https://profconq.com}"
echo "GET $BASE/api/admin/me"
curl -s -w "\nHTTP:%{http_code}\n" "$BASE/api/admin/me" -H "Cookie: pq_session=${PQ_SESSION:-}"
