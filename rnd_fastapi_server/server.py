from fastapi import FastAPI, HTTPException
from rnd_fastapi_server.models import Create, CharacterRequest
from rnd_fastapi_server.utils import choose
from model.char_constructor import CharConstructor
from db.db_source import DBSource
import httpx
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# @app.post("/create-character-list")
# async def register_user(create: Create):
#     return choose(create.gender.value, create.race.value, create.character_class.value)

@app.post("/initialize-character-list")
async def create_char(create: Create):
    new_char = CharConstructor()
    char_dict =  new_char.initialize_char(
                             char_class=create.character_class,
                             char_race=create.race,
                             char_subrace=create.subrace,
                             char_gender=create.gender,
                             user_id=create.user_id)
    supabase = DBSource(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))
    supabase.connect()
    char_dict['id'] = str(uuid.uuid4())
    
    supabase.insert("character_list", char_dict)
    #print(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list")
    #response = httpx.post(f"{os.getenv("QUESTHUB_URL")}/api/v1/characters/char-list",json=char_dict)
    return char_dict
    
@app.get("/character-list-options/{char_class}/{char_race}/{char_subrace}")
async def get_options(char_class: str, char_race: str, char_subrace: str):
    new_char = CharConstructor()
    new_char.initialize_char(char_class=char_class,
                             char_race=char_race,
                             char_subrace=char_subrace)
    return new_char.get_options()

@app.put("/save-character-list")
async def save_char(request: CharacterRequest):
    new_char = CharConstructor()
    updated_character = request.model_dump(exclude_unset=True)
    new_char.player_list = updated_character
    
    supabase = DBSource(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))
    supabase.connect()
    character_id = str(updated_character['id'])
    
    result = supabase.update("character_list", updated_character, character_id)
    
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Character not found")