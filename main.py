from fastapi import FastAPI
from pydantic import BaseModel
import json
import random
from db_source import DBSource

clases = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Маг":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

supabase = DBSource('https://supabase.questhub.pro/',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzMwMzIyMDAwLAogICJleHAiOiAxODg4MDg4NDAwCn0.oaSCoTPKV6H1XJ_7eWgl67oxnfav4KnNXu8KUkNROJs")
supabase.connect()

with open('player.json', 'r', encoding="utf-8") as player_list: 
        player_list = json.load(player_list)




app = FastAPI()



class Create(BaseModel):
    gender: str
    rac: str
    clas: str

@app.post("/register/")
async def register_user(gender: str, rac: str, clas: str):
    return choose(gender, rac, clas)



def choose(gender: str, rac: str, clas: str):
    # print(f"choose male:(M/F)")
    # gender = input()

    # print(f"choose race:")
    # for i in races.keys():
        # print(i)
    rac = races[rac]
    race_file = supabase.get_race_data_by_name(rac)
    # with open(f'race/{rac}.json', 'r', encoding="utf-8") as race_file: 
    #     race_file = json.load(race_file)
    subrace = race_file["race"]['subraces']
    if subrace != []:
        random.shuffle(subrace)
        subrace = subrace[0]
        player_list["race"] = subrace['name']
    else:
         player_list["race"] = race_file["race"]['name']
    if gender == 'M':
         names = race_file["race"]["man_names"]
    else:
         names = race_file["race"]["woman_names"]
    random.shuffle(names)
    player_list["name"] = names[0]

    #surnames
    surnames = race_file["race"]["woman_names"]
    random.shuffle(surnames)
    player_list["surname"] = surnames[0]


    #age
    race_file['race']["age"]
    player_list['age'] = random.randint(race_file['race']["age"]['min'],race_file['race']["age"]['max'])


    # print(f"choose class:")
    # for i in race_file['class_options']:
    #     print(i)
    clas = clases[clas]
    class_file = supabase.get_class_data_by_name(clas)
    # with open(f'classes/{clas}.json', 'r', encoding="utf-8") as class_file: 
    #     class_file = json.load(class_file)
    subclass = class_file["class"]['subclasses']
    random.shuffle(subclass)
    subclass = subclass[0]
    player_list["class"] = class_file["class"]["name"]

    #stats:
    primary_ability = class_file["class"]["primary_ability"]
    stats = player_list["stats"]
    values = [15,14,13,12,10,8]
    max_values = []
    for i in range(len(primary_ability)):
         max_values.append(values.pop(0))
    random.shuffle(values)
    a = 0 
    for i in stats.keys():
         if i not in primary_ability:
              stats[i] = values[a]
              a+=1
    for i in primary_ability:
         stats[i] = max_values[0]
         max_values.pop(0) 
    ability_bonuses = race_file["race"]["ability_bonuses"]
    for i in ability_bonuses.keys():
         stats[i] += ability_bonuses[i]
    if subrace != []:
        ability_bonuses = subrace["ability_bonuses"]
    for i in ability_bonuses.keys():
         stats[i] += ability_bonuses[i]


    #stat_modifiers 
    stats_modifiers = player_list["stats_modifiers"]
    for i in stats.keys():
        stats_modifiers[i] = (stats[i] - 10)//2
    player_list["stats"] = stats
    player_list["stats_modifiers"] = stats_modifiers

    #saving_throws
    saving_throws = class_file["class"]["saving_throws"]
    for i in saving_throws:
         player_list["saving_throws"][i] = player_list["stats_modifiers"][i]

    #умения
    traits = race_file["race"]["traits"]
    if subrace != []:
        subrace_traits = subrace["traits"]
        for j in subrace_traits:
            traits.append(j)      

    for i in traits:
        keys = []
        for j in i.keys():
            keys.append(j)
        player_list["traits_and_abilities"][i[keys[0]]] = i[keys[1]]

    #Health_points
    hit_dice = class_file["class"]["hit_dice"].split('d')
    health_points = random.randint(1,int(hit_dice[1])) + player_list["stats_modifiers"]["constitution"]
    player_list["health_points"] = health_points
    
    #speed
    player_list['travel_speed'] = race_file['race']["speed"]["walk"]

    #skills
    player_list["skills"] = class_file['class']["skills"]

    #master_bonus
    #у первого уровня всегда 2 

    #инициатива
    player_list["initiative"] = player_list["stats_modifiers"]["dexterity"]
     
    #пасивная мудрость
    passive_wisdom = 10 + player_list["stats_modifiers"]["wisdom"]
    if  'восприятие' in player_list['skills']:
         passive_wisdom += player_list['master_bonus']

    #languages
    player_list["languages"]  = race_file["race"]["languages"] 


    #attack and damage
    class_file = supabase.get_race_data_by_name(clas)
    weapon_file = supabase.get_weapon_data()
    # with open(f'weapon.json', 'r', encoding="utf-8") as weapon_file: 
    #     weapon_file = json.load(weapon_file) 
    for i in  player_list["weapons"]:
        if i not in weapon_file["armor"]:
            player_list["attack_and_damage_values"][i] = weapon_file["weapons"][i]

    #weapons
    weapon = race_file["starting_equipment"]["weapons"][random.randint(0,len(race_file["starting_equipment"]["weapons"])-1)]
    player_list["weapons"][weapon] = weapon_file["weapons"][weapon]

    spells_file = supabase.get_spells_data()
    # with open(f'spells.json', 'r', encoding="utf-8") as spells_file: 
    #     spells_file = json.load(spells_file) 

    if rac in spells_file["races"].keys():
         player_list["spells_and_magic"] = spells_file["races"][rac]
         
    if subrace != []:
        if subrace["name"] in spells_file["races"].keys():
            player_list["spells_and_magic"] = spells_file["races"][subrace["name"]]

    if clas in spells_file["classes"].keys():
         player_list["spells_and_magic"] = spells_file["classes"][clas]
    # for i in  player_list["spells_and_magic"].keys():
    #     player_list["attack_and_damage_values"][i]  = spells_file["spells"][i] 

    #spells


    #inventory
    armor = race_file["starting_equipment"]["armor"]
    random.shuffle(armor)


    player_list["weapons"][armor[0]] = weapon_file["armor"][armor[0]]

    player_list["attack_and_damage_values"][armor[0]] = weapon_file["armor"][armor[0]]

    keys = []
    for j in race_file["starting_equipment"]["packs"].keys():
        keys.append(j)
    random.shuffle(keys)
    for i in race_file["starting_equipment"]["packs"][keys[0]]:
         player_list["inventory"].append(i)
    tools = race_file["starting_equipment"]["tools"]
    random.shuffle(tools)
    player_list["inventory"].append(tools[0])
         
    #worldview
    keys = []
    for j in race_file["race"]["worldview"].keys():
        keys.append(j)
    random.shuffle(keys)
    player_list["worldview"] = race_file["race"]["worldview"][keys[0]]
    

    #backstory
    lore_file = supabase.get_lore_data()
    # with open(f'lore.json', 'r', encoding="utf-8") as lore_file: 
    #     lore_file = json.load(lore_file) 
    player_list["backstory"] = lore_file["races"][rac][random.randint(0,len(lore_file["races"][rac])-1)]
    # print(weapon_file["armor"])
    return player_list
