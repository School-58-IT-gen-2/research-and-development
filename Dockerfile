# Используем образ Python 3.10
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir fastapi uvicorn

# Открываем порт 8000
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
