# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def main_game_loop():
    while(0):
        while(0):
            break


def attack(skill: Skill, user: Character, target: Character):
    user_dex = user.get_stat("dex")
    target_dex = target.get_stat("dex")
    user_roll = input(f"{user.name} roll d20")
    target_roll = input(f"{target.name} roll d10")
    initiation = initiation_roll(user_dex, user_roll)
    defense = defense_roll(target_dex, target_roll)

    if initiation > defense:
        print("Attack Hits!!")
        target.damage_taken

def initiation_roll(dex, roll=None):
    if roll:
        return dex + roll
    else:
        print("Roll D20")
        auto_roll = d20()
        print(f"You got {auto_roll}")
        return dex+auto_roll

def defense_roll(dex, roll=None):
    if roll:
        return dex + roll
    else:
        print("Roll D10")
        auto_roll = d10()
        print(f"You got {auto_roll}")
        return dex+auto_roll

# def main_game_loop():
#     turn, characters, skills, items = load_game()
#     while turn:
#         turn += 1
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_game_loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
