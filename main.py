import json
import random
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}



# Словари для классов и рас, как и в первом файле
clases = {
    'Следопыт': 'pathfinder', "Варвар": "barbarian", "Бард": "bard", 
    "Плут": "dodger", "Друид": "druid", "Колдун": "magician", 
    "Монах": "monk", "Паладин": "paladin", "Жрец": "priest", 
    "Маг": "warlock", "Воин": "warrior", "Волшебник": "wizzard"
}
races = {
    "Дварф": 'dwarf', "Эльф": 'elves', 'Полурослик': "halfling", 
    'Человек': "human", 'Драконорожденный': "dragonborn", 
    'Гном': "gnom", 'Полуэльф': "halfelf", 'Полуорк': "halfork", 
    'Тифлинг': "tiefling"
}

# Загрузка шаблона игрока из файла player.json
with open('player.json', 'r', encoding="utf-8") as player_file:
    player_template = json.load(player_file)

# Функция выбора характеристик персонажа
def choose(gender: str, race: str, character_class: str):
    player_list = player_template.copy()  # Создаем копию шаблона игрока

    # Получение рассы из словаря races
    rac = races.get(race)
    if not rac:
        raise ValueError(f"Некорректная раса: {race}")

    # Загрузка информации о расе из файла
    with open(f'race/{rac}.json', 'r', encoding="utf-8") as race_file: 
        race_file = json.load(race_file)

    subrace = race_file["race"]['subraces']  # Подраса, если есть
    if subrace:
        random.shuffle(subrace)
        subrace = subrace[0]
        player_list["race"] = subrace['name']  # Выбираем случайную подрасу
    else:
        player_list["race"] = race_file["race"]['name']  # Если подрасы нет, выбираем основную расу

    # Выбор имени в зависимости от пола
    names = race_file["race"]["man_names"] if gender == 'M' else race_file["race"]["woman_names"]
    random.shuffle(names)
    player_list["name"] = names[0]

    # Определение возраста персонажа в пределах диапазона
    player_list['age'] = random.randint(race_file['race']["age"]['min'], race_file['race']["age"]['max'])

    # Получение класса из словаря clases
    clas = clases.get(character_class)
    if not clas:
        raise ValueError(f"Некорректный класс: {character_class}")

    # Загрузка информации о классе
    with open(f'classes/{clas}.json', 'r', encoding="utf-8") as class_file: 
        class_file = json.load(class_file)

    # Выбор случайного подкласса
    subclass = class_file["class"]['subclasses']
    random.shuffle(subclass)
    player_list["class"] = subclass[0]['name']

    # Установка значений характеристик
    primary_ability = class_file["class"]["primary_ability"]
    stats = player_list["stats"]
    values = [15, 14, 13, 12, 10, 8]
    max_values = [values.pop(0) for _ in primary_ability]  # Максимальные значения для основных способностей
    random.shuffle(values)
    
    # Распределение значений характеристик
    for key in stats.keys():
        stats[key] = max_values.pop(0) if key in primary_ability else values.pop()

    # Применение бонусов от расы и подрасы
    ability_bonuses = race_file["race"]["ability_bonuses"]
    for key, value in ability_bonuses.items():
        stats[key] += value
    if subrace:
        ability_bonuses = subrace.get("ability_bonuses", {})
        for key, value in ability_bonuses.items():
            stats[key] += value

    # Расчет модификаторов характеристик
    player_list["stats_modifiers"] = {key: (value - 10) // 2 for key, value in stats.items()}
    player_list["stats"] = stats  # Сохраняем обновленные характеристики

    # Определение очков здоровья
    hit_dice = class_file["class"]["hit_dice"].split('d')
    player_list["health_points"] = random.randint(1, int(hit_dice[1])) + player_list["stats_modifiers"]["constitution"]

    # Скорость передвижения
    player_list['travel_speed'] = race_file['race']["speed"]["walk"]

    # Умения персонажа
    player_list["skills"] = class_file['class']["skills"]

    # Языки персонажа
    player_list["languages"] = race_file["race"]["languages"]

    return player_list  # Возвращаем созданного персонажа
