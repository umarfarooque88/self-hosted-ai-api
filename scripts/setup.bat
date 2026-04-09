@echo off
REM Self-Hosted AI API - Windows Setup Script
REM Run this script to set up the development environment

echo 🚀 Self-Hosted AI API - Setup Script
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    exit /b 1
)
echo ✅ Python found:
python --version

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama not found.
    echo Please install Ollama from: https://ollama.ai/
    echo After installing, run this script again.
    exit /b 1
)
echo ✅ Ollama found

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Dependencies installed

REM Copy environment file
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created. Please edit with your values.
) else (
    echo ✅ .env file already exists
)

REM Pull default model
echo 📥 Checking for default model...
ollama list | findstr "qwen:1.8b" >nul 2>&1
if errorlevel 1 (
    echo Pulling qwen:1.8b model (this may take a few minutes)...
    ollama pull qwen:1.8b
    echo ✅ Model pulled
) else (
    echo ✅ Default model already exists
)

echo.
echo ====================================
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Start Ollama: ollama serve
echo 3. Run the API: python src\app.py
echo 4. Test: curl http://localhost:8000/health
echo.
