<#
    Registers the Lookdev Tool module folder with every installed Maya
    version by adding MAYA_MODULE_PATH to that version's Maya.env.

    Maya.env is read directly by Maya at startup, so this avoids the
    unreliable delay in Windows propagating a changed user/session
    environment variable to newly launched GUI apps.
#>
param(
    [Parameter(Mandatory = $true)][string]$ModulesDir
)

$marker = "# --- Lookdev Tool module path ---"

$shellFolders = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
$documents = [Environment]::ExpandEnvironmentVariables($shellFolders.Personal)
$mayaAppDir = Join-Path $documents "maya"

if (-not (Test-Path $mayaAppDir)) {
    Write-Output "[Lookdev] No Maya app directory found at $mayaAppDir (Maya may not have run yet)."
    exit 0
}

$versions = Get-ChildItem $mayaAppDir -Directory | Where-Object { $_.Name -match '^\d{4}$' }

if (-not $versions) {
    Write-Output "[Lookdev] No versioned Maya folders found under $mayaAppDir."
    exit 0
}

foreach ($version in $versions) {
    $envFile = Join-Path $version.FullName "Maya.env"
    $content = ""
    if (Test-Path $envFile) {
        $content = [string](Get-Content $envFile -Raw)
    }
    if ($content -notmatch [regex]::Escape($marker)) {
        $block = "`r`n$marker`r`nMAYA_MODULE_PATH = $ModulesDir;%MAYA_MODULE_PATH%`r`n$marker`r`n"
        Add-Content -Path $envFile -Value $block
        Write-Output "[Lookdev] Registered module path in $envFile"
    }
    else {
        Write-Output "[Lookdev] Already registered in $envFile"
    }
}
