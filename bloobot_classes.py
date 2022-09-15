class Unit:
    max_hp = 0
    current_hp = 0
    int = 0
    str = 0
    dex = 0
    level = 1
    buffs = ""
    attack_skill = ""
    special_skill = ""

class Character(Unit):
    money = 0
    f_class = ""
    mob_data = []

class Mob(Unit):
    level = 1
    species = ""
    drop_table = []

