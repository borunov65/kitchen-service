#!/usr/bin/env bash
set -e

echo "Starting build.sh"

# Завантажуємо змінні з .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Оновлюємо pip і встановлюємо залежності
pip install --upgrade pip
pip install -r requirements.txt

# Міграції
python3 manage.py migrate

# Збірка статичних файлів
python3 manage.py collectstatic --noinput

echo "Build finished successfully!"
