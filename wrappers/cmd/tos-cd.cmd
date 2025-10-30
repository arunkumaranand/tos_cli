@echo off
REM Change current CMD directory to the path mapped by an env name in TOS
REM Usage: tos-cd ENV_NAME

setlocal ENABLEDELAYEDEXPANSION

if "%~1"=="" (
  echo Usage: tos-cd ENV_NAME
  exit /b 1
)

set "_ENV_NAME=%~1"
set "_TARGET="

REM 1) Try local tos.exe in the same Scripts directory (pip installs)
set "_BIN_DIR=%~dp0"
if exist "%_BIN_DIR%tos.exe" (
  for /f "usebackq delims=" %%P in (`"%_BIN_DIR%tos.exe" path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
)

REM 2) Try global tos.exe on PATH
if not defined _TARGET (
  for /f "usebackq delims=" %%P in (`tos.exe path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
)

REM 3) Fallback: use PowerShell to run 'tos' (uv may install a PS shim)
if not defined _TARGET (
  for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command tos path ^"%_ENV_NAME%^" 2^>nul`) do set "_TARGET=%%P"
)

REM 4) Final fallback: import module directly
if not defined _TARGET (
  for /f "usebackq delims=" %%P in (`python -m main path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
)

if not defined _TARGET (
  echo Failed to resolve path for %_ENV_NAME%
  exit /b 1
)

endlocal & cd /d "%_TARGET%"
