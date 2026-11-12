from colorama import Fore

class WorldMap:
    SYMBOLS = {"#": Fore.WHITE + "#", ".": Fore.GREEN + ".", "N": Fore.MAGENTA + "N",
               "M": Fore.RED + "M", "S": Fore.CYAN + "S", "B": Fore.RED + "B"}

    def __init__(self, name, layout):
        self.name = name.title()
        self.layout = [list(row) for row in layout]

    def in_bounds(self, position):
        x, y = position
        return 0 <= y < len(self.layout) and 0 <= x < len(self.layout[y])

    def tile_at(self, position):
        x, y = position
        return self.layout[y][x] if self.in_bounds(position) else "#"

    def walkable(self, position):
        return self.tile_at(position) != "#"

    def clear_tile(self, position):
        x, y = position
        if self.in_bounds(position):
            self.layout[y][x] = "."

    def display(self, player_position):
        px, py = player_position
        for y, row in enumerate(self.layout):
            line = ""
            for x, tile in enumerate(row):
                line += Fore.YELLOW + "@" if (x, y) == (px, py) else self.SYMBOLS.get(tile, tile)
            print(line)
        print("@ You | # Wall | N Person | M Monster | S Passage")
