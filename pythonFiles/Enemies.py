class Enemy:
    def __init__(self, name, classType, race, stats, level=0, equipment = [], drops = [], skills = [], description = ""):

        self.name = name
        self.classType = classType
        self.race = race
        self.stats = stats
        self.level = level
        self.equipment = equipment
        self.drops = drops
        self.skills = skills
        self.description = description

    # eg Enemy(Dark Elf, Ranger, Elf, [hp=10, mp = 10 str = 1, dex = 2, int = 3, wis = 4, con = 5, cha = 6], level = 5,
    # equipment = [dark helmet, leather armor], drops: {amulet: 20, dark helmet:10}, skills = [earthquake, dark claw],
    # description = " a fallen elf"




