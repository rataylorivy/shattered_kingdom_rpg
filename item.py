class Item:
    def __init__(self, name, description, price, kind, power=0):
        self.name, self.description, self.price = name, description, price
        self.kind, self.power = kind, power

ITEMS = {
    "Potion": Item("Potion", "Restores 20 HP.", 10, "healing", 20),
    "Ether": Item("Ether", "Restores 8 MP.", 12, "mana", 8),
    "Moonleaf": Item("Moonleaf", "A fragrant herb used in a side quest.", 3, "quest"),
    "Herb": Item("Herb", "A useful medicinal herb.", 4, "quest"),
    "Crown Shard": Item("Crown Shard", "A fragment of the broken royal seal.", 0, "quest")
}
