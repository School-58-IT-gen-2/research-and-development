import os
import json
import random
from db.db_source import DBSource


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

clases = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Маг":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

class CharConstructor:
    def __init__(self):
        self.player_list = {
            "race": "",
            "character_class": "",
            "initiative": 1,
            "experience": 0,
            "ownership_bonus": 2,
            "ability_saving_throws": {},
            "death_saving_throws": 0,
            "inspiration": False,
            "skills":[],
            "interference": False,
            "advantages": False,
            "traits_and_abilities":{},
            "weaknesses":{},
            "valuables":{},
            "name": "",
            "stat_modifiers":{"strength":0,"dexterity":0,"constitution":0,"intelligence":0,"wisdom":0,"charisma":0},
            "stats":{"strength":None,"dexterity":None,"constitution":None,"intelligence":None,"wisdom":None,"charisma":None},
            "backstory": "",
            "notes": "",
            "diary": "",
            "hp": 0,
            "level": 1,
            "passive_perception": 1,
            "travel_speed": 1,
            "speed": 0,
            "weapons_and_equipment":{},
            "spells":{},
            "languages":[],
            "special_features":{},
            "npc_relations":{},
            "user_id":0,
            "surname": "",
            "inventory": [],
            "age": 1,
            "attack_and_damage_values":{},
            "worldview": ""
        }
        self.skills_counter = 0
        self.inventory_counter = 0
        self.inventory_lim = 0
        self.__characteristic_limit = 27
        self.supabase = DBSource(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))
        self.supabase.connect()

    def get_classes(self):
        return read_json_file('json_data\main_constructor.json')['Classes']
    
    def set_class(self, char_class: str):
        self.player_list['character_class'] = char_class
        print(f'Выбран класс: {char_class}')

    def get_races(self):
        return read_json_file('json_data\main_constructor.json')['Races']
    
    def set_race(self, char_race: str):
        self.player_list['race'] = char_race
        print(f'Выбрана раса: {char_race}')
        
    def get_characteristics(self):
        characteristics_translate = {'strength': 'Сила', "dexterity": "Ловкость",
                                     "constitution": "Телосложение", "intelligence": "Интеллект",
                                     "wisdom": "Мудрость", "charisma": "Харизма"}
        target_characteristic = next((k for k, v in self.player_list['stats'].items() if v is None), None)
        
        if target_characteristic == None: return None, None, None
        
        recomended_str = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Рекомендуемые характеристики"][characteristics_translate[target_characteristic]]
        
        recomended_min, recomended_max = list(map(int, recomended_str.split('-')))
        recomended_btns = list(map(str, range(8, min(16, recomended_max + 3))))
        
        recomended_btns = list(filter(lambda x: (9 if int(x) == 15 else int(x) - 8) <= self.__characteristic_limit, recomended_btns))
        recomended_to_class = list(map(str, list(range(recomended_min, recomended_max + 1))))
        
        return characteristics_translate[target_characteristic], recomended_btns, recomended_to_class
    
    def set_characteristics(self, characteristics):
        target_characteristic = next((k for k, v in self.player_list['stats'].items() if v is None), None)
        self.__characteristic_limit -= 9 if int(characteristics) == 15 else int(characteristics) - 8
        exec(f"self.player_list['stats']['{target_characteristic}'] = {int(characteristics)}")
        print(f'Выбрана: {target_characteristic}, значение: {characteristics}')

    def add_skill(self, skill):
        if skill == 'random':
            skills_list = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Список"]
            print(skills_list)
            print(self.player_list['skills'])
            for skill in self.player_list["skills"]:
                print(skill)
                skills_list.remove(skill)
            
            self.player_list['skills'].append(random.choice(skills_list))
        else:
            self.player_list['skills'].append(skill)
        self.skills_counter += 1
        skills_max_count = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Количество"]
        print(f'Выбран навык: {skill}, количество навыков: {self.skills_counter}, максимальное количество навыков: {skills_max_count}')
        if self.skills_counter == skills_max_count:
            return 'thats it'
        return 'more'
        
    def get_skills(self):

        
        skills_list = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Список"]
        for skill in self.player_list["skills"]:

            skills_list.remove(skill)

        return {"skills_list": skills_list, "skills_count": self.skills_counter, "skills_limit": read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Количество"]}
    
    def get_inventory(self) -> list[str]:
        
        options_list = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Опции инвентаря"]
        self.inventory_lim = len(options_list)
        return options_list
    
    def add_inventory(self, item: str):
        #race_file = self.supabase.get_race_data_by_name(self.race)
        for i in item.split(' + '):
            weapon_file = self.supabase.get_weapon_data()
            for i in self.player_list["weapons_and_equipment"]:
                if i not in weapon_file["armor"]:
                    self.player_list["attack_and_damage_values"][i] = weapon_file["weapons"][i]
            
            if i in weapon_file["weapons"].keys():
                self.player_list["weapons_and_equipment"][i] = weapon_file["weapons"][i]
            elif i in weapon_file['armor'].keys():
                self.player_list["weapons_and_equipment"][i] = weapon_file['armor'][i]
            else:
                self.player_list['inventory']
                
        self.inventory_counter += 1
        
    def set_gender(self, gender):
        print(f'Выбран гендер: {gender}')


    def set_name(self, name):
        print(f'Выбрано имя: {name}')


    def set_story(self, story):
        print(f'Выбрана предыстория: {story}')


    def set_age(self, age):
        print(f'Выбран возраст: {age}')

    def get_result(self):
        return "Персонаж:\n - гемор\n - мутор"

