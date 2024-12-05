import requests
import random
import json
import os

url = 'http://127.0.0.1:8000/create_character'

# Словарь с расами и соответствующими файлами JSON
races = {
    "Дварф": 'dwarf.json', "Эльф": 'elves.json', 'Полурослик': "halfling.json", 
    'Человек': "human.json", 'Драконорожденный': "dragonborn.json", 
    'Гном': "gnom.json", 'Полуэльф': "halfelf.json", 'Полуорк': "halforc.json", 
    'Тифлинг': "tiefling.json"
}

genders = ['M', 'W']

# Путь к директории, где хранятся файлы JSON
json_directory = "race"  # Замените на путь к директории с вашими JSON файлами

# Получаем данные из файла расы
def get_race_data(race_filename):
    file_path = os.path.join(json_directory, race_filename)  # Полный путь к файлу
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)  # Загружаем и возвращаем JSON данные
    else:
        print(f"Файл для расы не найден: {file_path}")
        return None

# Перебор всех комбинаций пола, рас и классов
for gender in genders:
    for race, race_filename in races.items():
        race_data = get_race_data(race_filename)
        
        if race_data:
            # Извлекаем доступные классы из данных о расе
            available_classes = race_data.get("class_options", [])
            
            # Для каждого доступного класса отправляем запрос
            for character_class in available_classes:
                data = {
                    'gender': gender,
                    'race': race,
                    'character_class': character_class
                }

                response = requests.post(url, json=data)

                if response.status_code != 200:
                    print(f"{response.status_code}:{data}")


data = {
    'gender': 'M',        
    'race': 'Человек',       
    'character_class': 'Воин' 
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print(response.json()) 
else:
    print('123')

player = [
    "name","race","class","worldview","age","health_points","initiative","level","passive_wisdom","travel_speed","experience","ownership_bonus","death_saving_throws","inspiration","interference","advantages","stats","stats_modifiers","saving_throws","weapons","inventory","spells_and_magic","traits_and_abilities","languages","combat_abilities","weaknesses","attack_and_damage_values","relationships_with_npcs","valuables","skills"
]


def check_missing_fields(data, required_fields):
    missing_fields = []

    for field in required_fields:
        # Если поле отсутствует или его значение пустое
        if field not in data or data[field] in [None, '', {}, [], False]:
            missing_fields.append(field)
    
    return missing_fields

missing = check_missing_fields(response.json(), player)

if missing:
    print("Следующие поля не заполнены или отсутствуют:")
    for field in missing:
        print(f"- {field}")
else:
    print("Все поля заполнены.")