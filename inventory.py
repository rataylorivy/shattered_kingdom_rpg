from colorama import Fore
from item import ITEMS

class Inventory:
    def __init__(self, items=None):
        self.items = list(items or [])

    def add(self, item_name):
        self.items.append(item_name)

    def count(self, item_name):
        return self.items.count(item_name)

    def remove(self, item_name):
        if item_name in self.items:
            self.items.remove(item_name)
            return True
        return False

    def show(self):
        print(Fore.CYAN + "\n-- INVENTORY --")
        if not self.items:
            print("Your inventory is empty.")
            return
        counts = {}
        for name in self.items:
            counts[name] = counts.get(name, 0) + 1
        for name, count in counts.items():
            print(f"{name} x{count} - {ITEMS.get(name).description if name in ITEMS else 'Unknown item'}")
        choice = input("Use a Potion or Ether? (name, or Enter to return): ").strip().title()
        if choice in ("Potion", "Ether"):
            # Player is passed to use(); standalone inventory view cannot consume it.
            print("Use items during combat, or choose a different option.")

    def use(self, name, player):
        if name not in ("Potion", "Ether") or not self.remove(name):
            return False
        item = ITEMS[name]
        if item.kind == "healing":
            restored = min(item.power, player.max_hp - player.hp)
            player.hp += restored
            print(f"You recover {restored} HP.")
        else:
            restored = min(item.power, player.max_mp - player.mp)
            player.mp += restored
            print(f"You recover {restored} MP.")
        return True

    def to_list(self):
        return list(self.items)
