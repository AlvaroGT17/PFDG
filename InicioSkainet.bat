@echo off
chcp 65001 >nul

echo Iniciando el servidor BACKEND...
start "Backend Server" /D "D:\Programación\Proyecto_Final_de_Grado\PFDG\backend" cmd /k "npm run dev"
timeout /t 3 >nul

echo Iniciando el servidor FRONTEND...
start "Frontend Server" /D "D:\Programación\Proyecto_Final_de_Grado\PFDG\frontend" cmd /k "npm run dev"
timeout /t 5 >nul

echo Abriendo navegador con la página de login...
start "" "http://localhost:1702"
