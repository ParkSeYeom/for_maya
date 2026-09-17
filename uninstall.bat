@echo off
setlocal enabledelayedexpansion

set "MODULES_DIR=%LOCALAPPDATA%\MayaModules"
set "PS1=%~dp0unregister_module_path.ps1"

echo [Lookdev] Removing installed files...
if exist "%MODULES_DIR%\LookdevTool" rmdir /s /q "%MODULES_DIR%\LookdevTool"
if exist "%MODULES_DIR%\LookdevTool.mod" del /f /q "%MODULES_DIR%\LookdevTool.mod"

rem Remove the MayaModules folder itself only if it is now empty.
if exist "%MODULES_DIR%" (
    dir /b "%MODULES_DIR%" 2>nul | findstr "^" >nul
    if errorlevel 1 rmdir "%MODULES_DIR%"
)

echo [Lookdev] Removing Maya.env registration...
if exist "%PS1%" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
) else (
    echo [Lookdev] unregister_module_path.ps1 not found next to uninstall.bat - skipped.
)

echo.
echo [Lookdev] Uninstall complete.
echo [Lookdev] If Maya is currently open, close it - the Lookdev menu
echo [Lookdev] will not come back on the next launch.
pause
