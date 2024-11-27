import json
import random
classs = {'Следопыт':'pathfinder',"Варвар":"barbarian","Бард":"bard","Плут":"dodger","Друид":"druid","Колдун":"magician","Монах":"monk","Паладин":"paladin","Жрец":"priest","Маг":"warlock","Воин":"warrior","Волшебник":"wizzard"}
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halfork",'Тифлинг':"tiefling"}

with open('player.json', 'r', encoding="utf-8") as player_list: 
        player_list = json.load(player_list)
def choose():
    print(f"choose male:(M/F)")
    gender = input()

    print(f"choose race:")
    for i in races.keys():
        print(i)
    choose = races[input()]
    with open(f'race/{choose}.json', 'r', encoding="utf-8") as race_file: 
        race_file = json.load(race_file)
    subrace = race_file["race"]['subraces']
    random.shuffle(subrace)
    subrace = subrace[0]

    player_list["race"] = subrace['name']
    if gender == 'M':
         names = race_file["race"]["man_names"]
    else:
         names = race_file["race"]["woman_names"]
    random.shuffle(names)
    player_list["name"] = names[0]


    print(f"choose class:")
    for i in race_file['class_options']:
        print(i)
    choose = classs[input()]

    with open(f'classes/{choose}.json', 'r', encoding="utf-8") as class_file: 
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
    print(primary_ability)
    for i in stats.keys():
         if i not in primary_ability:
              print(a)
              print(values)
              stats[i] = values[a]
              a+=1
    for i in primary_ability:
         stats[i] = max_values[0]
         max_values.pop(0) 
    ability_bonuses = race_file["race"]["ability_bonuses"]
    for i in ability_bonuses.keys():
         stats[i] += ability_bonuses[i]
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


    return player_list

print(choose())