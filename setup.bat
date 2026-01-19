@echo off
REM Setup script for Document Scanner Application (Windows)

echo ================================================
echo    Document Scanner - Setup Script
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)
echo All dependencies installed successfully
echo.

REM Create necessary directories
echo Setting up project directories...
if not exist data\sample_images mkdir data\sample_images
if not exist data\output mkdir data\output
echo Directories created
echo.

REM Run tests
echo Running tests...
pytest tests\ -v

if errorlevel 1 (
    echo Some tests failed, but you can still use the application
) else (
    echo All tests passed
)
echo.

REM Final message
echo ================================================
echo    Setup Complete!
echo ================================================
echo.
echo To run the application:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run the application:
echo      python main.py
echo.
echo For more information, see:
echo   - QUICKSTART.md - Quick start guide
echo   - README.md - Full documentation
echo.
echo Happy scanning!
echo.
pause
