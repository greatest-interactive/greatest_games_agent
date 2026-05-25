# Collect Game Market Data - PowerShell Script
# This script collects trending game data from all platforms

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  GREATEST GAME AGENT - DATA COLLECTION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Activate virtual environment
& "$scriptPath\venv\Scripts\Activate.ps1"

# Run collection script
python "$scriptPath\collect_data.py"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
