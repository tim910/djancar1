@echo off
title DjanCar - Carsharing Ulyanovsk
color 0E

cd /d "%~dp0"

echo.
echo ==========================================
echo    DjanCar - Carsharing Ulyanovsk
echo ==========================================
echo.

REM ===== [1] Check Python =====
echo [1/7] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)
python --version

REM ===== [2] Create venv if missing =====
echo.
echo [2/7] Virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo   Creating venv...
    python -m venv venv
    if errorlevel 1 (
        echo   ERROR: failed to create venv
        pause
        exit /b 1
    )
    echo   OK - venv created
) else (
    echo   OK - venv exists
)

call venv\Scripts\activate.bat

REM ===== [3] Install dependencies if needed =====
echo.
echo [3/7] Dependencies...
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo   Installing packages... this may take 2 minutes
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt
    if errorlevel 1 (
        echo   ERROR: pip install failed
        pause
        exit /b 1
    )
    echo   OK - packages installed
) else (
    echo   OK - packages already installed
)

REM ===== [4] Create .env if missing =====
echo.
echo [4/7] Configuration .env...
if not exist ".env" (
    copy .env.example .env >nul
    echo   OK - .env created with Yandex API key
    echo.
    echo   IMPORTANT: edit .env if your postgres password is not "postgres"
    echo.
) else (
    echo   OK - .env exists
)

REM ===== [5] Check PostgreSQL connection =====
echo.
echo [5/7] Checking PostgreSQL...
python -c "import os; from decouple import config; import psycopg2; psycopg2.connect(host=config('DB_HOST',default='127.0.0.1'), port=config('DB_PORT',default='5432'), user=config('DB_USER',default='postgres'), password=config('DB_PASSWORD',default='postgres'), dbname='postgres')" 2>nul
if errorlevel 1 (
    echo   ERROR: cannot connect to PostgreSQL
    echo.
    echo   Make sure:
    echo     1. PostgreSQL is installed and running
    echo     2. The password in .env matches your postgres user password
    echo.
    echo   Install PostgreSQL: https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)
echo   OK - PostgreSQL connection works

REM ===== [6] Create database if missing =====
echo.
echo [6/7] Database "djancar"...
python -c "from decouple import config; import psycopg2; from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT; conn=psycopg2.connect(host=config('DB_HOST',default='127.0.0.1'), port=config('DB_PORT',default='5432'), user=config('DB_USER',default='postgres'), password=config('DB_PASSWORD',default='postgres'), dbname='postgres'); conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT); cur=conn.cursor(); cur.execute(\"SELECT 1 FROM pg_database WHERE datname='djancar'\"); exists=cur.fetchone(); cur.execute('CREATE DATABASE djancar') if not exists else None; conn.close(); print('OK')"
if errorlevel 1 (
    echo   ERROR: cannot create djancar database
    pause
    exit /b 1
)

REM ===== [7] Migrations + demo data (only first time) =====
echo.
echo [7/7] Migrations and demo data...
python manage.py makemigrations accounts cars rentals core --noinput >nul 2>&1
python manage.py migrate --noinput
if errorlevel 1 (
    echo   ERROR: migration failed
    pause
    exit /b 1
)

REM Seed only if no cars yet
python -c "import django,os;os.environ.setdefault('DJANGO_SETTINGS_MODULE','djancar.settings');django.setup();from cars.models import Car;exit(0 if Car.objects.exists() else 1)" >nul 2>&1
if errorlevel 1 (
    echo   First run - loading demo data...
    python manage.py seed_demo
) else (
    echo   OK - data already loaded
)

REM ===== Start server =====
echo.
echo ==========================================
echo    DjanCar is ready!
echo ==========================================
echo    Site:   http://127.0.0.1:8000
echo    Admin:  http://127.0.0.1:8000/admin/
echo ==========================================
echo    admin / admin12345  - superuser
echo    demo  / demo12345   - regular user
echo ==========================================
echo    Press Ctrl+C to stop the server
echo ==========================================
echo.

start "" "http://127.0.0.1:8000"
python manage.py runserver

pause
