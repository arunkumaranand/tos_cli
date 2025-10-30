@echo off
REM Change current CMD directory using short alias: td ENV_NAME

setlocal ENABLEDELAYEDEXPANSION

if "%~1"=="" (
  echo Usage: td ENV_NAME
  exit /b 1
)

set "_ENV_NAME=%~1"
set "_TARGET="

REM 1) Try local t.exe in the same Scripts directory (pip installs)
set "_BIN_DIR=%~dp0"
if exist "%_BIN_DIR%t.exe" (
  for /f "usebackq delims=" %%P in (`"%_BIN_DIR%t.exe" path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
)

REM 2) Try global t.exe on PATH
if not defined _TARGET (
  for /f "usebackq delims=" %%P in (`t.exe path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
)

REM 3) Fallback to legacy name
if not defined _TARGET (
  if exist "%_BIN_DIR%tos.exe" (
    for /f "usebackq delims=" %%P in (`"%_BIN_DIR%tos.exe" path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
  ) else (
    for /f "usebackq delims=" %%P in (`tos.exe path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
  )
)

REM 4) PowerShell shim
if not defined _TARGET (
  for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command t path ^"%_ENV_NAME%^" 2^>nul`) do set "_TARGET=%%P"
)

REM 5) Python module fallback
if not defined _TARGET (
  for /f "usebackq delims=" %%P in (`python -m main path "%_ENV_NAME%" 2^>nul`) do set "_TARGET=%%P"
)

if not defined _TARGET (
  echo Failed to resolve path for %_ENV_NAME%
  exit /b 1
)

endlocal & cd /d "%_TARGET%"

