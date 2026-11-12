from colorama import Fore, Style, init
from auth import authenticate
from database import GameDatabase
from player import Player
from world_map import WorldMap
from combat import Combat
from npc import NPC, NPCS
from shop import Shop
from quest import QuestManager
from monster import MONSTER_TYPES, create_monster
from item import ITEMS

init(autoreset=True)

class Game:
    def __init__(self):
        self.db = GameDatabase()
        self.player = None
        self.current_map = "village"
        self.position = (1, 1)
        self.quests = None
        self.maps = {
            "village": WorldMap("village", [
                "##########",
                "#..N.....#",
                "#..##....#",
                "#........#",
                "#....S...#",
                "##########"
            ]),
            "forest": WorldMap("forest", [
                "############",
                "#....#.....#",
                "#.##.#.##..#",
                "#....M.....#",
                "###....##..#",
                "#.....#....#",
                "#..N..#....#",
                "############"
            ]),
            "dungeon": WorldMap("dungeon", [
                "############",
                "#..M.......#",
                "#.####.###.#",
                "#......#...#",
                "#.##...#.#.#",
                "#....B.....#",
                "############"
            ])
        }
        self.combat = Combat()

    def run(self):
        print(Fore.CYAN + Style.BRIGHT + "\n=== THE SHATTERED KINGDOM ===")
        print("The ancient seal has broken. A creeping blight spreads beyond the old walls.")
        username, saved = authenticate(self.db)
        if saved:
            self.player = Player.from_dict(saved["player"])
            self.current_map = saved.get("current_map", "village")
            self.position = tuple(saved.get("position", [1, 1]))
            self.quests = QuestManager.from_dict(saved.get("quests", {}))
            print(Fore.GREEN + f"Welcome back, {username}. Your journey continues.")
        else:
            self.player = Player(username)
            self.quests = QuestManager()
            print(Fore.YELLOW + f"\nWelcome, {username}. The kingdom needs your help.")
            print("Controls: WASD to move, I inventory, C character, Q quests, H help, X save and exit.")
        self.main_loop()

    def main_loop(self):
        while True:
            self.show_location()
            command = input("\n> ").strip().lower()
            if command in ("x", "exit", "quit"):
                self.save()
                print(Fore.CYAN + "Progress saved. Farewell, adventurer!")
                break
            elif command in ("w", "a", "s", "d"):
                self.move(command)
            elif command == "i":
                self.player.inventory.show()
            elif command == "c":
                self.player.show_status()
            elif command == "q":
                self.quests.show()
            elif command == "h":
                self.help()
            elif command == "n":
                self.talk()
            elif command == "t":
                self.travel()
            elif command == "b":
                self.visit_shop()
            elif command == "r":
                self.rest()
            elif command == "v":
                self.save()
            else:
                print(Fore.RED + "I don't recognize that command. Press H for help.")

    def show_location(self):
        area = self.maps[self.current_map]
        print(Fore.BLUE + Style.BRIGHT + f"\n-- {area.name.upper()} --")
        area.display(self.position)
        print("Nearby actions: N talk | T travel (at a gate) | B shop (village) | R rest (village)")
        print("WASD move | I inventory | C character | Q quests | V save | X save & exit | H help")

    def help(self):
        print("""
W/A/S/D  Move one tile
N        Talk to a nearby character
T        Travel between areas (stand on a gate marked S)
B        Visit the village shop
R        Rest in the village to restore HP and MP
I        View/use inventory
C        View character stats and skills
Q        View quest progress
V        Save
X        Save and exit
""")

    def move(self, direction):
        dxdy = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        dx, dy = dxdy[direction]
        x, y = self.position
        target = (x + dx, y + dy)
        area = self.maps[self.current_map]
        if not area.walkable(target):
            print(Fore.RED + "A wall blocks your way.")
            return
        self.position = target
        tile = area.tile_at(target)
        if tile == "M":
            monster = create_monster(self.current_map)
            print(Fore.RED + f"A {monster.name} appears!")
            if self.combat.fight(self.player, monster):
                completed_before = set(self.quests.completed)
                self.quests.record_monster(monster.name)
                self.reward_new_quests(completed_before)
                self.player.gain_xp(monster.xp_reward)
                self.player.gold += monster.gold_drop
                print(Fore.YELLOW + f"You receive {monster.gold_drop} gold and {monster.xp_reward} XP.")
                if monster.item_drop:
                    self.player.inventory.add(monster.item_drop)
                    print(Fore.GREEN + f"The monster dropped: {monster.item_drop}!")
                    if monster.item_drop == "Moonleaf" and self.quests.is_active("side_herbs") and self.player.inventory.count("Moonleaf") >= 2:
                        completed_before = set(self.quests.completed)
                        self.quests.complete("side_herbs")
                        self.reward_new_quests(completed_before)
                area.clear_tile(target)
                if self.current_map == "dungeon" and monster.name == "The Hollow King":
                    self.quests.complete("main_final")
                    print(Fore.GREEN + Style.BRIGHT + "THE KINGDOM IS FREE! You have completed the main quest.")
                self.save()
            else:
                print(Fore.RED + "You retreat to the village infirmary.")
                self.current_map, self.position = "village", (1, 1)
                self.player.hp = max(1, self.player.max_hp // 2)
        elif tile == "N":
            print("Someone is nearby. Press N to speak.")
        elif tile == "S":
            print("A marked passage leads onward. Press T to travel.")

    def talk(self):
        characters = NPCS.get(self.current_map, [])
        if not characters:
            print("There is nobody nearby to talk to.")
            return
        print("\nPeople here:")
        for index, npc in enumerate(characters, 1):
            print(f"{index}. {npc.name}")
        print("0. Never mind")
        try:
            choice = int(input("Who would you like to speak with? "))
            if choice == 0:
                return
            npc = characters[choice - 1]
        except (ValueError, IndexError):
            print("Please choose a listed character.")
            return

        print(Fore.MAGENTA + f'{npc.name}: "{npc.dialogue}"')
        if npc.quest_id == "main_start":
            if not self.quests.is_complete("main_start"):
                self.quests.complete("main_start")
                self.quests.activate("main_forest")
                print("Main quest started: clear three creatures from the forest.")
            elif self.quests.is_complete("main_forest"):
                self.quests.activate("main_final")
                print("The elder reveals the dungeon passage. The Hollow King waits below.")
            else:
                print("The elder urges you to clear three creatures from the forest.")
        elif npc.quest_id == "side_herbs":
            if not self.quests.is_complete("side_herbs"):
                self.quests.activate("side_herbs")
                print("Side quest started: collect two Moonleaf herbs.")
            else:
                print("Elara thanks you again for your help.")
        elif npc.quest_id == "side_bandits":
            if not self.quests.is_complete("side_bandits"):
                self.quests.activate("side_bandits")
                print("Side quest started: defeat two creatures.")
            else:
                print("Captain Bram salutes you.")
        elif npc.quest_id == "main_dungeon":
            if self.quests.is_complete("main_forest"):
                self.quests.activate("main_final")
                print("The elder reveals the dungeon passage. The Hollow King waits below.")
            else:
                print("The elder says: clear the blight from the forest first.")
        else:
            print("They wish you well.")

    def travel(self):
        if self.current_map == "village":
            self.current_map, self.position = "forest", (1, 1)
        elif self.current_map == "forest":
            self.current_map, self.position = "dungeon", (1, 1)
        else:
            self.current_map, self.position = "forest", (1, 1)
        print(Fore.CYAN + f"You travel to {self.maps[self.current_map].name}.")

    def visit_shop(self):
        if self.current_map != "village":
            print("The shop is only available in the village.")
            return
        Shop(self.player).visit()

    def rest(self):
        if self.current_map != "village":
            print("You can only rest safely in the village.")
            return
        self.player.hp = self.player.max_hp
        self.player.mp = self.player.max_mp
        print(Fore.GREEN + "You rest and recover all HP and MP.")

    def reward_new_quests(self, completed_before):
        rewards = {
            "side_herbs": (15, 20, "Ether"),
            "side_bandits": (20, 25, "Potion")
        }
        for quest_id in set(self.quests.completed) - completed_before:
            if quest_id in rewards:
                gold, xp, item = rewards[quest_id]
                self.player.gold += gold
                self.player.gain_xp(xp)
                self.player.inventory.add(item)
                print(Fore.YELLOW + f"Quest reward: {gold} gold, {xp} XP, and {item}!")

    def save(self):
        self.db.save_game(self.player.username, self.player.to_dict(), self.current_map,
                          list(self.position), self.quests.to_dict())
