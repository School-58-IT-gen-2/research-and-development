import json
import random
clases = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Маг":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halfork",'Тифлинг':"tiefling"}

with open('player.json', 'r', encoding="utf-8") as player_list: 
        player_list = json.load(player_list)
def choose():
    print(f"choose male:(M/F)")
    gender = input()

    print(f"choose race:")
    for i in races.keys():
        print(i)
    rac = races[input()]
    with open(f'race/{rac}.json', 'r', encoding="utf-8") as race_file: 
        race_file = json.load(race_file)
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


    #age
    race_file['race']["age"]
    player_list['age'] = random.randint(race_file['race']["age"]['min'],race_file['race']["age"]['max'])


    print(f"choose class:")
    for i in race_file['class_options']:
        print(i)
    clas = clases[input()]

    with open(f'classes/{clas}.json', 'r', encoding="utf-8") as class_file: 
        class_file = json.load(class_file)
    subclass = class_file["class"]['subclasses']
    random.shuffle(subclass)
    subclass = subclass[0]
    player_list["class"] = subclass['name']

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


    #death_saving_throws
    #по дефолту 0


    #умения
    traits = race_file["race"]["traits"]
    if subrace != []:
        subrace_traits = subrace["traits"]
        for j in subrace_traits:
            traits.append(j)      
    for i in traits:
        player_list["traits_and_abilities"].append(i)

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

    #spells
    for i in class_file["class"]["spells"]:
           keys = []
           for j in i.keys():
                keys.append(i[j])
           player_list["spells_and_magic"][keys[0]] = keys[1]

    #weapons
    player_list["weapons"].append(race_file["starting_equipment"]["weapons"][random.randint(0,len(race_file["starting_equipment"]["weapons"])-1)])

    
    #attack and damage
    with open(f'weapon.json', 'r', encoding="utf-8") as weapon_file: 
        weapon_file = json.load(weapon_file) 
    for i in  player_list["weapons"]:
        player_list["attack_and_damage_values"][i] = weapon_file["weapons"][i]


    with open(f'spells.json', 'r', encoding="utf-8") as spells_file: 
        spells_file = json.load(spells_file) 

    if rac in spells_file["races"].keys():
         player_list["spells_and_magic"] = spells_file["races"][rac]

    if clas in spells_file["races"].keys():
         player_list["spells_and_magic"] = spells_file["classes"][clas]
    # for i in  player_list["spells_and_magic"].keys():
    #     player_list["attack_and_damage_values"][i]  = spells_file["spells"][i] 


    #inventory
    armor = race_file["starting_equipment"]["armor"]
    random.shuffle(armor)
    player_list["inventory"].append(armor[0])
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
    

    return player_list

print(choose())