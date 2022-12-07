from typing import Optional

from Dice import *
from __future__ import annotations

def mutable(parameter, default_val):
    if parameter is None:
        return default_val
    else:
        return parameter
class Skill:
    def __init__(self, idd, name=None, next_level:Optional[Skill]=None, base_attack=0, roll=None, per_turn=0, turns=1, delay=0, mp_cost=0,
                 hp_cost=0, accuracy=None, description=""):

        self.idd = idd # name-level eg fireball-3
        if name is None:
            self.name = idd
        else:
            self.name = name

        self.base_attack = base_attack #
        self.roll = mutable(roll, [0,0])
        self.per_turn = per_turn
        self.turns = turns
        self.delay = delay
        self.mp_cost = mp_cost
        self.hp_cost = hp_cost
        self.accuracy = accuracy # dex+d20 > 100-accuracy = hit
        self.next_level = next_level # another skill which is an evolution of this skill
        self.description = description

    def print_proficiency_levels(self):
        """
        0 - 1: -2
        2 - 5: + 1
        5 - 10: + 3
        10 - 50: + 4
        >50: +8

        :return:
        """
        pass

    def use_skill(self, user, target):# Character/Enemy/NPC
        if self.accuracy:
            pass

    def evolve_skill(self):
        if self.next_level is None:
            print("You have reached the next proficiency level")
            if level>4:
                print("Name your evolved skill?")
                if not inputt:
                    return Skill()

        elif self.next_level == "Final":
            print("Max level achieved")
        else:
            print(f'Your level {self.level }{self.name} skill evolved into level {self.level+1} {self.next_level.name}')
            return self.next_level




class PhysicalAttack(Skill):
    def __init__(self, name, target):
        super().__init__(name, target, mp_cost=0)