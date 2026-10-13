# ============================================================
#  deploy-vercel.ps1 — Deploy Swift Sign Chatbot to Vercel
#  Run this in PowerShell from the project folder:
#      powershell -ExecutionPolicy Bypass -File deploy-vercel.ps1
#  It will: fix PATH, log you in (once), set the API key, deploy.
# ============================================================

# 1) Make node + vercel CLI available
$env:PATH = 'C:\Program Files\nodejs;' + $env:PATH + ';' + $env:APPDATA + '\npm'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host ""
Write-Host "=== Swift Sign Chatbot -> Vercel Deploy ===" -ForegroundColor Cyan
Write-Host ""

# 2) Ensure logged in (interactive — a browser window will open ONCE)
$who = vercel whoami 2>&1 | Out-String
if ($who -match "Logged out" -or $who -match "Error" -or [string]::IsNullOrWhiteSpace($who)) {
    Write-Host "Logging in to Vercel (complete this in your browser)..." -ForegroundColor Yellow
    vercel login
} else {
    Write-Host "Already logged in as: $($who.Trim())" -ForegroundColor Green
}

# 3) Link to the existing project (uses .vercel/project.json)
Write-Host "Linking project..." -ForegroundColor Cyan
vercel link --yes

# 4) Set GEMINI_API_KEY from backend/.env (without printing it)
$envFile = Join-Path $root "backend\.env"
$apiKey = $null
if (Test-Path $envFile) {
    $line = Get-Content $envFile | Where-Object { $_ -match '^\s*GEMINI_API_KEY\s*=' } | Select-Object -First 1
    if ($line) { $apiKey = ($line -split '=', 2)[1].Trim() }
}
if (-not $apiKey) { $apiKey = $env:GEMINI_API_KEY }

if ($apiKey) {
    Write-Host "Setting GEMINI_API_KEY in Vercel (Production)..." -ForegroundColor Cyan
    $apiKey | vercel env add GEMINI_API_KEY production
    Write-Host "API key set." -ForegroundColor Green
} else {
    Write-Host "WARNING: Could not find GEMINI_API_KEY in backend\.env." -ForegroundColor Red
    Write-Host "Add it manually in Vercel -> Settings -> Environment Variables." -ForegroundColor Red
}

# 5) Deploy to production
Write-Host ""
Write-Host "Deploying to production..." -ForegroundColor Cyan
vercel --prod

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host "Open https://swiftsign-chatbot.vercel.app and test the chat." -ForegroundColor Green
Write-Host ""
