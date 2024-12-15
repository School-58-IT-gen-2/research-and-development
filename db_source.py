from typing import List
from pydantic import SecretStr
from supabase.client import ClientOptions
from supabase import create_client, Client
import json


class DBSource():
    """Адаптер для работы с базой данных"""

    def __init__(self, url: str, key: SecretStr):
        """
        :param str url: Ссылка на supabase
        :param str key: Ключ от supabase
        """
        self.__url = url
        self.__key = key.get_secret_value()

    def connect(self) -> None:
        """Подключение к БД"""
        try:
            supabase: Client = create_client(
                supabase_url=self.__url,
                supabase_key=self.__key,
                options=ClientOptions(
                    postgrest_client_timeout=10,
                    storage_client_timeout=10,
                    schema="public",
                ),
            )
            self.__supabase = supabase
        except Exception as error:
            print(f"Error: {error}")

    def insert_race(self, race) -> List[dict]:
        with open(f'race/{race}.json', 'r', encoding="utf-8") as race_file: 
            race_file = json.load(race_file)
        raceL = {
            "name": race,
            "race": race_file["race"],
            "class_options": race_file["class_options"],
            "starting_equipment": race_file["starting_equipment"]
        }
        """
        Вставка строки в таблицу

        :param str table_name: Название таблицы
        :param dict dict: Словарь с данными для новой строки
        :return List[dict]: Список из словаря с новой строкой
        """
        return dict(self.__supabase.table(race).insert(raceL).execute())[
            "data"
        ]
    
    def insert_class(self, clas) -> List[dict]:
        with open(f'classes/{clas}.json', 'r', encoding="utf-8") as class_file: 
            class_file = json.load(class_file)
        class_dict = {
            "name": clas,
            "class": class_file["class"]
        }
        """
        Вставка строки в таблицу

        :param str table_name: Название таблицы
        :param dict dict: Словарь с данными для новой строки
        :return List[dict]: Список из словаря с новой строкой
        """
        return dict(self.__supabase.table("classes").insert(class_dict).execute())[
            "data"
        ]

    def get_race_data_by_name(self,name: str) -> list:
        return dict(self.__supabase.table("races").select().eq("name", name).execute())[
            "data"
        ]
    
    def get_clas_data_by_name(self,name: str) -> list:
        return dict(self.__supabase.table("classes").select().eq("name", name).execute())[
            "data"
        ]
    def get_weapon_data(self) -> list:
        return dict(self.__supabase.table("weapon").select().eq("id", 1).execute())[
            "data"
        ]
    def get_spells_data(self) -> list:
        return dict(self.__supabase.table("weapon").select().eq("id", 1).execute())[
            "data"
        ]
    def get_lore_data(self) -> list:
        return dict(self.__supabase.table("lore").select().eq("id", 1).execute())[
            "data"
        ]
    
    def create_new_race(self,race :str) -> None:
        with open(f'race/{race}.json', 'r', encoding="utf-8") as race_file: 
            race_file = json.load(race_file)
        race = {
            "name": race,
            "race": race_file["race"],
            "class_options": race_file["class_options"],
            "starting_equipment": race_file["starting_equipment"]
        }

        return self.__supabase.table('races').insert(race).execute()

    def create_new_clas(self,clas :str) -> None:
        print(clas)
        with open(f'classes/{clas}.json', 'r', encoding="utf-8") as class_file: 
            class_file = json.load(class_file)
        class_ = {
            "name": clas,
            "class": class_file["class"]
        }

        self.__supabase.table('races').insert(class_).execute()
