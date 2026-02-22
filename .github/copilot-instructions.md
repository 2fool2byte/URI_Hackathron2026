# Copilot Instructions for URI_Hackathon2026

## Project Overview
This is a Pygame-based turn-based battle game where players fight enemies with spells, items, and basic attacks. The game has menu navigation between a main menu and spell selection menus.

## Architecture

### Core Systems
1. **Character System** (`Characters.py`):
   - Base `Character` class with health, weakness/immunity system, and attacks dictionary
   - `Boss` class extends Character with a `heal()` method
   - Characters track attacks as dict entries with "damage" and "element" keys
   - Weakness multiplies damage by 1.3x; Immunity blocks damage entirely
   - Both character types and enemies use element-based damage calculations (case-insensitive)

2. **Spell System** (`spells.py`):
   - Spells are `@dataclass` objects with: name, damage, mana_cost, element (Enum), spell_type, cooldown
   - Two enums: `Element` (FIRE/WATER/GRASS/NONE) and `SpellType` (BASIC/SIGNATURE)
   - Global spell instances (punch, aqua_bolt, fireball, etc.) are instantiated as module-level constants
   - Spells are collected into a `spells` dict (e.g., `spells = {punch, aqua_bolt, ...}`)

3. **Enemy System** (`enemies.py`):
   - `Enemies` class (note: singular naming conflict) with name, weakness, immunity, element, attack damage
   - Enemies have simpler structure than Character (no attacks dict; single attack value)
   - Global enemy instances defined at module level (fslime, wslime, gslime, fspirit, etc.)

4. **Items System** (`items.py`):
   - `Potion` class with name, p_type ("Health"/"Mana"), amount, price
   - `consume()` method updates player health or mana (case-insensitive type check)
   - Pre-instantiated potions: small/medium/large variants for health and mana

5. **Game Loop** (`main.py`):
   - Pygame display at 1280x720 (+ 200px bottom panel)
   - Button-based UI for menus (punch, spells, items buttons)
   - Menu state tracked via `current_menu` string ("main", "spells")
   - Two draw layers: background/panel, then main game elements, then buttons
   - Event loop: checks click events on buttons, delegates to clickable objects

## Critical Patterns

### Bug Hotspot: Undefined Variables
Recent issue: `open_spells` variable referenced in Button constructor that doesn't exist. Always check that Button parameters reference defined image variables (e.g., `spells_button_img`, not undefined names).

### Button and Menu Flow
- Buttons store click state and call registered callbacks
- Menu switching happens via button clicks changing `current_menu`
- Each menu state draws different button sets (main shows items/spells/punch; spells menu shows fire_button/aqua_button/back_button)
- Button images must be loaded before instantiation and correctly named

### Element System
- Three elements: Fire, Water, Grass (plus None for neutral attacks)
- Weakness creates 1.3x damage multiplier
- Immunity blocks damage (returns "Immune" string)
- Comparisons are case-insensitive (use `.casefold()`)

### Character vs Enemy Differences
- **Character**: attacks stored as dict {name: {damage, element}}; uses `attackAction(target, attack_name)`
- **Enemy**: single attack value + element property; use `attackAction(player)` for direct damage
- Both inherit similar health/weakness/immunity logic but implement it slightly differently

## Developer Workflow

### Run the Game
```bash
python main.py
```
Requires: pygame. See `Requirements.txt` for dependencies.

### Adding New Content
- **New Spells**: Add `@dataclass Spell` instance to `spells.py`, add to module-level `spells` collection
- **New Enemies**: Create `Enemies()` instance in `enemies.py`, add to `enemies` list
- **New Potions**: Create `Potion()` instance in `items.py`, add to `potions` list
- **New Character/Boss**: Subclass `Character` in `Characters.py`, add attacks dict

### Common Fixes
- Image loading: use `pygame.image.load()` + `.convert_alpha()` + `pygame.transform.scale()`
- Undefined variables: check all Button constructors reference existing `*_img` variables
- Type checking: be careful with `in` vs `==` for element/type comparisons (code uses both patterns)

## File Organization
```
main.py           # Game loop, UI rendering, menu logic
Characters.py     # Character and Boss classes
enemies.py        # Enemy class and instances
spells.py         # Spell dataclass and instances
items.py          # Potion class and instances
img/              # Game assets (Backgrounds, Characters, Icons)
```

## Notes for AI Agents
- The codebase has minor inconsistencies (Enemy vs Enemies, some type checks use `in` vs `==`)
- Player character instantiated as `Character(25, 250, "Player", ...)` with x, y position as first args
- Stage system uses dict list with "enemies" and "background" keys (not yet fully integrated in main loop)
- Some imported items (like `spells.splasha` referenced in Character constructor) may not exist—verify spell names match `spells.py` definitions before referencing
