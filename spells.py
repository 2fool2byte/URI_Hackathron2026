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

# Spells

# Basic Spells
punch = Spell(
    name="Punch",
    damage=10,
    mana_cost=0,
    element=Element.NONE,
    spell_type=SpellType.BASIC
)
# Water Spells
aqua_bolt = Spell(
    name="Aqua Bolt",
    damage=15,
    mana_cost=10,
    element=Element.WATER,
    spell_type=SpellType.BASIC
)
waterfall = Spell(
    name="Waterfall",
    damage=30,
    mana_cost=25,
    element=Element.WATER,
    spell_type=SpellType.SIGNATURE
)
# Grass Spells
vine_whip = Spell(
    name="Vine Whip",
    damage=15,
    mana_cost=10,
    element=Element.GRASS,
    spell_type=SpellType.BASIC
)
leaf_storm = Spell(
    name="Leaf Storm",
    damage=30,
    mana_cost=25,
    element=Element.GRASS,
    spell_type=SpellType.SIGNATURE
)
# Fire Spells
fireball = Spell(
    name="Fireball",
    damage=15,
    mana_cost=10,
    element=Element.FIRE,
    spell_type=SpellType.BASIC
)
dragons_breath = Spell(
    name="Dragon's Breath",
    damage=30,
    mana_cost=25,
    element=Element.FIRE,
    spell_type=SpellType.SIGNATURE
)

spells = [punch, aqua_bolt, waterfall, vine_whip, leaf_storm, fireball, dragons_breath]