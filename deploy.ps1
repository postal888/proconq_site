# Deploy profconq.com static site + admin to tsc-server
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = "tsc-server:/var/www/proficonq/tutor-app/dist/"

$files = @(
    "index.html", "favicon.svg", "icons.svg", "profconq-logo.svg",
    "verbos.js", "verbos-data.json"
)
foreach ($f in $files) {
    scp (Join-Path $Root $f) "${dest}"
}
scp -r (Join-Path $Root "admin") "${dest}"
scp -r (Join-Path $Root "vocab-images") "${dest}"
scp -r (Join-Path $Root "books") "${dest}"
scp -r (Join-Path $Root "course") "${dest}"
Write-Host "Site deployed to $dest"
Write-Host "Admin: https://profconq.com/admin/"
Write-Host "API deploy: python deploy/deploy-admin-standalone.py"
