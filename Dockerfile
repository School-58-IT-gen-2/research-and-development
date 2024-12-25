FROM python:3.10-slim

WORKDIR /app

COPY . /app
COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "rnd_fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "uvicorn rnd_fastapi_server:app --host 0.0.0.0 --port 8000 & python tg_bot.py"]