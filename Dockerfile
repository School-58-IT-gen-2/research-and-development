FROM python:3.10-slim

WORKDIR /app

COPY . /app
COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1

CMD ["uvicorn", "rnd_fastapi_server.server:app", "--host", "0.0.0.0", "--port", "6000"]