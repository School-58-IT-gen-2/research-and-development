from fastapi import FastAPI
from rnd_fastapi_server.models import Create
from rnd_fastapi_server.utils import choose

app = FastAPI()

@app.post("/create-character-list")
async def register_user(create: Create):
    return choose(create.gender.value, create.race.value, create.character_class.value)