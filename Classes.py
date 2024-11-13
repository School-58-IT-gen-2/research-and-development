class MainInfo():
    def __init__(self):
        pass
    name = ""
    category = "" #класс
    level = 1
    race = ""
    worldview = ""


class Characteristic():
    def __init__(self):
        #здесь делаем распределение наших очков,от туда узнаем модификаторы и спасброски(еще зависят от рассы)
        pass
    STR = 10
    DEX = 10
    CON = 10
    INT = 10
    WIS = 10
    CHA = 10
    master_bonus = 2
    modSTR = 0 
    modDEX = 0
    modCON = 0
    modINT = 0
    modWIS = 0
    modCHA = 0
    saving_throws = {}
    saving_throws_death = 0

class Abilities():
    def __init__(self):
        pass
    skills = []
    combat_abilities = []
    special_features = []

class PointsAndHealth():
    def __init__(self):
        pass
    health_points = 1
    health_cubes = 1
    experience_points = 1

class DefenseAndAttack():
    def __init__(self):
        pass
    AC = 0
    initiative = 0
    movement_speed = 1
    AttacksAndSpells = {}

class EquipmentAndInventory():
    def __init__(self):
        pass
    weapons_and_armor = []
    items_and_supplies = []
    money = 0

class PrehistoryAndPersonality():
    def __init__(self):
        pass
    traits = []
    moral_values = []
    history_and_origin = []
    weaknesses_and_disadvantages = []
class AdditionalInformation():
    def __init__(self):
        pass
    languages = []
    features_and_traits = []

