#!/bin/bash
curl -s -w "\nHTTP:%{http_code}\n" -X POST "$1" \
  -H 'Content-Type: application/json' \
  -d '{"code":"FRIEND100"}'
