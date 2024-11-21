import json
import random
races = {"дварф":'dwarf',"эльф":'elves',"p":'Полурослик',"c":'Человек',"d":'Драконорожденный',"g":'Гном',"p":'Полуэльф',"P":'Полуорк',"T":'Тифлинг'}
with open('player.json', 'r', encoding="utf-8") as player_list: 
        player_list = json.load(player_list)
def choose():
    print(f"choose male:(M/F)")
    gender = input()

    print(f"choose race:")
    for i in races.keys():
        print(i)
    choose = races[input()]
    with open(f'{choose}.json', 'r', encoding="utf-8") as race_file: 
        race_file = json.load(race_file)
    subrace = race_file["race"]['subraces']
    random.shuffle(subrace)
    subrace = subrace[0]

    player_list["race"] = subrace['name']
    if gender == 'M':
         names = race_file["race"]["male_names"]
    else:
         names = race_file["race"]["female_names"]
    random.shuffle(names)
    player_list["name"] = names[0]


    print(f"choose class:")
    for i in race_file['class_options']:
        print(i)
    choose = input()
    player_list["class"] = choose
    print(player_list)


    #stats:
    stats = player_list["stats"]
    values = [15,12,13,10,8,14]
    random.shuffle(values)
    a = 0 
    for i in stats.keys():
         stats[i] = values[a]
         a+=1
         
    ability_bonuses = race_file["race"]["ability_bonuses"]
    for i in ability_bonuses.keys():
         stats[i] += ability_bonuses[i]

    ability_bonuses = subrace["ability_bonuses"]
    for i in ability_bonuses.keys():
         stats[i] += ability_bonuses[i]


    stats_modifiers = player_list["stats_modifiers"]
    for i in stats.keys():
        stats_modifiers[i] = (stats[i] - 10)//2
    player_list["stats"] = stats
    player_list["stats_modifiers"] = stats_modifiers

    traits = race_file["race"]["traits"]
    subrace_traits = subrace["traits"]
    for i in subrace_traits.keys():
         traits[i] = subrace_traits[i]


    return player_list

print(choose())