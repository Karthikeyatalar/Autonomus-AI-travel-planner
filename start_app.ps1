$frontendPath = Join-Path -Path $PSScriptRoot -ChildPath "frontend"
$backendPath = Join-Path -Path $PSScriptRoot -ChildPath "backend"

Write-Host "Starting AI Travel Management Application..." -ForegroundColor Green

# Start Backend in a new window
Write-Host "Starting Backend..." -ForegroundColor Cyan
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; & '.\.venv\Scripts\python.exe' -m uvicorn app.main:app --reload"

# Start Frontend in a new window
Write-Host "Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Write-Host "Both services are starting in separate windows!" -ForegroundColor Green
