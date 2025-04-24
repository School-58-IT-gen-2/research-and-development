from enum import Enum
from typing import Dict, List, Optional
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
    user_id: Optional[str] = None
    gender: GenderVariants
    character_class: ClassVariants
    race: RacesVariants
    subrace: str = 'random'
    
class StatModifiers(BaseModel):
    strength: int = 0
    dexterity: int = 0
    constitution: int = 0
    intelligence: int = 0
    wisdom: int = 0
    charisma: int = 0

class Stats(BaseModel):
    strength: Optional[int] = None
    dexterity: Optional[int] = None
    constitution: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    charisma: Optional[int] = None

from pydantic import BaseModel
from typing import Optional, Union, Dict, List, Any
import uuid

class Note(BaseModel):
    # Реализация модели Note
    pass

class Item(BaseModel):
    # Реализация модели Item
    pass

class Spell(BaseModel):
    # Реализация модели Spell
    pass

class TraitsAndAbilities(BaseModel):
    # Реализация модели TraitsAndAbilities
    pass

class StatModifiers(BaseModel):
    # Реализация модели StatModifiers
    pass

class Stats(BaseModel):
    # Реализация модели Stats
    pass

class CharacterRequest(BaseModel):
    """Объединенная модель персонажа"""
    # Поля из первой модели
    id: Optional[Union[str, uuid.UUID]] = None
    race: Optional[str] = None
    character_class: Optional[str] = None
    backstory: Optional[str] = None
    notes: Optional[Union[Note, str]] = None  # Объединенный тип
    hp: Optional[int] = None
    initiative: Optional[int] = None
    lvl: Optional[int] = None
    passive_perception: Optional[int] = None
    speed: Optional[int] = None
    experience: Optional[int] = None
    ownership_bonus: Optional[int] = None
    ability_saving_throws: Optional[Dict[str, Any]] = None
    death_saving_throws: Optional[int] = None
    interference: Optional[bool] = None
    advantages: Optional[bool] = None
    weapons_and_equipment: Optional[Union[List[Item], Dict]] = None  # Объединенный тип
    spells: Optional[Union[List[Spell], Dict]] = None  # Объединенный тип
    traits_and_abilities: Optional[Union[List[TraitsAndAbilities], Dict]] = None  # Объединенный тип
    languages: Optional[List[Any]] = None
    special_features: Optional[Dict[str, Any]] = None
    weaknesses: Optional[Dict[str, Any]] = None
    npc_relations: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    gold: Optional[int] = None
    skills: Optional[List[Any]] = None
    stat_modifiers: Optional[Union[Dict[str, Any], StatModifiers]] = None  # Объединенный тип
    stats: Optional[Union[Dict[str, Any], Stats]] = None  # Объединенный тип
    user_id: Optional[str] = None
    inspiration: Optional[bool] = True
    surname: Optional[str] = None
    inventory: Optional[List[Item]] = None
    age: Optional[int] = None
    worldview: Optional[str] = None
    subrace: Optional[str] = None
    gender: Optional[str] = None
    archetype: Optional[str] = None
    fighting_style: Optional[str] = None
    created_at: Optional[str] = None

    # Поля из второй модели с сохранением имен
    diary: Optional[str] = None
    class_features: Optional[Dict] = None
    valuables: Optional[Dict] = None
    attack_and_damage_values: Optional[Dict] = None
    travel_speed: Optional[int] = None