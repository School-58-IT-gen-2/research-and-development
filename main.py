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
    player_list["race"] = race_file["race"]['name']

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
         
    ability_boneses = race_file["race"]["ability_bonuses"]
    for i in ability_boneses.keys():
         stats[i] += ability_boneses[i]

    stats_modifiers = player_list["stats_modifiers"]
    for i in stats.keys():
        stats_modifiers[i] = (stats[i] - 10)//2
    player_list["stats"] = stats
    player_list["stats_modifiers"] = stats_modifiers


    return player_list

print(choose())