# proficonq

Portuguese learning SPA (vocabulary, reader, programs, review, dictionary, profile).

## Routes

| Path | Section |
|------|---------|
| `/` | Vocabulary (default) |
| `/vocabulary` | Vocabulary |
| `/reader` | Books reader |
| `/programs` | Study programs |
| `/review` | Review hub |
| `/review/flashcards` | Flashcards |
| `/review/tests` | Tests |
| `/progress` | Progress |
| `/dictionary` | Big dictionary |
| `/dictionary/verbs` | Verbs |
| `/grammar` | Grammar |
| `/profile` | Profile |

## Local static preview

```bash
cd E:\GIT\Proficonq
python -m http.server 3456
```

Open http://localhost:3456 — UI and routing work; `/api/*` needs the backend (see Portuprep `tutor-app`).

## Production (nginx)

Use `nginx.conf`: `try_files $uri $uri/ /index.html` and proxy `/api/` to the Node/Vite API if used.

## Deploy to server (example)

```powershell
scp -r index.html favicon.svg icons.svg verbos.js verbos-data.json vocab-images books course nginx.conf tsc-server:/var/www/proficonq/
```
