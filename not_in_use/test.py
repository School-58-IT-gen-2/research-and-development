from fastapi.testclient import TestClient
from collections import defaultdict
import json
import time
import os

# from rnd_fastapi_server import app, choose

# # Создаём экземпляр TestClient
# client = TestClient(app)

# # gender = ['M', 'W']
# # races = {"Дварф": 'dwarf', "Эльф": 'elves', 'Полурослик': "halfling", 'Человек': "human", 'Драконорожденный': "dragonborn",
# #          'Гном': "gnom", 'Полуэльф': "halfelf", 'Полуорк': "halforc", 'Тифлинг': "tiefling"}

# # keys = list(races.keys())

# # check = defaultdict(int)

# # for g in gender:
# #     for r in keys:
# #         with open(f"race/{races.get(r)}.json", "r", encoding="utf-8") as file:
# #             d = json.load(file)

# #         class_options = d.get('class_options', [])
# #         for c in class_options:
# #             with open('test_player.json', 'r') as f:
# #                 json_data1 = json.load(f)

# #             data = {
# #                 "gender": f"{g}",
# #                 "rac": f"{r}",
# #                 "clas": f"{c}"
# #             }

# #             response = client.post("/register/", params=data)

# #             json_data2 = response.json()

# #             # Сравнение по ключам
# #             keys1 = json_data1.keys()
# #             keys2 = json_data2.keys()

# #             common_keys = set(keys1) & set(keys2)  # пересечение ключей
# #             print(g, r, c)
# #             for key in common_keys:
# #                 if json_data1[key] == json_data2[key]:
# #                     check[key] += 1


# # print(check)
# # print('end')



# # 1

# # time.sleep(4)
# # os.system('cls')
# # print('Первый легкий тест на работоспособность Fast API')
# # time.sleep(5)

# data = {
#     "gender": "W",
#     "rac": "Тифлинг",
#     "clas": "Жрец"
# }

# # Отправляем POST запрос на endpoint /register/
# response = client.post("/register/", params=data)

# # Печатаем статус код и ответ
# print("Response status code:", response.status_code)
# print("Response JSON:", response.json())
# # print('end')






# # time.sleep(10)
# # os.system('cls')
# # print('Второй тест для проверки генерации карточек')
# # time.sleep(5)


# # gender = ['M', 'W']
# # # races = ['dwarf','elves',"halfling","human","dragonborn","gnom","halfelf","halforc","tiefling"]
# # races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

# # keys = list(races.keys())


# # for g in gender:
# #     for r in keys:
# #         with open(f"race/{races.get(r)}.json", "r", encoding="utf-8") as file:
# #             d = json.load(file)

# #         class_options = d.get('class_options', [])
# #         for c in class_options:
# #             for _ in range(5):
# #                 data = {
# #                             "gender": f"{g}",
# #                             "rac": f"{r}",
# #                             "clas": f"{c}"
# #                         }
# #                 response = client.post("/register/", params=data)

           
# #                 print(response.status_code, g, r, c)
# #             # print(g, r, c)

# # print('end')









# # time.sleep(3)
# # os.system('cls')
# # print('Третий тест на стрессоустойчивость (отправка большого количества идентичных запросов)')
# # time.sleep(5)

# # c = 0
# # for i in range(1001):
# #     c = i
# #     data = {
# #                 "gender": "M",
# #                 "rac": "Дварф",
# #                 "clas": "Воин"
# #             }

# #     # Отправляем POST запрос на endpoint /register/
# #     response = client.post("/register/", params=data)

# #     # Печатаем статус код и ответ
# #     print("Response status code:", response.status_code)

# # print('кол-во запросов:', c)
# # print('end')

import requests

# URL вашего FastAPI сервера
url = "http://localhost:8000/create-character-list"


data = {
    "gender": "M",
    "rac": "Полурослик",
    "clas": "Жрец"
}

# Отправка POST запроса
response = requests.post(url, json=data)

# Проверка ответа
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)






# gender = ['M', 'W']
# # races = ['dwarf','elves',"halfling","human","dragonborn","gnom","halfelf","halforc","tiefling"]
# races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

# keys = list(races.keys())

# start_time = time.time()
# n = 0
# for g in gender:
#     for r in keys:
#         with open(f"C:/Users/Artem/Desktop/RnD/research-and-development/not_in_use/race/{races.get(r)}.json", "r", encoding="utf-8") as file:
#             d = json.load(file)

#         class_options = d.get('class_options', [])
#         if not class_options:
#             print(f"Warning: No class options found in {races.get(r)}.json")
#         for c in class_options:
#             for _ in range(5):
#                 data = {
#                             "gender": f"{g}",
#                             "rac": f"{r}",
#                             "clas": f"{c}"
#                         }
                
#                 response = requests.post(url, json=data)

                
#                 print(response.status_code, g, r, c)
#                 n += 1
#             # print(g, r, c)


# end_time = time.time()

# # Общее время выполнения
# execution_time = end_time - start_time

# # Результат деления времени на n
# print('кол-во секунд на весь тест', execution_time, 'кол-во секунд на один лист', execution_time / n, 'кол-во листов персонажа', n)
# print('end')
