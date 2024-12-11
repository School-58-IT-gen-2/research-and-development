from fastapi.testclient import TestClient
from collections import defaultdict
import json
from main import app, choose

# Создаём экземпляр TestClient
client = TestClient(app)

gender = ['M', 'W']
races = {"Дварф": 'dwarf', "Эльф": 'elves', 'Полурослик': "halfling", 'Человек': "human", 'Драконорожденный': "dragonborn",
         'Гном': "gnom", 'Полуэльф': "halfelf", 'Полуорк': "halforc", 'Тифлинг': "tiefling"}

keys = list(races.keys())

check = defaultdict(int)

for g in gender:
    for r in keys:
        with open(f"race/{races.get(r)}.json", "r", encoding="utf-8") as file:
            d = json.load(file)

        class_options = d.get('class_options', [])
        for c in class_options:
            with open('test_player.json', 'r') as f:
                json_data1 = json.load(f)

            data = {
                "gender": f"{g}",
                "rac": f"{r}",
                "clas": f"{c}"
            }

            response = client.post("/register/", params=data)

            json_data2 = response.json()

            # Сравнение по ключам
            keys1 = json_data1.keys()
            keys2 = json_data2.keys()

            common_keys = set(keys1) & set(keys2)  # пересечение ключей

            for key in common_keys:
                if json_data1[key] == json_data2[key]:
                    check[key] += 1


print(check)
print('end')



# 4

# gender = ['M', 'W']
# # races = ['dwarf','elves',"halfling","human","dragonborn","gnom","halfelf","halforc","tiefling"]
# races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

# keys = list(races.keys())


# for g in gender:
#     for r in keys:
#         with open(f"race/{races.get(r)}.json", "r", encoding="utf-8") as file:
#             d = json.load(file)

#         class_options = d.get('class_options', [])
#         for c in class_options:
#             for _ in range(5):
#                 data = {
#                             "gender": f"{g}",
#                             "rac": f"{r}",
#                             "clas": f"{c}"
#                         }
#                 response = client.post("/register/", params=data)

           
#                 print(response.status_code, g, r, c)
#             # print(g, r, c)

# print('end')


# 3

# for i in range(10000):
#     print(i)
#     data = {
#                 "gender": "M",
#                 "rac": "Дварф",
#                 "clas": "Воин"
#             }

#     # Отправляем POST запрос на endpoint /register/
#     response = client.post("/register/", params=data)

#     # Печатаем статус код и ответ
#     print("Response status code:", response.status_code)



# 1

# Определяем тестовые данные (пользовательские параметры)
# data = {
#     "gender": "M",
#     "rac": "Дварф",
#     "clas": "Воин"
# }

# # Отправляем POST запрос на endpoint /register/
# response = client.post("/register/", params=data)

# # Печатаем статус код и ответ
# print("Response status code:", response.status_code)
# print("Response JSON:", response.json())




