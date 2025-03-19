from enum import Enum
from pydantic import BaseModel

class RacesVariants(Enum):
    dwarf = "Дварф"
    elves = "Эльф"
    halfling = 'Полурослик'
    human = 'Человек'
    dragonborn = 'Драконорожденный'
    gnom = 'Гном'
    halfelf = 'Полуэльф'
    halforc = 'Полуорк'
    tiefling = 'Тифлинг'

class ClassVariants(Enum):
    pathfinder = 'Следопыт'
    barbarian = "Варвар"
    bard = "Бард"
    dodger = "Плут"
    druid = "Друид"
    magician = "Колдун"
    monk = "Монах"
    paladin = "Паладин"
    priest = "Жрец"
    warlock = "Маг"
    warrior = "Воин"
    wizzard = "Волшебник"

class GenderVariants(Enum):
    M = "M"
    F = "W"

class Create(BaseModel):
    gender: GenderVariants
    race: RacesVariants
    character_class: ClassVariants