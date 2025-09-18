@echo off
echo.
echo =============================================
echo   🏫 Sistema de Gestão Escolar
echo   Iniciando servidores...
echo =============================================
echo.

echo 🔧 Verificando dependências...
cd back-end
python -c "import fastapi, uvicorn, sqlalchemy, jose, passlib, python_multipart" 2>nul
if errorlevel 1 (
    echo ❌ Instalando dependências...
    pip install -r requirements.txt
)

echo.
echo 🚀 Iniciando Backend (FastAPI)...
start "Backend - Sistema Escolar" cmd /k "python start.py"

echo.
echo ⏳ Aguardando backend inicializar...
timeout /t 3

echo.
echo 🌐 Iniciando Frontend (HTTP Server)...
cd ..\front-end
start "Frontend - Sistema Escolar" cmd /k "python -m http.server 8080"

echo.
echo ⏳ Aguardando frontend inicializar...
timeout /t 2

echo.
echo =============================================
echo   ✅ Sistema iniciado com sucesso!
echo =============================================
echo.
echo 🌐 Frontend: http://localhost:8080
echo 🔧 Backend:  http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo 🔍 Debug:    http://localhost:8080/debug.html
echo.
echo 🔐 Login: admin@escola.com / 123456
echo.
echo ❗ Mantenha estas janelas abertas para o sistema funcionar
echo ❗ Para parar: Feche as janelas ou pressione Ctrl+C
echo.

echo 🌐 Abrindo sistema no navegador...
timeout /t 2
start http://localhost:8080

pause