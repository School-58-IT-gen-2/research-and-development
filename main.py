import json
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
    names = race_file[""]


    if gender == 'M':
         names = race_file["male_names"]
    else:
         names = race_file["female_names"]
    names.sort()
    player_list["name"] = names[0]
    

    print(f"choose class:")
    for i in race_file['class_options']:
        print(i)
    choose = input()
    player_list["class"] = choose
    print(player_list)
    return choose

print(choose())