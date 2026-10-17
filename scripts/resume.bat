@echo off
REM ============================================================
REM  scripts\resume.bat — Resume Azr.AI work session
REM
REM  Run this FIRST at the start of every new CMD window
REM  before running any phase command.
REM
REM  What it does:
REM    1. Activates the azrai conda environment
REM    2. Navigates to the project root
REM    3. Prints environment info for confirmation
REM ============================================================

echo.
echo === Resuming Azr.AI work session ===
echo.

REM --- 1. Activate conda environment ---
call conda activate azrai
if errorlevel 1 (
    echo [ERROR] Failed to activate conda env 'azrai'
    echo Check that conda is installed and 'azrai' env exists.
    pause
    exit /b 1
)

REM --- 2. Navigate to project root ---
cd /d "C:\Users\mazra\Downloads\coral-reef-kuantan"

REM Add src to PYTHONPATH so scripts can find the azrai library
if not defined PYTHONPATH set PYTHONPATH=%CD%\src

REM --- 3. Confirm ready state ---
echo === Session ready ===
echo   Environment: %CONDA_DEFAULT_ENV%
echo   Project:     %CD%
echo.
echo   Next: run any phase command, e.g.
echo     scripts\run_phase_d_flowB.bat
echo.