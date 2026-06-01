@echo off
echo ==============================================
echo 🚀 Punjabi Guftar - Automation Pipeline V1.0
echo ==============================================

echo.
echo [1/3] Installing Required Libraries (Free & No API)...
python -m pip install -r requirements.txt

echo.
echo [2/3] Extracting Script and Generating Punjabi Voiceovers...
python generate_vo.py

echo.
echo [3/3] Downloading Royalty-Free Background Music...
python download_music.py

echo.
echo ✅ Tier 2 (Audio) Automation Complete!
pause
