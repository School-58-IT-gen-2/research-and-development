import json


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


class CharConstructor:
    def __init__(self):
        self.char_class = None

    def get_classes(self):
        return read_json_file('json_data\main_constructor.json')['Classes']
    
    def set_class(self, char_class: str):
        self.char_class = char_class

