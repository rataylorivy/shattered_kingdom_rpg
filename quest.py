from colorama import Fore

QUESTS = {
    "main_start": ("The Elder's Request", "Speak with Elder Rowan.", 0),
    "main_forest": ("Clear the Forest", "Defeat three creatures in the forest.", 3),
    "main_final": ("The Hollow King", "Enter the dungeon and defeat the Hollow King.", 1),
    "side_herbs": ("A Healer's Help", "Collect two Moonleaf herbs.", 2),
    "side_bandits": ("Trouble on the Road", "Defeat two creatures.", 2)
}

class QuestManager:
    def __init__(self):
        self.active = []
        self.completed = []
        self.progress = {}

    def activate(self, quest_id):
        if quest_id in QUESTS and quest_id not in self.active and quest_id not in self.completed:
            self.active.append(quest_id)
            self.progress.setdefault(quest_id, 0)

    def complete(self, quest_id):
        if quest_id not in self.completed:
            if quest_id not in self.active:
                self.activate(quest_id)
            self.active = [q for q in self.active if q != quest_id]
            self.completed.append(quest_id)
            print(Fore.GREEN + f"Quest completed: {QUESTS[quest_id][0]}")

    def is_active(self, quest_id):
        return quest_id in self.active

    def is_complete(self, quest_id):
        return quest_id in self.completed

    def record_monster(self, name):
        for q in ("main_forest", "side_bandits"):
            if q in self.active:
                self.progress[q] = self.progress.get(q, 0) + 1
                goal = QUESTS[q][2]
                if self.progress[q] >= goal:
                    self.complete(q)

    def show(self):
        print(Fore.CYAN + "\n-- QUESTS --")
        for q in self.active:
            title, desc, goal = QUESTS[q]
            progress = self.progress.get(q, 0)
            suffix = f" ({progress}/{goal})" if goal else ""
            print(f"[ACTIVE] {title}: {desc}{suffix}")
        for q in self.completed:
            print(Fore.GREEN + f"[DONE] {QUESTS[q][0]}")
        if not self.active and not self.completed:
            print("No quests yet. Speak with Elder Rowan.")

    def to_dict(self):
        return {"active": self.active, "completed": self.completed, "progress": self.progress}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.active = data.get("active", [])
        obj.completed = data.get("completed", [])
        obj.progress = data.get("progress", {})
        return obj
