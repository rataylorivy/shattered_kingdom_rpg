from tinydb import TinyDB, Query

class GameDatabase:
    def __init__(self, path="game_data.json"):
        self.db = TinyDB(path)
        self.users = self.db.table("users")

    def get_user(self, username):
        User = Query()
        results = self.users.search(User.username == username)
        return results[0] if results else None

    def create_user(self, username, password):
        if self.get_user(username):
            return False
        self.users.insert({"username": username, "password": password,
                           "player": None, "current_map": "village",
                           "position": [1, 1], "quests": {}})
        return True

    def save_game(self, username, player_data, current_map, position, quests):
        User = Query()
        self.users.update({"player": player_data, "current_map": current_map,
                           "position": position, "quests": quests},
                          User.username == username)

