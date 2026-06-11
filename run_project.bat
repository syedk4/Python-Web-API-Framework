@echo off
REM Run the Python Web API Testing Framework
REM Assumes you are running this inside an environment where `python` and required packages are available.

REM Change to the directory of this script (project root)
cd /d "%~dp0"

REM Optional: activate a virtual environment if you have one
REM call .venv\Scripts\activate
REM or: call venv\Scripts\activate

REM Start the application
py app.py

REM Keep the window open if run via double-click
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%.
    pause
) else (
    echo.
    echo Application stopped.
    pause
)

