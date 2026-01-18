@echo off
REM ========================================
REM Clean Git History - Remove API Key
REM ========================================
REM This script creates a fresh git history
REM without the API key that was in the first commit
REM ========================================

echo.
echo ============================================
echo  ClickSUMO - Clean Git History Script
echo ============================================
echo.
echo This will:
echo  1. Backup your current .git folder
echo  2. Create a fresh git repository
echo  3. Commit all files WITHOUT the API key
echo.
echo Your files are safe - only git history is affected
echo.
pause

echo.
echo [1/5] Backing up current .git folder...
if exist .git_backup rmdir /s /q .git_backup
move .git .git_backup
echo      ✓ Backup created at .git_backup

echo.
echo [2/5] Initializing fresh git repository...
git init
git branch -M main
echo      ✓ Fresh repository created

echo.
echo [3/5] Adding all files (API keys are protected by .gitignore)...
git add .
echo      ✓ Files staged

echo.
echo [4/5] Creating initial commit...
git commit -m "Initial release: ClickSUMO v8.0 (NEBULA AI) with RAG

ClickSUMO - AI-Powered SUMO Traffic Simulation Platform

Features:
- One-click network creation with 6 templates
- AI-powered traffic demand generation
- Advanced signal optimization (Webster's method, coordination)
- RAG-enhanced AI assistant with SUMO documentation search
- Real-time output analysis with interactive visualizations
- Project save/load system
- Documentation browser with semantic search

Version: 8.0 (NEBULA AI)
Author: Mahbub Hassan
Institution: Chulalongkorn University
License: MIT"

echo      ✓ Clean commit created

echo.
echo [5/5] Verifying no API keys in repository...
git grep -i "gsk_Pqi" && (
    echo      ✗ ERROR: API key found!
    echo.
    echo Please check the files manually.
    pause
    exit /b 1
) || (
    echo      ✓ No API keys found - SAFE to push!
)

echo.
echo ============================================
echo  SUCCESS! Your git history is now clean
echo ============================================
echo.
echo Your old git history is backed up at: .git_backup
echo You can delete it after pushing to GitHub.
echo.
echo Next steps:
echo  1. Create a new repository on GitHub
echo  2. Run: git remote add origin https://github.com/YOUR_USERNAME/clicksumo.git
echo  3. Run: git push -u origin main
echo.
echo See GITHUB_PUSH_GUIDE.md for detailed instructions
echo.
pause
