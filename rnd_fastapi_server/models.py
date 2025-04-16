from enum import Enum
from pydantic import BaseModel

class RacesVariants(str, Enum):
    dwarf = "Дварф"
    elves = "Эльф"
    halfling = 'Полурослик'
    human = 'Человек'
    dragonborn = 'Драконорожденный'
    gnom = 'Гном'
    halfelf = 'Полуэльф'
    halforc = 'Полуорк'
    tiefling = 'Тифлинг'

class ClassVariants(str, Enum):
    pathfinder = 'Следопыт'
    barbarian = "Варвар"
    bard = "Бард"
    dodger = "Плут"
    druid = "Друид"
    magician = "Колдун"
    monk = "Монах"
    paladin = "Паладин"
    priest = "Жрец"
    warlock = "Чародей"
    warrior = "Воин"
    wizzard = "Волшебник"

class GenderVariants(str, Enum):
    M = "M"
    F = "W"

class Create(BaseModel):
    #gender: GenderVariants
    character_class: ClassVariants
    race: RacesVariants
    subrace: str = 'random'