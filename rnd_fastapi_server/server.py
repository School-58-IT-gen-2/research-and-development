from fastapi import FastAPI
from rnd_fastapi_server.models import Create
from rnd_fastapi_server.utils import choose
from model.char_constructor import CharConstructor

app = FastAPI()

# @app.post("/create-character-list")
# async def register_user(create: Create):
#     return choose(create.gender.value, create.race.value, create.character_class.value)

@app.post("/initialize-character-list")
async def create_char(create: Create):
    new_char = CharConstructor()
    return new_char.initialize_char(char_class=create.character_class,
                             char_race=create.race,
                             char_subrace=create.subrace)
    
@app.get("/character-list-options/{char_class}/{char_race}/{char_subrace}")
async def get_options(char_class: str, char_race: str, char_subrace: str):
    new_char = CharConstructor()
    new_char.initialize_char(char_class=char_class,
                             char_race=char_race,
                             char_subrace=char_subrace)
    return new_char.get_options()