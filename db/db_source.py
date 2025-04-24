from typing import List
from pydantic import SecretStr
from supabase.client import ClientOptions
from supabase import create_client, Client
import uuid
import json
import os


class DBSource():
    """Адаптер для работы с базой данных"""

    def __init__(self, url: str, key: str):
        """
        :param str url: Ссылка на supabase
        :param str key: Ключ от supabase
        """
        self.__url = url
        self.__key = key

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

    def insert(self, table_name: str, insert_dict: dict) -> List[dict]:
        """
        Вставка строки в таблицу.

        Args:
            table_name (str): Название таблицы.
            dict (dict): Словарь с данными для новой строки.
        
        Returns:
            List[dict]: Список из словаря с новой строкой.
        """
        return dict(self.__supabase.table(table_name).insert(insert_dict).execute())[
            "data"
        ]

    def update(self, table_name: str, update_dict: dict, id: str| uuid.UUID) -> List[dict]:
        """
        Изменение строки в таблице.

        Args:
            table_name (str): Название таблицы.
            dict (dict): Словарь с данными для новой строки.
            id (int): id строки, которую нужно изменить.

        Returns:
            List[dict]: Список из словаря с новой строкой.
        """
        return dict(
            self.__supabase.table(table_name).update(update_dict).eq("id", id).execute()
        )["data"]
    
    def get_race_data_by_name(self,name: str) -> list:
        return dict(self.__supabase.table("races").select().eq("name", name).execute())[
            "data"
        ][0]
    
    def get_class_data_by_name(self,name: str) -> list:
        return dict(self.__supabase.table("classes").select().eq("name", name).execute())[
            "data"
        ][0]
    def get_weapon_data(self) -> list:
        return dict(self.__supabase.table("weapon").select().eq("id", 1).execute())[
            "data"
        ][0]
    def get_player_data(self) -> list:
        return dict(self.__supabase.table("character_list").select().eq("id", 11).execute())["data"][0]
    
    
    def get_spells_data(self) -> list:
        return dict(self.__supabase.table("spells").select().eq("id", 1).execute())[
            "data"
        ][0]
    def get_lore_data(self) -> list:
        return dict(self.__supabase.table("lore").select().eq("id", 1).execute())[
            "data"
        ][0]
