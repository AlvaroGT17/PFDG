@echo off
chcp 65001 >nul

echo Iniciando el servidor BACKEND...
start "Backend Server" cmd /k "cd /d D:\Programación\Proyecto_Final_de_Grado\PFDG\backend && title Backend Server && (for /L %%i in (0) do (title Backend Server & timeout /t 1 >nul)) | npm run dev"
timeout /t 3 >nul

echo Iniciando el servidor FRONTEND...
start "Frontend Server" cmd /k "cd /d D:\Programación\Proyecto_Final_de_Grado\PFDG\frontend && title Frontend Server && (for /L %%i in (0) do (title Frontend Server & timeout /t 1 >nul)) | npm run dev"
timeout /t 5 >nul

echo Abriendo navegador con la página de login...
start "" "http://localhost:1702"

