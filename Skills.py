from typing import Optional

from Dice import *
from __future__ import annotations

default_level_modifiers = {0:-2, 1:0, 2:1, 3:3, 4:8, 5:15} # level : modifier
proficiency_levels = {}
def mutable(parameter, default_val):
    if parameter is None:
        return default_val
    else:
        return parameter
class Skill:
    def __init__(self, idd, level=0, nickname=None, base_effect=0,
                 roll=None, description=""):
        """
        The most basic skill. Only base attack, only physical, no mana involved.
        :param idd: The 'official' name of the skill, key in the database. Format name-level eg fireball-3
        :param level: The proficiency level of the skill. Effects of proficiency in default_level_modifiers
        :param nickname: What the player chooses to call the skill. Eg 'Hot-ball'
        :param base_effect: base attack/healing points, increases with proficiency
        :param roll: [max roll, times] eg 4d6 = [6,4]
        :param description: optional, eg 'small ball of fire'

        Future plans:
        next_level: The evolutionary successor to this skill. Eg fireball->flamethrower
        type: magic/physical/psychic
        per_turn: effect inflicted per turn
        turns: number of turns <per_turn> takes effect
        """
        # next_level:Optional[Skill]=None

        self.idd = idd
        self.level = level
        if nickname is None:
            self.nickname = idd.split("-")[0]
        else:
            self.nickname = nickname

        self.base_effect = base_effect #
        self.roll = mutable(roll, [0,0])
        self.description = description

        # dex+d20 > 100-accuracy = hit
        # self.next_level = next_level # another skill which is an evolution of this skill
    def get_combat_stats(self):
        return self.base_effect, self.roll

    def use_skill(self, user, target):# Character/Enemy/NPC
        pass

    def evolve_skill(self):
        if self.level >= 5:
            print("You have reached max level.")
            return
        print("You have reached the next proficiency level")
        new_level = self.level+1
        new_nickname = ''
        if new_level >= 3:
            new_nickname = input("Name your evolved skill?")

        if new_nickname:
            self.nickname = new_nickname
        idd = self.idd.split("-")
        self.idd = idd + str(new_level)
        self.base_effect -= default_level_modifiers[self.level]
        self.base_effect += default_level_modifiers[new_level]

        self.level += 1

        # if self.next_level is None:
        #     print("You have reached the next proficiency level")
        #     if self.level>4:
        #         nickname = input("Name your evolved skill?")
        #
        #         if not nickname:
        #             return Skill(idd=self.nickname+str(self.level+1), level=self.level+1, nickname=self.nickname,
        #                          next_level=None, base_effect=self.base_effect+default_level_modifiers[self.level+1],
        #                          roll=self.roll, description=self.description
        #                          )
        #         else:
        #             return Skill()
        #
        # elif self.next_level == "Final":
        #     print("Max level achieved")
        # else:
        #     print(f'Your level {self.level }{self.name} skill evolved into level {self.level+1}
        #     {self.next_level.name}')
        #     return self.next_level
    def print_proficiency_levels(self):
        """
        0 - 2: -5
        3 - 20: + 0
        20 - 100: + 1
        100 - 300: + 3
        300-1000: +8
        1000+:+15

        :return:
        """
        pass


"""
types of attack needs to be extendable

skill 

physical magical psychic 
base  bleeding  base bleeding

OR 

skill
base bleeding 
physical magical psychic     physical magical psychic

OR 

Skill (basic)
id, level, nickname, next_level, base_effect, roll, description

BleedingSkill 

Skill AND effect_per_turn, turns

MagicSkill 
Skill AND mp_cost, type="magic"


"""

# class PhysicalAttack(Skill):
#     def __init__(self, name, target):
#         super().__init__(name, target, mp_cost=0)
# class MagicalAttack(Skill):