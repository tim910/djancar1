#!/usr/bin/env bash
# Скрипт сборки для Render.com
# Render запускает его автоматически перед стартом сервиса.

set -o errexit

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Applying database migrations..."
python manage.py makemigrations accounts cars rentals core --no-input
python manage.py migrate --no-input

echo "==> Loading demo data (idempotent)..."
python manage.py seed_demo || echo "seed_demo skipped"

echo "==> Fixing car image_filenames for existing cars..."
python manage.py fix_car_images || echo "fix_car_images skipped"

echo "==> Build complete!"
