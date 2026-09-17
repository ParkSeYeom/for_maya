<#
    Removes the Lookdev Tool MAYA_MODULE_PATH block that
    register_module_path.ps1 added to each installed Maya version's
    Maya.env, restoring it to its pre-install content.
#>

$marker = "# --- Lookdev Tool module path ---"

$shellFolders = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
$documents = [Environment]::ExpandEnvironmentVariables($shellFolders.Personal)
$mayaAppDir = Join-Path $documents "maya"

if (-not (Test-Path $mayaAppDir)) {
    Write-Output "[Lookdev] No Maya app directory found at $mayaAppDir."
    exit 0
}

$versions = Get-ChildItem $mayaAppDir -Directory | Where-Object { $_.Name -match '^\d{4}$' }

if (-not $versions) {
    Write-Output "[Lookdev] No versioned Maya folders found under $mayaAppDir."
    exit 0
}

foreach ($version in $versions) {
    $envFile = Join-Path $version.FullName "Maya.env"
    if (-not (Test-Path $envFile)) {
        continue
    }

    $content = [string](Get-Content $envFile -Raw)
    if ($content -notmatch [regex]::Escape($marker)) {
        Write-Output "[Lookdev] Nothing to remove in $envFile"
        continue
    }

    $pattern = "(\r?\n)*" + [regex]::Escape($marker) + "(?s).*?" + [regex]::Escape($marker) + "(\r?\n)*"
    $newContent = [regex]::Replace($content, $pattern, "")

    Set-Content -Path $envFile -Value $newContent -NoNewline
    Write-Output "[Lookdev] Removed module path block from $envFile"
}
