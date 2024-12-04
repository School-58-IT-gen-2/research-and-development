from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import json

# uvicorn api:app --reload

app = FastAPI()

class CharacterRequest(BaseModel):
    race: str
    class_: str

classs = {
    'Следопыт': 'pathfinder',
    "Варвар": "barbarian",
    "Бард": "bard",
    "Плут": "dodger",
    "Друид": "druid",
    "Колдун": "magician",
    "Монах": "monk",
    "Паладин": "paladin",
    "Жрец": "priest",
    "Маг": "warlock",
    "Воин": "warrior",
    "Волшебник": "wizzard"
}

races = {
    "Дварф": 'dwarf',
    "Эльф": 'elves',
    'Полурослик': "halfling",
    'Человек': "human",
    'Драконорожденный': "dragonborn",
    'Гном': "gnom",
    'Полуэльф': "halfelf",
    'Полуорк': "halfork",
    'Тифлинг': "tiefling"
}

with open('player.json', 'r', encoding="utf-8") as player_list:
    player_list = json.load(player_list)

def generate_character(race: str, class_: str):
    if race not in races or class_ not in classs:
        raise HTTPException(status_code=400, detail="Invalid race or class")

    race_key = races[race]
    class_key = classs[class_]

    try:
        with open(f'race/{race_key}.json', 'r', encoding="utf-8") as race_file:
            race_data = json.load(race_file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Race {race} not found")

    try:
        with open(f'classes/{class_key}.json', 'r', encoding="utf-8") as class_file:
            class_data = json.load(class_file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Class {class_} not found")

    subrace = race_data["race"].get('subraces', [])
    if subrace:
        random.shuffle(subrace)
        subrace = subrace[0]
        player_list["race"] = subrace['name']
    else:
        player_list["race"] = race_data["race"]['name']

    names = race_data["race"]["man_names"] if player_list["gender"] == "M" else race_data["race"]["woman_names"]
    random.shuffle(names)
    player_list["name"] = names[0]


    return player_list

@app.post("/generate_card/")
def create_character(character_request: CharacterRequest):
    race = character_request.race
    class_ = character_request.class_

    character = generate_character(race, class_)

    return character
