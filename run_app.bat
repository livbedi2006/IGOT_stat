@echo off
title STATWISE - MoSPI AI Skill Intelligence Platform
echo ======================================================================
echo       STATWISE: MoSPI AI Learning Platform (Problem Statement 26101)
echo ======================================================================
echo.

echo [1/3] Checking dependencies...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed or not in PATH.
    pause
    exit /b 1
)

echo [2/3] Starting FastAPI Backend on port 8000...
start "STATWISE Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

echo [3/3] Starting Frontend on port 5173...
start "STATWISE Frontend" cmd /k "cd frontend && npm run dev -- --host 127.0.0.1 --port 5173"

echo.
echo ======================================================================
echo STATWISE is launching!
echo Frontend: http://127.0.0.1:5173/
echo Backend API Docs: http://127.0.0.1:8000/docs
echo ======================================================================
echo.
pause
