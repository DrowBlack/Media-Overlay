@echo off
taskkill /f /im pythonw.exe
echo App closed.
timeout /t 2 >nul