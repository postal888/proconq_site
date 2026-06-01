# profconq.com

Portuguese learning SPA (vocabulary, reader, programs, review, dictionary, profile).

## Routes

| Path | Section |
|------|---------|
| `/` | Vocabulary (default) |
| `/vocabulary` | Vocabulary |
| `/reader` | Books reader |
| `/programs` | Study programs |
| `/review` | Review hub |
| `/progress` | Progress |
| `/dictionary` | Big dictionary |
| `/profile` | Profile |
| `/admin/` | **Admin panel** (separate login, not linked from site) |

## Admin

- URL: https://profconq.com/admin/
- Credentials: `E:\GIT\passwords.txt` (not in git)
- Sync password to server: `python deploy/sync-admin-password.py`
- Full admin deploy: `python deploy/deploy-admin-standalone.py`

## Deploy site (static)

```powershell
.\deploy.ps1
```

## Deploy API + admin (server)

```powershell
python deploy/deploy-admin-standalone.py
python deploy/sync-admin-password.py
```

## Local preview

```powershell
python -m http.server 3456
```

Open http://localhost:3456 — UI works; `/api/*` needs backend on server.

## Production nginx

See `nginx.conf` — copy to server and reload nginx after edits.
