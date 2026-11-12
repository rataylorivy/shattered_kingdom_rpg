from colorama import Fore

class Combat:
    def fight(self, player, monster):
        print(Fore.RED + f"\nBattle begins: {monster.name} (HP {monster.hp})")
        while monster.is_alive() and player.hp > 0:
            print(f"\nYour HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")
            print(f"{monster.name} HP: {monster.hp}/{monster.max_hp}")
            print("1. Attack  2. Use skill  3. Use potion  4. Retreat")
            choice = input("Choose: ").strip()
            if choice == "1":
                damage = 8 + player.level * 2
                monster.take_damage(damage)
                print(f"You deal {damage} damage.")
            elif choice == "2":
                self.use_skill(player, monster)
            elif choice == "3":
                if not player.inventory.use("Potion", player):
                    print("No potion available.")
            elif choice == "4":
                print("You retreat!")
                return False
            else:
                print("Please enter 1, 2, 3, or 4.")
                continue
            if monster.is_alive():
                monster.attack_player(player)
            for skill in player.skills:
                skill.tick()
        if player.hp <= 0:
            return False
        print(Fore.GREEN + f"You defeated {monster.name}!")
        return True

    def use_skill(self, player, monster):
        if not player.skills:
            print("You have no skills.")
            return
        for index, skill in enumerate(player.skills, 1):
            status = "ready" if skill.ready() else f"cooldown {skill.remaining_cooldown}"
            print(f"{index}. {skill.name} ({skill.mp_cost} MP, {status}) - {skill.description}")
        try:
            choice = int(input("Skill number (0 to cancel): "))
            if choice == 0:
                return
            skill = player.skills[choice - 1]
            if not skill.use(player, monster):
                print("That skill is unavailable (not enough MP or cooling down).")
        except (ValueError, IndexError):
            print("Invalid skill choice.")
