@echo off

REM 1. Activate env and navigate (resume.bat)
call "%~dp0resume.bat"

REM 2. Force working directory and PYTHONPATH (absolute, not relative)
cd /d "C:\Users\mazra\Downloads\coral-reef-kuantan"
set PYTHONPATH=C:\Users\mazra\Downloads\coral-reef-kuantan\src;%PYTHONPATH%

echo.
echo === Phase D Flow B — full pipeline ===
echo   CD: %CD%
echo   PYTHONPATH: %PYTHONPATH%
echo.

python scripts\phase_d\run_phase_d_1_load_detections.py
if errorlevel 1 goto :fail
python scripts\phase_d\run_phase_d_3_segment_coral.py
if errorlevel 1 goto :fail
python scripts\phase_d\run_phase_d_4_coral_crca.py
if errorlevel 1 goto :fail
python scripts\phase_d\run_phase_d_6_d_to_white.py
if errorlevel 1 goto :fail
python scripts\phase_d\run_phase_d_9_aggregate.py
if errorlevel 1 goto :fail
python scripts\phase_d\run_phase_d_10_verify.py
if errorlevel 1 goto :fail

echo.
echo ✅ Phase D Flow B complete.
echo    Results: results\phase_d\
exit /b 0

:fail
echo.
echo ❌ A step failed. Check the error above.
exit /b 1