from fastapi.testclient import TestClient
from main import app, choose  
import json

# Создаём экземпляр TestClient
client = TestClient(app)

gender = ['M', 'W']
# races = ['dwarf','elves',"halfling","human","dragonborn","gnom","halfelf","halforc","tiefling"]
races = {"Дварф":'dwarf',"Эльф":'elves','Полурослик':"halfling",'Человек':"human",'Драконорожденный':"dragonborn",'Гном':"gnom",'Полуэльф':"halfelf",'Полуорк':"halforc",'Тифлинг':"tiefling"}

keys = list(races.keys())


for g in gender:
    for r in keys:
        with open(f"race/{races.get(r)}.json", "r", encoding="utf-8") as file:
            d = json.load(file)

        class_options = d.get('class_options', [])
        for c in class_options:
            for _ in range(5):
                data = {
                            "gender": f"{g}",
                            "rac": f"{r}",
                            "clas": f"{c}"
                        }
                response = client.post("/register/", params=data)

           
                print(response.status_code, g, r, c)
            # print(g, r, c)

print('end')

# 5
# 200 M Дварф Жрец
# 200 M Дварф Воин
# 200 M Дварф Паладин
# 200 M Дварф Следопыт
# 200 M Эльф Следопыт
# 200 M Эльф Маг
# 200 M Эльф Колдун
# 200 M Эльф Бард
# 200 M Эльф Плут
# 9


# 1
# 200 M Дварф Жрец
# 200 M Дварф Воин   
# 200 M Дварф Паладин
# 200 M Дварф Следопыт
# 200 M Эльф Следопыт
# 200 M Эльф Маг     
# 200 M Эльф Колдун
# 200 M Эльф Бард
# 200 M Эльф Плут
# 200 M Полурослик Плут
# 200 M Полурослик Жрец    
# 200 M Полурослик Следопыт
# 200 M Полурослик Монах
# 200 M Человек Воин
# 200 M Человек Жрец
# 200 M Человек Маг
# 200 M Человек Паладин
# 200 M Человек Следопыт
# 200 M Человек Бард
# 19


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




