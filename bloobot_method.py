import bloobot_classes
import random
import json

def create_mob(name):
        creature = bloobot_classes.Mob()
        mobs = open('mob_data.json')
        pokedex = json.load(mobs)
        level_min = pokedex[name]['level_min']
        level_max = pokedex[name]['level_max']
        creature.level = random.randint(level_min,level_max)
        creature.species = name
        creature.max_hp = pokedex[name]['hp'] + creature.level
        creature.current_hp = creature.max_hp
        creature.int = pokedex[name]['int'] + creature.level
        creature.str = pokedex[name]['str']+ creature.level
        creature.dex = pokedex[name]['dex'] + creature.level
        creature.attack_skill = pokedex[name]['attack_skill']
        creature.special_skill = pokedex[name]['special_skill']
        return creature

def primary_attacks(character):
        #Character attacks
        if character.attack_skill == "Slash Strike":
                return int((character.str/5) + 4)
        #Mob attacks
        elif character.attack_skill == "Slash":
                return int((character.str/6) + 2)
        elif character.attack_skill == "Summon Vines":
                return int((character.int/6) + 2)
        elif character.attack_skill == "Bite":
                return int((character.str/12) + (character.dex/12) + 2)
        elif character.attack_skill == "Clobber":
                return int (character.str/8 + 3)