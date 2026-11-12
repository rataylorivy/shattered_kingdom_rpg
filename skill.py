from colorama import Fore

class Skill:
    def __init__(self, name, mp_cost, cooldown, description):
        self.name, self.mp_cost, self.cooldown = name, mp_cost, cooldown
        self.description = description
        self.remaining_cooldown = 0

    def ready(self):
        return self.remaining_cooldown == 0

    def tick(self):
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= 1

    def use(self, player, target=None):
        raise NotImplementedError

class PowerStrike(Skill):
    def __init__(self):
        super().__init__("Power Strike", 3, 1, "A stronger physical attack.")

    def use(self, player, target=None):
        if player.mp < self.mp_cost or not self.ready():
            return False
        player.mp -= self.mp_cost
        damage = 16 + player.level * 2
        target.take_damage(damage)
        self.remaining_cooldown = self.cooldown
        print(Fore.YELLOW + f"Power Strike deals {damage} damage!")
        return True

class Fireball(Skill):
    def __init__(self):
        super().__init__("Fireball", 5, 2, "A burst of magical energy.")

    def use(self, player, target=None):
        if player.mp < self.mp_cost or not self.ready():
            return False
        player.mp -= self.mp_cost
        damage = 23 + player.level * 2
        target.take_damage(damage)
        self.remaining_cooldown = self.cooldown
        print(Fore.YELLOW + f"Fireball deals {damage} damage!")
        return True

class Heal(Skill):
    def __init__(self):
        super().__init__("Heal", 4, 2, "Restore some health.")

    def use(self, player, target=None):
        if player.mp < self.mp_cost or not self.ready():
            return False
        player.mp -= self.mp_cost
        restored = min(18, player.max_hp - player.hp)
        player.hp += restored
        self.remaining_cooldown = self.cooldown
        print(Fore.GREEN + f"Heal restores {restored} HP.")
        return True

class QuickShot(Skill):
    def __init__(self):
        super().__init__("Quick Shot", 2, 1, "A quick ranged attack.")

    def use(self, player, target=None):
        if player.mp < self.mp_cost or not self.ready():
            return False
        player.mp -= self.mp_cost
        damage = 11 + player.level
        target.take_damage(damage)
        self.remaining_cooldown = self.cooldown
        print(Fore.YELLOW + f"Quick Shot deals {damage} damage!")
        return True

SKILL_BY_NAME = {c().name: c for c in (PowerStrike, Fireball, Heal, QuickShot)}
