import random
from colorama import Fore

class Monster:
    def __init__(self, name, hp, attack, xp_reward, gold_drop, item_drop=None):
        self.name, self.max_hp, self.hp = name, hp, hp
        self.attack = attack
        self.xp_reward = xp_reward
        self.gold_drop = gold_drop
        self.item_drop = item_drop

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def is_alive(self):
        return self.hp > 0

    def attack_player(self, player):
        damage = random.randint(max(1, self.attack - 2), self.attack + 2)
        player.hp = max(0, player.hp - damage)
        print(Fore.RED + f"{self.name} deals {damage} damage.")

class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", 18, 6, 12, 7, "Herb")

class Wolf(Monster):
    def __init__(self):
        super().__init__("Blight Wolf", 24, 8, 16, 9, "Potion")

class Slime(Monster):
    def __init__(self):
        super().__init__("Moss Slime", 15, 5, 10, 5, "Moonleaf")

class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", 30, 9, 22, 12, "Potion")

class HollowKing(Monster):
    def __init__(self):
        super().__init__("The Hollow King", 75, 12, 80, 60, "Crown Shard")

MONSTER_TYPES = [Goblin, Wolf, Slime, Skeleton]

def create_monster(area):
    if area == "dungeon":
        return HollowKing()
    return random.choice(MONSTER_TYPES)()
