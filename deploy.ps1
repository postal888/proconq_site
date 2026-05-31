# Deploy proficonq static site to tsc-server
$dest = "tsc-server:/var/www/proficonq/"
$files = @(
    "index.html", "favicon.svg", "icons.svg",
    "verbos.js", "verbos-data.json", "nginx.conf"
)
foreach ($f in $files) {
    scp "E:\GIT\Proficonq\$f" "${dest}"
}
scp -r "E:\GIT\Proficonq\vocab-images" "${dest}"
scp -r "E:\GIT\Proficonq\books" "${dest}"
scp -r "E:\GIT\Proficonq\course" "${dest}"
Write-Host "Deployed to $dest"
