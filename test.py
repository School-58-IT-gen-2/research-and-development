from fastapi.testclient import TestClient
from main import app, choose  

# Создаём экземпляр TestClient
client = TestClient(app)


# Определяем тестовые данные (пользовательские параметры)
data = {
    "gender": "M",
    "rac": "Дварф",
    "clas": "Воин"
}

# Отправляем POST запрос на endpoint /register/
response = client.post("/register/", params=data)

# Печатаем статус код и ответ
print("Response status code:", response.status_code)
print("Response JSON:", response.json())

