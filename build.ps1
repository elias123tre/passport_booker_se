# Make sure you have a virtualenv in the folder `venv` with playwright and pyinstaller installed
# Steps to do the above:
# 1. `python -m venv venv`
# 2. `.\venv\Scripts\Activate.ps1`
# 3. `pip install playwright pyinstaller`
# 4. Run this file to build a packaged binary

$env:PLAYWRIGHT_BROWSERS_PATH="0"
& .\venv\Scripts\playwright.exe install chromium
& .\venv\Scripts\pyinstaller --onefile main.py