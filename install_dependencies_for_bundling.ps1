# Ensure pip is available
$python = "python"
$pip = "$python -m pip"

# List of packages to install
$packages = @("pywin32", "pyinstaller", "pystray", "pillow")

foreach ($pkg in $packages) {
    Write-Host "Installing $pkg..." -ForegroundColor Cyan
    & $pip install $pkg
}

Write-Host "✅ All packages installed successfully!" -ForegroundColor Green
