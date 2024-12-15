from supabase import create_client, Client
from datetime import datetime, timezone
import json
import supabase

class SupabaseDBAdapter :
    def __init__(self, url:str, key:str) -> None:
        supabase: Client = create_client(url, key)

    def get_race_data_by_name(name: str) -> list:
        race_data = supabase.table("races").select("*").eq("name", name).execute()
        return race_data.data
    
    def get_clas_data_by_name(name: str) -> list:
        clas_data = supabase.table("classes").select("*").eq("name", name).execute()
        return clas_data.data

    def create_new_race(adapter,race :str) -> None:
        with open(f'race/{race}.json', 'r', encoding="utf-8") as race_file: 
            race_file = json.load(race_file)
        race = {
            "name": race,
            "race": race_file["race"],
            "class_options": race_file["class_options"],
            "starting_equipment": race_file["starting_equipment"]
        }

        supabase.table('races').insert(race).execute()

    def create_new_clas(adapter,clas :str) -> None:
        print(clas)
        with open(f'classes/{clas}.json', 'r', encoding="utf-8") as class_file: 
            class_file = json.load(class_file)
        class_ = {
            "name": clas,
            "class": class_file["class"]
        }

        supabase.table('races').insert(class_).execute()

