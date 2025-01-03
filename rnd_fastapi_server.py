
from fastapi import FastAPI
from pydantic import BaseModel
import json
import random
from db_source import DBSource
import uvicorn
from dotenv import load_dotenv
import os
# import tg_bot


clases = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Маг":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}



app = FastAPI()



class Create(BaseModel):
    gender: str
    rac: str
    clas: str


@app.post("/create-character-list")
async def register_user(create: Create):
    return choose(create.gender, create.rac, create.clas)



def choose(gender: str, rac: str, clas: str):
    load_dotenv()
    supabase = DBSource(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))
    supabase.connect()
    player_list = supabase.get_player_data()
    rac = races[rac]
    race_file = supabase.get_race_data_by_name(rac)
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

    clas = clases[clas]
    class_file = supabase.get_class_data_by_name(clas)
    subclass = class_file["class"]['subclasses']
    random.shuffle(subclass)
    subclass = subclass[0]
    player_list["character_class"] = class_file["class"]["name"]

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
    stats_modifiers = player_list["stat_modifiers"]
    for i in stats.keys():
        stats_modifiers[i] = (stats[i] - 10)//2
    player_list["stats"] = stats
    player_list["stat_modifiers"] = stats_modifiers

    #saving_throws
    saving_throws = class_file["class"]["saving_throws"]
    for i in saving_throws:
         player_list["ability_saving_throws"][i] = player_list["stat_modifiers"][i]

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
    health_points = int(hit_dice[1]) + int(player_list["stat_modifiers"]["constitution"])
    player_list["hp"] = health_points
    
    #speed
    player_list['speed'] = race_file['race']["speed"]["walk"]

    #skills
    player_list["skills"] = class_file['class']["skills"]

    #master_bonus
    #у первого уровня всегда 2 

    #инициатива
    player_list["initiative"] = 0
     
    #пасивная мудрость
    passive_perception = 10 + player_list["stat_modifiers"]["wisdom"]
    if  'восприятие' in player_list['skills']:
         passive_perception += player_list['ownership_bonus']
    player_list["passive_perception"] = passive_perception

    #languages
    player_list["languages"]  = race_file["race"]["languages"] 


    #attack and damage
    weapon_file = supabase.get_weapon_data()
    for i in  player_list["weapons_and_equipment"]:
        if i not in weapon_file["armor"]:
            player_list["attack_and_damage_values"][i] = weapon_file["weapons"][i]

    #weapons
    weapon = race_file["starting_equipment"]["weapons"][random.randint(0,len(race_file["starting_equipment"]["weapons"])-1)]
    player_list["weapons_and_equipment"][weapon] = weapon_file["weapons"][weapon]

    spells_file = supabase.get_spells_data()


    if rac in spells_file["races"].keys():
         player_list["spells"] = spells_file["races"][rac]
         
    if subrace != []:
        if subrace["name"] in spells_file["races"].keys():
            player_list["spells"] = spells_file["races"][subrace["name"]]

    if clas in spells_file["classes"].keys():
         player_list["spells"] = spells_file["classes"][clas]
    #inventory
    armor = race_file["starting_equipment"]["armor"]
    random.shuffle(armor)


    player_list["weapons_and_equipment"][armor[0]] = weapon_file["armor"][armor[0]]

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
    player_list["backstory"] = lore_file["races"][rac][random.randint(0,len(lore_file["races"][rac])-1)]
    return player_list
