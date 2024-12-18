from fastapi import FastAPI
from pydantic import BaseModel
import json
import random
from db_source import DBSource
import uvicorn
from dotenv import load_dotenv
import os



clases = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Маг":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

load_dotenv()
supabase = DBSource(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))
supabase.connect()
print(supabase.get_lore_data())
print(supabase.get_player_data())
print(supabase.get_spells_data())

print()