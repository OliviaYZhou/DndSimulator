import random
from typing import List, Optional, Union
from Dice import *
from Skills import *
from Items import *
stat_indices = {"str": 0, "dex": 1, "con": 2, "int": 3, "wis": 4, "cha": 5}
proficiency_levels = [3, 20, 100, 300, 1000]
exp_levels = {1:0, 2:300, 3:900, 4:2700, 5:6500, 6:14000, 7:23000, 8:34000, 9:48000, 10:64000, 11:85000,
              12:100000, 13:120000, 14:140000, 15:165000, 16:195000, 17:225000, 18:265000, 19:305000, 20:355000}
def rollStats() -> dict:
    stats = [1]*6
    for i in range(6):
        four_d6 = d6(4)
        print(four_d6)
        stats[i] = sum(sorted(four_d6, reverse=True).pop())
    print(stats)
    # TODO choose stats
    return to_stat_dict(stats)
    # return stats

def to_stat_dict(stat_list: List[int]) -> dict:
    """
    Converts stats from list to dict
    :param stat_list: list of stats, [str, dex, con, int, wis, cha]
    :return: dictionary of stats, eg {"str": 0, "dex": 1, "con": 3, "int": 4, "wis": 5, "cha": 6}
    """
    return {
        "str": stat_list[0],
        "dex": stat_list[1],
        "con": stat_list[2],
        "int": stat_list[3],
        "wis": stat_list[4],
        "cha": stat_list[5]
    }

class Character:
    name = ""

    stats = {"str": 0, "dex": 1, "con": 2, "int": 3, "wis": 4, "cha": 5}

    max_hp = 0 # max_hp = hp_rolls + level*con
    hp_rolls = []
    max_mp = 0

    level = 1

    gold = 0

    talent1 = 0
    talent2 = 1

    bag = []
    skills = [] # max skills, skills, used times, proficiency level

    equipped = {"helmet": None, "armor":None, "shoes":None, "weapon": None, "top":None, "bot":None, "accessories":[]}


    temp_stat_modifiers = [0,0,0,0,0,0]
    perm_modifiers = {"hp": 0}

    damage_taken = 0
    mp_used = 0

    race = "Human"
    classType = "Civilian"

    description = ""


    def __init__(self, name: str, stats: Optional[Union[List[int], dict]] = None, exp:int=0, gold:int =50,
                 talent1:str ="str", talent2:str = "dex", bag:List[Item]=None, skills:dict[str:List[Skill,int]]=None,
                 race:str="Human", classType:str="Civilian", description:str = ""):
        """

        :param name:
        :param stats:
        :param exp:
        :param gold:
        :param talent1:
        :param talent2:
        :param bag:
        :param skills: {skillname: [Skill, uses]}
        :param race:
        :param classType:
        :param description:
        """
        self.exp = exp
        self.name = name
        if not stats:
            self.stats = rollStats()
            # TODO ask if roll stats
        elif type(stats) == list:
            self.stats = to_stat_dict(stats)
        elif type(stats) == dict:
            self.stats = stats
        else:
            print("stats format incorrect")
            self.stats = {}
        # [str, dex, con, int, wis, cha]
        self.gold = gold
        self.talent1 = stat_indices[talent1] #TODO offer roll for talent 1
        self.talent2 = stat_indices[talent2]
        self.bag = mutable(bag, [])
        self.skills = mutable(skills, [])
        self.race = race
        self.classType = classType
        self.description = description

    def recalculate_HP(self):
        self.max_hp = sum(self.hp_rolls)+self.stats["con"]*self.level+self.perm_modifiers["hp"]

    def setCon(self, amount):
        self.stats["con"] = amount
        self.recalculate_HP()

    def printStats(self, compare=None):
        if compare:
            print(f"STR: {self.stats['str']}+{compare[stat_indices['str']]}\n"
                  f"DEX: {self.stats['dex']}+{compare[stat_indices['dex']]}\n"
                  f"CON: {self.stats['con']}+{compare[stat_indices['con']]}\n"
                  f"INT: {self.stats['int']}+{compare[stat_indices['int']]}\n"
                  f"WIS: {self.stats['wis']}+{compare[stat_indices['wis']]}\n"
                  f"CHA: {self.stats['cha']}+{compare[stat_indices['cha']]}\n"
                  f"HP: {self.max_hp}+{compare[6]}\n"
                  f"MP: {self.max_mp}+{compare[7]}\n"
                  )
        else:
            print(f"HP: {self.max_hp}\n"
                  f"MP: {self.max_mp}\n"
                  f"STR: {self.stats['stR']}\n"
                  f"DEX: {self.stats['dex']}\n"
                  f"CON: {self.stats['con']}\n"
                  f"INT: {self.stats['iNt']}\n"
                  f"WIS: {self.stats['wis']}\n"
                  f"CHA: {self.stats['cha']}\n")

    def levelUp(self, stat, roll=None):
        change = [0] * 8
        if stat not in stat_indices:
            print("Error: Nonexistent Stat. Try again.")
            return False
        else:
            self.stats[stat] += 1
            change[stat_indices[stat]] = 1
            print(f"{stat} + 1")
        if not roll:
            autoRoll = sum(d6(4))
            self.hp_rolls.append(autoRoll)
            change[6] = autoRoll
        else:
            self.hp_rolls.append(roll)
            change[6] = roll
        self.recalculate_HP()

        self.printStats(change)
        return True

    def add_exp(self, exp_amount):
        self.exp += exp_amount
        if self.exp >= exp_levels[self.level+1]:
            print("LEVEL UP")
            while 1:
                stat = input("Choose a stat")
                if self.levelUp(stat):
                    break

    def addToBag(self, item):
        self.bag.append(item)

    def increaseStat(self, stat, amount=1):
        if type(stat) == str:
            if stat == self.talent1 or stat == self.talent2:
                self.stats[stat] += 2*amount
            else:
                self.stats[stat] += amount

    def modifyGold(self, amount):
        self.gold = self.gold + amount

    def purchaseItem(self, amount, item=None):
        if item:
            self.addToBag(item)
        self.gold -= amount

    def use_skill(self, skill_name):
        skill = self.skills[skill_name][0]
        effect, roll = skill.get_combat_stats()
        print(effect, f"{roll[1]}d{roll[0]}")
        self.skills[skill_name][1] += 1
        if self.skills[skill_name][1] in proficiency_levels:
            skill.evolve_skill()
        return effect, roll

    def attack(self, skill = None, initiationRoll = None, enemy = None, enemyRoll = None):
        if initiationRoll and enemyRoll:
            print()
        elif initiationRoll and enemy:
            pass
            #TODO
        else:
            print(self.stats["dex"]+d20())
            return self.stats["dex"]+d20()






