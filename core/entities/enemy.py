from core import *
from core.battle import *
from yaml import load


class Enemy(object):

    def __init__(self, type_: str, class_: str, name: str, max_hp: int, hp: int,
                 max_mp: int, mp: int, strength: int, defense: int, magic: int,
                 magic_defense: int, speed: int, resistance: list, elem_resistance: list,
                 elem_absorb: list, elem_weak: list, attacks: list, script: dict):
        self.type_ = type_
        self.class_ = class_
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.max_mp = max_mp
        self.mp = mp
        self.strength = strength
        self.defense = defense
        self.magic = magic
        self.magic_defense = magic_defense
        self.speed = speed
        self.resistance = resistance if resistance is not [] else None
        self.elem_resistance = elem_resistance if elem_resistance is not [] else None
        self.elem_absorb = elem_absorb if elem_absorb is not [] else None
        self.elem_weak = elem_weak if elem_weak is not [] else None
        self.attacks = attacks
        self.script = script

    @staticmethod
    def read_and_deserialize_yml(path: str = ""):
        with open(path) as file:
            content = load(file.read())["monster"]

        attacks = []
        for attack in content["attacks"]:
            attack = attack["attack"]
            effects = []
            for effect in attack["eff"]:
                effect = effect["effect"]
                effects.append(AttackEffect(effect["type"], effect["args"]))
            attacks.append(Attack(attack["name"],
                                  attack["key"],
                                  attack["dmg"],
                                  attack["acc"],
                                  attack["cost"],
                                  effects))

        return Enemy(content["type"],
                     content["class"],
                     content["name"],
                     content["stats"]["hp"],
                     content["stats"]["hp"],
                     content["stats"]["mp"],
                     content["stats"]["mp"],
                     content["stats"]["str"],
                     content["stats"]["def"],
                     content["stats"]["mag"],
                     content["stats"]["mgdf"],
                     content["stats"]["spd"],
                     content["stats"]["resist"].split(),
                     content["stats"]["elem_resist"].split(),
                     content["stats"]["elem_absorb"].split(),
                     content["stats"]["elem_weak"].split(),
                     attacks,
                     content["script"])

