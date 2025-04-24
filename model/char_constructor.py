import os
import json
import random
from db.db_source import DBSource


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

classes = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Чародей":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}
WEAPON_GROUPS = ['Простое дальнобойное', 'Воинское дальнобойное', "Простое рукопашное", "Воинское рукопашное", "Воинское"]
CHARACTERISTICS_TRANSLATE = {'strength': 'Сила', "dexterity": "Ловкость",
                                     "constitution": "Телосложение", "intelligence": "Интеллект",
                                     "wisdom": "Мудрость", "charisma": "Харизма"}

class CharConstructor:
    def __init__(self):
        self.player_list = {
            "id": None,
            "race": "",
            "subrace": "",
            "character_class": "",
            "initiative": 1,
            "experience": 0,
            "ownership_bonus": 2,
            "ability_saving_throws": {},
            "death_saving_throws": 0,
            "inspiration": False,
            "skills": [],
            "interference": False,
            "advantages": False,
            "traits_and_abilities": {},
            "class_features": {},
            "weaknesses": {},
            "valuables": {},
            "name": "",
            "stat_modifiers": {"strength": 0, "dexterity": 0, "constitution": 0, 
                            "intelligence": 0, "wisdom": 0, "charisma": 0},
            "stats": {"strength": None, "dexterity": None, "constitution": None,
                    "intelligence": None, "wisdom": None, "charisma": None},
            "backstory": "",
            "notes": "",
            "diary": "",
            "hp": 0,
            "lvl": 1,  # добавлено из первой модели
            "passive_perception": 1,
            "travel_speed": 1,
            "speed": 0,
            "weapons_and_equipment": {},
            "spells": {},
            "languages": [],
            "special_features": {},
            "npc_relations": {},
            "user_id": 0,
            "surname": "",
            "inventory": [],
            "age": 1,
            "attack_and_damage_values": {},
            "worldview": "",
            "gender": "",
            # Новые поля из первой модели
            "gold": None,
            "archetype": None,
            "fighting_style": None,
            "created_at": None
        }
        self.skills_counter = 0
        self.inventory_counter = 0
        self.inventory_lim = 0
        self.supabase = DBSource(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))
        self.supabase.connect()
        self.__characteristic_limit = 27
        self.__race_data = dict()
        self.__subrace_data = dict()
        self.__class_data = dict()
        self.__last_characteristic_variants = []
        
    def initialize_char(self, char_class: str, char_race: str, char_subrace: str, char_gender: str, user_id: str):
        '''
        Инициализация персонада по 3 параметрам
        Request: класс, раса, подраса
        Response: лист со значениями по умолчанию
        '''
        self.set_class(char_class)
        self.set_race(char_race)
        self.set_subrace(char_subrace if char_subrace != None else 'random')
        self.set_gender(char_gender)
        self.player_list['user_id'] = user_id
        
        self.set_initialize_default_values()
        
        return self.player_list
    
    def get_options(self):
        characteristics_dict = dict()
        for stat in list(CHARACTERISTICS_TRANSLATE.values()):
            data = self.get_characteristics()
            characteristics_dict[stat] = [data[1], data[2]]
        return {
            'options': characteristics_dict,
            'skils': self.get_skills(),
            'inventory': self.get_inventory(),
            'default_age': self.get_default_age(),
            'default_story': self.get_default_stories()
        }
        

    def get_classes(self):
        return read_json_file('json_data\main_constructor.json')['Classes']
    
    def set_class(self, char_class: str):
        if char_class == 'random':
            char_class = random.choice(list(classes.keys()))
        self.player_list['character_class'] = char_class
        print(f'Выбран класс: {char_class}')
        
        self.__class_data = self.supabase.get_class_data_by_name(classes[self.player_list['character_class']])

    def get_races(self):
        return read_json_file('json_data\main_constructor.json')['Races']
    
    def get_subraces(self):
        return self.__race_data["race"]['subraces']
    
    def get_recomended_races(self):
        return read_json_file('json_data\main_constructor.json')['Races']
    
    def set_race(self, char_race: str):
        if char_race == 'random':
            char_race = random.choice(list(races.keys()))
        self.player_list['race'] = char_race
        
        print(f'Выбрана раса: {char_race}')
        self.__race_data = self.supabase.get_race_data_by_name(races[self.player_list['race']])
        #self.set_subrace('random') #!!!!!!!!!!!!!!!!!!!!!!!! УДАЛИТЬ ПОСЛЕ ДОБАВЛЕНИЯ ВОПРОСА В АЙОГРАММ (пока стоит на рандоме)
        
    def set_subrace(self, subrace: str):
        if self.get_subraces() != []:
            if subrace == 'random':
                subrace = random.choice(self.get_subraces())
            self.__subrace_data = subrace
            self.player_list['subrace'] = subrace['name']
            
            print(f'Выбрана подраса: {subrace["name"]}')
        
        
    def get_characteristics(self):
        global CHARACTERISTICS_TRANSLATE
        target_characteristic = next((k for k, v in self.player_list['stats'].items() if v is None), None)
        
        if target_characteristic == None: return None, None, None
        
        recomended_str = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Рекомендуемые характеристики"][CHARACTERISTICS_TRANSLATE[target_characteristic]]
        
        recomended_min, recomended_max = list(map(int, recomended_str.split('-')))
        recomended_btns = list(map(str, range(8, min(16, recomended_max + 3))))
        
        recomended_btns = list(filter(lambda x: (9 if int(x) == 15 else int(x) - 8) <= self.__characteristic_limit, recomended_btns))
        recomended_to_class = list(map(str, list(range(recomended_min, recomended_max + 1))))
        self.__last_characteristic_variants = recomended_btns
        return CHARACTERISTICS_TRANSLATE[target_characteristic], recomended_btns, recomended_to_class
    
    def set_characteristics(self, characteristics):
        if characteristics == 'random':
            characteristics = random.choice(self.__last_characteristic_variants)
        target_characteristic = next((k for k, v in self.player_list['stats'].items() if v is None), None)
        self.__characteristic_limit -= 9 if int(characteristics) == 15 else int(characteristics) - 8
        
        exec(f"self.player_list['stats']['{target_characteristic}'] = {int(characteristics)}")
        
        if self.player_list['stats']['charisma'] != None:
            self.set_modifiers() # от статов
            self.set_hits() # от класса
            self.set_race_characteristics_bonuces() # от расы
        
        print(f'Выбрана: {target_characteristic}, значение: {characteristics}')

    def add_skill(self, skill):
        if skill == 'random':
            skills_list = read_json_file('json_data\class_constructor.json')["Classes"][self.player_list["character_class"]]["Навыки"]["Список"]
            for s in self.player_list["skills"]:
                
                skills_list.remove(s)
            
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
        weapon_file = self.supabase.get_weapon_data()
        for i in item.split(' + '):
            item_count = 1
            
            if '(' in i: 
                item_count = int(i[i.find('(') + 1:-1])
                i = i[:i.find('(')]
            
            if i in weapon_file["weapons"].keys():
                self.player_list["weapons_and_equipment"][i] = weapon_file["weapons"][i]
                if item_count > 1:
                    self.player_list["weapons_and_equipment"][i]['Кол-во'] = item_count
            elif i in weapon_file['armor'].keys():
                self.player_list["weapons_and_equipment"][i] = weapon_file['armor'][i]
            else:
                self.player_list['inventory'].append(f'{i}({item_count})' if item_count > 1 else i)
                
        self.inventory_counter += 1
        for j in self.player_list["weapons_and_equipment"]:
            if j not in weapon_file["armor"]:
                self.player_list["attack_and_damage_values"][j] = weapon_file["weapons"][j]
                
    def set_initialize_default_values(self):
        #от класса
        self.set_saving_throws()
        self.set_passive_persception()
        self.set_class_features()
        
        #от расы
        self.set_speed()
        self.set_languages()
        self.set_worldview()
        self.set_backstory()
        self.set_race_traits()
        
    def set_final_default_values(self):
        '''Финальная установка значений не требующих выбора'''
        
        #от статов
        self.set_modifiers()
        
        #от класса
        self.set_hits()
        
        #от расы
        self.set_race_characteristics_bonuces()
        
        
    def set_gender(self, gender):
        if gender == 'male':
            gender = 'Мужской'
        elif gender == 'female':
            gender = 'Женский'
        else:
            gender = random.choice(['Мужской', 'Женский'])
        self.player_list['gender'] = gender
        print(f'Выбран гендер: {gender}')

    def set_name(self, name):
        if name == 'random':
            if self.player_list['gender'] == 'Мужской':
                names = self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['man_names']
            else:
                names = self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['woman_names']

            name = random.choice(names)
        self.player_list['name'] = name
        print(f'Выбрано имя: {name}')
        
    def get_default_names(self, gender: str):
        if gender == 'Мужской':
            return self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['man_names']
        if gender == 'Женский':
            return self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['woman_names']
        return self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['man_names'] + self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['woman_names']

    def set_story(self, story):
        if story == 'random':
            story = random.choice(self.supabase.get_lore_data()['races'][races[self.player_list['race']]])
        print(f'Выбрана предыстория: {story}')
        
    def get_default_stories(self):
        return self.supabase.get_lore_data()['races'][races[self.player_list['race']]]

    def set_age(self, age):
        if age == 'random':
            range = self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['age']
            age = random.randint(range['min'], range['max'])

        self.player_list['age'] = age
        print(f'Выбран возраст: {age}')
        
    def get_default_age(self):
        return self.supabase.get_race_data_by_name(races[self.player_list['race']])['race']['age']

    
    def set_saving_throws(self):
        #saving_throws
        saving_throws = self.__class_data['class']["saving_throws"]
        for i in saving_throws:
            self.player_list["ability_saving_throws"][i] = self.player_list["stat_modifiers"][i] + self.player_list['ownership_bonus']

    def set_hits(self):
        hit_dice = self.__class_data["class"]["hit_dice"].split('d')
        health_points = int(hit_dice[1]) + int(self.player_list["stat_modifiers"]["constitution"])
        self.player_list["hp"] = health_points
        
    def set_passive_persception(self):
        passive_perception = 10 + self.player_list["stat_modifiers"]["wisdom"]
        if 'восприятие' in self.player_list['skills']:
            passive_perception += self.player_list['ownership_bonus']
        self.player_list["passive_perception"] = passive_perception
        
    def set_speed(self):
        self.player_list['speed'] = self.__race_data['race']["speed"]["walk"]
        
    def set_languages(self):
        self.player_list["languages"]  = self.__race_data["race"]["languages"] 
        
    def set_modifiers(self):
        stats_modifiers = self.player_list["stat_modifiers"]
        stats = self.player_list["stats"]
        for i in stats.keys():
            stats_modifiers[i] = (stats[i] - 10)//2
        self.player_list["stat_modifiers"] = stats_modifiers
        
    def set_worldview(self):
        keys = []
        for j in self.__race_data["race"]["worldview"].keys():
            keys.append(j)
        random.shuffle(keys)
        self.player_list["worldview"] = self.__race_data["race"]["worldview"][keys[0]]
        
    def set_backstory(self):
        race = races[self.player_list['race']]
        lore_file = self.supabase.get_lore_data()
        self.player_list["backstory"] = lore_file["races"][race][random.randint(0,len(lore_file["races"][race])-1)]
        
    def set_race_traits(self):
        subraces = self.__race_data["race"]['subraces']
        subrace = random.choice(subraces) if subraces != [] else []
        traits = self.__race_data["race"]["traits"]
        if subrace != []:
            subrace_traits = subrace["traits"]
            for j in subrace_traits:
                traits.append(j)      

        for i in traits:
            keys = []
            for j in i.keys():
                keys.append(j)
            self.player_list["traits_and_abilities"][i[keys[0]]] = i[keys[1]]
            
    def set_class_features(self):
        traits = dict()
        for i in range(1, self.player_list['lvl']):
            traits[i] = self.__class_data["class"]["features_by_level"][str(i)]
        self.player_list["class_features"] = traits
        
    def generate_random_char(self):
        self.set_class('random')
        self.set_race('random')
        while 1:
            _, __, ___ = self.get_characteristics()
            if _ == None:
                break
            self.set_characteristics('random')


        skills_limit = self.get_skills()['skills_limit']

        for i in range(skills_limit):
            self.add_skill('random')


        return self.player_list

    def set_race_characteristics_bonuces(self):
        all_bonuces = dict()
        for i in list(self.__race_data['race']['ability_bonuses'].keys()):
            all_bonuces[i] = self.__race_data['race']['ability_bonuses'][i]
        if self.__subrace_data != dict():
            for i in list(self.__subrace_data['ability_bonuses']):
                all_bonuces[i] = self.__subrace_data['ability_bonuses'][i]
        for i in list(all_bonuces.keys()):
            self.player_list['stats'][i] += all_bonuces[i]
            
    def get_weapon_group(self, group: str):
        return self.supabase.get_weapon_data['weapon_types'][group]
