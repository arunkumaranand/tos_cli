@echo off
REM Wrapper for `tos` on CMD to make `tos cd <ENV>` change current directory.
REM Place this directory early in PATH to override any installed `tos` shim.

setlocal ENABLEDELAYEDEXPANSION
set "_MAIN=%~dp0\..\..\main.py"

if /I "%~1"=="cd" (
  if "%~2"=="" (
    echo Usage: tos cd ENV_NAME
    exit /b 1
  )
  for /f "usebackq delims=" %%P in (`python "%_MAIN%" path "%~2" 2^>nul`) do set "_TARGET=%%P"
  if not defined _TARGET (
    echo Failed to resolve path for %~2
    exit /b 1
  )
  endlocal & cd /d "%_TARGET%"
  goto :eof
)

python "%_MAIN%" %*
endlocal

