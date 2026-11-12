# The Shattered Kingdom — Terminal RPG

A multi-file, terminal-based fantasy RPG built with Python. It includes account creation/login, TinyDB save files, character progression, quests, NPCs, monsters, skills, items, a shop, and multiple maps.

## Requirements
- Python 3.9+
- Packages in `requirements.txt`

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Run:
```bash
python main.py
```

The game creates `game_data.json` automatically in the same folder. It stores accounts and saved progress. Keep that file if you want to preserve saves.

## Controls
- `W`, `A`, `S`, `D`: move
- `N`: talk to the local character
- `T`: travel to the next area
- `B`: visit the village shop
- `R`: rest in the village
- `I`: inventory
- `C`: character stats and skills
- `Q`: quest log
- `V`: save
- `X`: save and exit
- `H`: help

## Quest path
1. Speak with Elder Rowan in the village.
2. Travel to the forest and defeat three creatures.
3. Return to the village and speak with Elder Rowan.
4. Travel through the forest to the dungeon and defeat the Hollow King.

Two optional quests are offered by the healer and guard in the village. Completing them grants gold, XP, and an item. The shop sells supplies and unlockable skills.

## Project structure
Each module has a distinct responsibility:
- `main.py`: program entry point
- `game.py`: main game loop and world coordination
- `player.py`: player stats and progression
- `monster.py`: monster base class and subclasses
- `skill.py`: skill base class and subclasses
- `combat.py`: turn-based battle system
- `item.py`: item definitions
- `inventory.py`: item storage and use
- `quest.py`: quest state and progress
- `npc.py`: non-player characters and dialogue
- `shop.py`: purchases and skill learning
- `world_map.py`: map layout and movement rules
- `database.py`: TinyDB persistence
- `auth.py`: registration and login
