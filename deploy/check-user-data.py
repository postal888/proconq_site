#!/usr/bin/env python3
import json
import sqlite3

DB = '/var/www/proficonq-api/data/app.db'
c = sqlite3.connect(DB)

print('=== users ===')
print('count:', c.execute('SELECT COUNT(*) FROM users').fetchone()[0])

print('\n=== user_data by key ===')
for row in c.execute('SELECT key, COUNT(*), SUM(length(json)) FROM user_data GROUP BY key ORDER BY key'):
    print(f'  {row[0]}: {row[1]} user(s), {row[2] or 0} bytes total')

print('\n=== recent updates ===')
for row in c.execute(
    'SELECT u.email, d.key, length(d.json), d.version, d.updated_at '
    'FROM user_data d JOIN users u ON u.id = d.user_id '
    'ORDER BY d.updated_at DESC LIMIT 12'
):
    email, key, size, ver, ts = row
    print(f'  {email[:30]:30} | {key:18} | {size:6} bytes | v{ver}')

print('\n=== vocabulary sample (first user with words) ===')
row = c.execute(
    "SELECT u.email, d.json FROM user_data d JOIN users u ON u.id = d.user_id "
    "WHERE d.key = 'vocabulary' ORDER BY length(d.json) DESC LIMIT 1"
).fetchone()
if row:
    email, js = row
    data = json.loads(js)
    words = data.get('words') or []
    print(f'  user: {email}, words: {len(words)}')
    if words:
        w = words[0]
        print(f'  first word: {w.get("word")!r} -> {w.get("translation")!r}')
else:
    print('  (no vocabulary rows)')

print('\n=== programs sample ===')
row = c.execute(
    "SELECT u.email, length(d.json) FROM user_data d JOIN users u ON u.id = d.user_id "
    "WHERE d.key = 'programs' LIMIT 3"
).fetchall()
for r in row:
    print(f'  {r[0]}: {r[1]} bytes')

print('\n=== program_progress sample ===')
row = c.execute(
    "SELECT u.email, length(d.json) FROM user_data d JOIN users u ON u.id = d.user_id "
    "WHERE d.key = 'program_progress' LIMIT 3"
).fetchall()
for r in row:
    print(f'  {r[0]}: {r[1]} bytes')

print('\n=== activity sample ===')
row = c.execute(
    "SELECT u.email, length(d.json) FROM user_data d JOIN users u ON u.id = d.user_id "
    "WHERE d.key = 'activity' LIMIT 3"
).fetchall()
for r in row:
    print(f'  {r[0]}: {r[1]} bytes')

print('\n=== programs JSON ===')
row = c.execute("SELECT json FROM user_data WHERE key='programs' LIMIT 1").fetchone()
if row:
    p = json.loads(row[0])
    print(json.dumps(p, ensure_ascii=False, indent=2)[:600])

print('\n=== program_progress JSON ===')
row = c.execute("SELECT json FROM user_data WHERE key='program_progress' LIMIT 1").fetchone()
if row:
    print(row[0])
