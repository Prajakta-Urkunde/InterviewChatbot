@echo off
echo Starting Qrious Interview Bot...
echo.

echo Installing API dependencies...
pip install -r requirements_api.txt
echo.

echo Starting Backend API Server...
start "Qrious API Server" cmd /k python api_server.py
timeout /t 3 /nobreak >nul

echo Starting Frontend Development Server...
cd frontend
start "Qrious Frontend" cmd /k npm run dev
cd ..

echo.
echo Both servers are starting...
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:5173
echo.
echo Press any key to exit this window (servers will continue running)
pause >nul