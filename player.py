from colorama import Fore
from inventory import Inventory
from skill import Fireball, Heal, PowerStrike

class Player:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.xp = 0
        self.gold = 20
        self.max_hp = 40
        self.hp = 40
        self.max_mp = 15
        self.mp = 15
        self.inventory = Inventory(["Potion", "Potion"])
        self.skills = [PowerStrike(), Heal()]

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 30:
            self.xp -= self.level * 30
            self.level += 1
            self.max_hp += 8
            self.max_mp += 3
            self.hp, self.mp = self.max_hp, self.max_mp
            print(Fore.YELLOW + f"LEVEL UP! You are now level {self.level}.")

    def show_status(self):
        print(f"\n{self.username} | Level {self.level} | XP {self.xp}/{self.level*30}")
        print(f"HP {self.hp}/{self.max_hp} | MP {self.mp}/{self.max_mp} | Gold {self.gold}")
        print("Skills:", ", ".join(skill.name for skill in self.skills))

    def to_dict(self):
        return {"username": self.username, "level": self.level, "xp": self.xp,
                "gold": self.gold, "max_hp": self.max_hp, "hp": self.hp,
                "max_mp": self.max_mp, "mp": self.mp,
                "inventory": self.inventory.to_list(),
                "skills": [s.name for s in self.skills]}

    @classmethod
    def from_dict(cls, data):
        from skill import SKILL_BY_NAME
        player = cls(data["username"])
        for key in ("level", "xp", "gold", "max_hp", "hp", "max_mp", "mp"):
            setattr(player, key, data.get(key, getattr(player, key)))
        player.inventory = Inventory(data.get("inventory", []))
        player.skills = [SKILL_BY_NAME[name]() for name in data.get("skills", ["Power Strike", "Heal"]) if name in SKILL_BY_NAME]
        return player
