@echo off

REM Set the working directory to the Flask application directory
cd "D:\ClearTax\UAT\code"

:restart
REM Start the Flask server
"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" app.py

REM wait for 24 hours (86400 seconds)
timeout /t 86400 /nobreak

REM Restart the script
goto restart