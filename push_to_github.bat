@echo off
REM Script to safely push changes to GitHub
REM This script verifies that config.env is excluded before pushing

echo ========================================
echo Python-API-Testing-Framework - GitHub Push Script
echo ========================================
echo.

echo Step 1: Checking if config.env is properly excluded...
git check-ignore -v config.env
if %ERRORLEVEL% EQU 0 (
    echo [OK] config.env is properly excluded from git
) else (
    echo [ERROR] config.env is NOT excluded! Aborting.
    echo Please check your .gitignore file.
    pause
    exit /b 1
)
echo.

echo Step 2: Showing current git status...
git status
echo.

echo Step 3: Files to be committed:
echo ----------------------------------------
git add .
git status --short
echo ----------------------------------------
echo.

echo WARNING: Please review the files above carefully!
echo Make sure config.env is NOT listed.
echo.
set /p CONTINUE="Do you want to continue? (yes/no): "

if /i NOT "%CONTINUE%"=="yes" (
    echo Aborted by user.
    pause
    exit /b 0
)

echo.
echo Step 4: Committing changes...
set /p COMMIT_MSG="Enter commit message: "
git commit -m "%COMMIT_MSG%"

echo.
echo Step 5: Pushing to GitHub...
git push

echo.
echo ========================================
echo Push completed!
echo ========================================
echo.
echo Your repository: https://github.com/syedk4/Python-API-Testing-Framework
echo.
pause

