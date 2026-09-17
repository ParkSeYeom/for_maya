@echo off
setlocal enabledelayedexpansion

set "SRC=%~dp0LookdevTool"
set "MODULES_DIR=%LOCALAPPDATA%\MayaModules"
set "DEST=%MODULES_DIR%\LookdevTool"
set "PS1=%~dp0register_module_path.ps1"

if not exist "%SRC%" (
    echo [Lookdev] LookdevTool folder not found next to install.bat.
    pause
    exit /b 1
)

if not exist "%MODULES_DIR%" mkdir "%MODULES_DIR%"

if exist "%DEST%" rmdir /s /q "%DEST%"
xcopy "%SRC%" "%DEST%\" /e /i /y >nul

> "%MODULES_DIR%\LookdevTool.mod" (
    echo + LookdevTool 1.0 LookdevTool
    echo scripts: scripts
    echo plug-ins: plug-ins
)

echo [Lookdev] Registering module path with installed Maya versions...
if exist "%PS1%" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" -ModulesDir "%MODULES_DIR%"
) else (
    echo [Lookdev] register_module_path.ps1 not found next to install.bat - skipped.
)

echo.
echo [Lookdev] Install complete. Restart Maya to see the Lookdev menu.
echo [Lookdev] Installed to: %DEST%
pause
