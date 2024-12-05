from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import choose  # Импортируем функцию choose

# Модель запроса
class CharacterRequest(BaseModel):
    gender: str
    race: str
    character_class: str

# Создаём приложение FastAPI
app = FastAPI()

# Эндпоинт для создания персонажа
@app.post('/create_character')
def create_character(request: CharacterRequest):
    try:
        character = choose(request.gender, request.race, request.character_class)
        return character
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Запуск сервера для локальной разработки
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
