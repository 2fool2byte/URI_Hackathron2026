from dataclasses import dataclass
from enum import Enum

class Element(Enum):
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    NONE = "None"

class SpellType(Enum):
    BASIC = "Basic"
    SIGNATURE = "Signature"

@dataclass
class Spell:
    name: str
    damage: int
    mana_cost: int
    element: Element
    spell_type: SpellType
    cooldown:int

# Spells

# Basic Spells
punch = Spell(
    name="Punch",
    damage=10,
    mana_cost=0,
    element=Element.NONE,
    spell_type=SpellType.BASIC,
    cooldown=0
)
# Water Spells
aqua_bolt = Spell(
    name="Aqua Bolt",
    damage=15,
    mana_cost=10,
    element=Element.WATER,
    spell_type=SpellType.BASIC,
    cooldown=1
)
waterfall = Spell(
    name="Waterfall",
    damage=30,
    mana_cost=25,
    element=Element.WATER,
    spell_type=SpellType.SIGNATURE,
    cooldown=3
)
# Grass Spells
vine_whip = Spell(
    name="Vine Whip",
    damage=15,
    mana_cost=10,
    element=Element.GRASS,
    spell_type=SpellType.BASIC,
    cooldown=1
)
leaf_storm = Spell(
    name="Leaf Storm",
    damage=30,
    mana_cost=25,
    element=Element.GRASS,
    spell_type=SpellType.SIGNATURE,
    cooldown=3
)
# Fire Spells
fireball = Spell(
    name="Fireball",
    damage=15,
    mana_cost=10,
    element=Element.FIRE,
    spell_type=SpellType.BASIC,
    cooldown=1
)
dragons_breath = Spell(
    name="Dragon's Breath",
    damage=30,
    mana_cost=25,
    element=Element.FIRE,
    spell_type=SpellType.SIGNATURE,
    cooldown=3
)

# Mob Spells

# Slime
splash = Spell(
    name="Splash",
    damage=8,
    mana_cost=0,
    element=Element.WATER,
    spell_type=SpellType.BASIC,
    cooldown=0
)
# Fire Spirit
ignite = Spell(
    name="Ignite",
    damage=13,
    mana_cost=0,
    element=Element.FIRE,
    spell_type=SpellType.BASIC,
    cooldown=0
)
# Golem
rock_throw = Spell(
    name="Rock Throw",
    damage=18,
    mana_cost=0,
    element=Element.NONE,
    spell_type=SpellType.BASIC,
    cooldown=1
)
entangle = Spell(
    name="Entangle",
    damage=12,
    mana_cost=0,
    element=Element.GRASS,
    spell_type=SpellType.BASIC,
    cooldown=0
)
# Witch
curse = Spell(
    name="Curse",
    damage=20,
    mana_cost=0,
    element=Element.NONE,
    spell_type=SpellType.SIGNATURE,
    cooldown=2
)

# Spell Lists
mob_spells = [splash, ignite, rock_throw, entangle]
witch_spells = [curse, aqua_bolt, vine_whip, fireball]
player_spells = [punch, aqua_bolt, waterfall, vine_whip, leaf_storm, fireball, dragons_breath]

# Combined Spell List for Export
spells = [player_spells, mob_spells, witch_spells]