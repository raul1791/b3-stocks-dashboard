$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Set-Location "c:\Users\TWF\Downloads\testeClaude"
$changed = git status --porcelain
if ($changed) {
    git add -A
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "Auto-update: $timestamp"
    git push origin master
}
