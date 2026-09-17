# STATWISE One-Click PowerShell Launcher
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "      STATWISE: MoSPI AI Learning Platform (Problem Statement 26101)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Check Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "[OK] Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not found in PATH." -ForegroundColor Red
    exit 1
}

# Check Node
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js is not found in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "`nStarting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "-m uvicorn backend.main:app --host 127.0.0.1 --port 8000" -WindowStyle Normal

Write-Host "Starting Frontend Dev Server on http://127.0.0.1:5173..." -ForegroundColor Yellow
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Set-Location frontend; npm run dev -- --host 127.0.0.1 --port 5173" -WindowStyle Normal

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "STATWISE Platform Launched Successfully!" -ForegroundColor Green
Write-Host "  Frontend Web UI:   http://127.0.0.1:5173/" -ForegroundColor White
Write-Host "  Backend API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
