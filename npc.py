class NPC:
    def __init__(self, name, dialogue, quest_id=None):
        self.name, self.dialogue, self.quest_id = name, dialogue, quest_id

NPCS = {
    "village": [
        NPC("Elder Rowan", "The seal beneath the old fortress has shattered. The forest creatures are restless.", "main_start"),
        NPC("Healer Elara", "Moonleaf grows in the forest. Bring me two leaves and I can make a useful remedy.", "side_herbs"),
        NPC("Captain Bram", "Creatures have been harassing travelers. Defeat two and the road may become safer.", "side_bandits")
    ],
    "forest": [
        NPC("Mira the Ranger", "The trees remember a time before the blight. Clear the creatures and seek the old passage.")
    ],
    "dungeon": [
        NPC("The Echo", "A voice drifts through the dark: the crown can be mended, but only after its guardian falls.")
    ]
}
