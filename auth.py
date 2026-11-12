from colorama import Fore

def authenticate(database):
    print("\n1. Create account\n2. Log in")
    while True:
        choice = input("Choose 1 or 2: ").strip()
        if choice in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    while True:
        username = input("Username: ").strip()
        if len(username) < 3:
            print("Username must be at least 3 characters.")
            continue
        password = input("Password: ").strip()
        if len(password) < 4:
            print("Password must be at least 4 characters.")
            continue
        if choice == "1":
            if database.create_user(username, password):
                print(Fore.GREEN + "Account created.")
                return username, None
            print("That username already exists. Try logging in.")
            choice = "2"
        else:
            user = database.get_user(username)
            if user and user["password"] == password:
                return username, user if user.get("player") else None
            print(Fore.RED + "Incorrect username or password.")
