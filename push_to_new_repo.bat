@echo off
echo ========================================
echo Push to New GitHub Repository
echo Python-Web-API-Framework
echo ========================================
echo.

echo IMPORTANT FIRST STEP:
echo.
echo You need to allow the secret in GitHub first!
echo.
echo 1. Open this link in your browser:
echo    https://github.com/syedk4/Python-Web-API-Framework/security/secret-scanning/unblock-secret/3EzrlJHe6Jz6uWlATVVDhHb2eYK
echo.
echo 2. Click the "Allow secret" button
echo.
echo 3. Then come back here and press any key to continue...
echo.
pause

echo.
echo ========================================
echo Pushing Code to GitHub...
echo ========================================
echo.

echo [1/3] Pushing main branch...
git push origin main
echo.

echo [2/3] Pushing feature/testing branch...
git push origin feature/testing
echo.

echo [3/3] Pushing all other branches...
git push --all origin
echo.

echo ========================================
echo DONE!
echo ========================================
echo.
echo Your repository is now at:
echo https://github.com/syedk4/Python-Web-API-Framework
echo.
echo You can view it in your browser!
echo.
pause

