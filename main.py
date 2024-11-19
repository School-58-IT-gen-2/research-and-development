import json
races = {"дварф":'dwarf',"эльф":'elves',"p":'Полурослик',"c":'Человек',"d":'Драконорожденный',"g":'Гном',"p":'Полуэльф',"P":'Полуорк',"T":'Тифлинг'}
def choose():
    print(f"choose race:")
    for i in races.keys():
        print(i)
    choose = races[input()]
    with open(f'{choose}.json', 'r', encoding="utf-8") as race_file: 
        race_file = json.load(race_file)
        print(race_file)
    print(f"choose class:")
    for i in race_file['class_options']:
        print(i)
    choose = input()
    return choose

print(choose())