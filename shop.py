from colorama import Fore
from item import ITEMS

class Shop:
    STOCK = ("Potion", "Ether", "Fireball", "Quick Shot")

    def __init__(self, player):
        self.player = player

    def visit(self):
        print(Fore.CYAN + "\n-- VILLAGE SHOP --")
        for index, name in enumerate(self.STOCK, 1):
            if name in ITEMS:
                item = ITEMS[name]
                print(f"{index}. {name} - {item.price} gold: {item.description}")
            else:
                print(f"{index}. Learn {name} - 25 gold")
        print("0. Leave")
        choice = input("Buy: ").strip()
        if choice == "0":
            return
        try:
            selected = self.STOCK[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return
        if selected in ITEMS:
            item = ITEMS[selected]
            if self.player.gold < item.price:
                print("You don't have enough gold.")
                return
            self.player.gold -= item.price
            self.player.inventory.add(selected)
            print(Fore.GREEN + f"Purchased {selected}.")
        else:
            from skill import SKILL_BY_NAME
            if self.player.gold < 25:
                print("You need 25 gold.")
                return
            if any(s.name == selected for s in self.player.skills):
                print("You already know that skill.")
                return
            self.player.gold -= 25
            self.player.skills.append(SKILL_BY_NAME[selected]())
            print(Fore.GREEN + f"You learned {selected}!")
