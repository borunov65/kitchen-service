#!/usr/bin/env bash
set -e

echo "Starting build.sh"

# Завантажуємо змінні з .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Встановлюємо Poetry, якщо він ще не встановлений
if ! command -v poetry &> /dev/null
then
    echo "Poetry not found, installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Встановлюємо залежності
poetry install --no-root

# Міграції
python3 manage.py migrate

# Збірка статичних файлів
python3 manage.py collectstatic --noinput

echo "Build finished successfully!"
