import json
import random

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


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
            "stats":{"strength":10,"dexterity":10,"constitution":10,"intelligence":10,"wisdom":10,"charisma":10},
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

    def get_classes(self):
        return read_json_file('json_data\main_constructor.json')['Classes']
    
    def set_class(self, char_class: str):
        self.player_list['character_class'] = char_class

    def get_races(self):
        return read_json_file('json_data\main_constructor.json')['Races']
    
    def set_race(self, char_race: str):
        self.player_list['race'] = char_race
        
    def get_characteristics(self):
        return ['1','2','3']
        return read_json_file('json_data\main_constructor.json')["Classes"][self.player_list["character_class"]]["Рекомендуемые характеристики"]
    
    def set_characteristics(self, characteristics):
        pass

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
        if self.skills_counter == skills_max_count:
            return 'thats it'
        return 'more'
        
    def get_skills(self):

        
        skills_list = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Список"]
        for skill in self.player_list["skills"]:

            skills_list.remove(skill)

        return {"skills_list": skills_list, "skills_count": self.skills_counter, "skills_limit": read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Количество"]}