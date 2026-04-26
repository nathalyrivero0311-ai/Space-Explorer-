# ============================================================
# SPACE EXPLORER - A Text-Based Space Adventure Game
# Intro to Computer Science - Python Project
# ============================================================
# HOW TO PLAY:
#   python space_explorer.py
#
# GOAL:
#   Pilot your spaceship through 5 planets, battle aliens,
#   collect resources, and make it back to Earth alive!
# ============================================================

import random   # Used for random events, alien attacks, loot


# ============================================================
# OBJECT-ORIENTED PROGRAMMING: Classes
# ============================================================

class Spaceship:
    """
    Represents the player's spaceship.
    Covers: OOP, __init__, methods, int, str, float, bool, list
    """

    def __init__(self, name, ship_type):
        # String attributes
        self.name = name
        self.ship_type = ship_type      # e.g. "Fighter", "Scout", "Hauler"

        # Integer attributes
        self.hull = 100                 # health of the ship
        self.max_hull = 100
        self.fuel = 80                  # fuel needed to travel
        self.max_fuel = 100
        self.attack = 10
        self.shield = 5
        self.credits = 50
        self.level = 1
        self.experience = 0

        # List — cargo hold stores collected items
        self.cargo = []

        # Boolean — is the ship still flying?
        self.is_operational = True

    def show_status(self):
        """Print all ship stats. Uses: strings, f-strings, integers."""
        print("\n" + "=" * 45)
        print(f"  SHIP    : {self.name}  [{self.ship_type}]")
        print(f"  Level   : {self.level}   XP: {self.experience}")
        print(f"  Hull    : {self.hull} / {self.max_hull}")
        print(f"  Fuel    : {self.fuel} / {self.max_fuel}")
        print(f"  Attack  : {self.attack}")
        print(f"  Shield  : {self.shield}")
        print(f"  Credits : {self.credits}")
        print("=" * 45)

    def show_cargo(self):
        """Show cargo hold contents. Uses: list, for loop, conditional."""
        print("\n  --- Cargo Hold ---")
        if len(self.cargo) == 0:
            print("  (Empty)")
        else:
            # Control loop: for loop over list
            for i, item in enumerate(self.cargo, start=1):
                print(f"  {i}. {item}")

    def collect_item(self, item):
        """Add item to cargo list."""
        self.cargo.append(item)
        print(f"  >> Collected: {item}")

    def use_repair_kit(self):
        """
        Repair hull using a Repair Kit from cargo.
        Uses: list methods, conditionals, integers, arithmetic
        """
        if "Repair Kit" in self.cargo:
            repair = 35
            self.hull = min(self.hull + repair, self.max_hull)
            self.cargo.remove("Repair Kit")
            print(f"  >> Repair Kit used! Hull restored by {repair}.")
            print(f"  >> Hull is now {self.hull}/{self.max_hull}.")
        else:
            print("  >> No Repair Kits in cargo!")

    def take_damage(self, damage):
        """
        Reduce hull by damage after shields absorb some.
        Uses: integers, arithmetic, max(), boolean
        """
        absorbed = max(damage - self.shield, 1)   # Always take at least 1
        self.hull -= absorbed
        print(f"  >> Hull took {absorbed} damage! Hull: {self.hull}/{self.max_hull}")
        if self.hull <= 0:
            self.hull = 0
            self.is_operational = False

    def use_fuel(self, amount):
        """Burn fuel to travel. Uses: integers, conditional."""
        self.fuel -= amount
        if self.fuel < 0:
            self.fuel = 0
        print(f"  >> Burned {amount} fuel. Remaining: {self.fuel}/{self.max_fuel}")

    def gain_experience(self, amount):
        """
        Add XP and level up if enough is earned.
        Uses: integers, conditionals, arithmetic
        """
        self.experience += amount
        print(f"  >> Gained {amount} XP! (Total: {self.experience})")
        if self.experience >= self.level * 60:
            self.level += 1
            self.attack += 4
            self.shield += 2
            self.max_hull += 15
            self.hull = self.max_hull
            print(f"\n  *** LEVEL UP! Now Level {self.level}! ***")
            print(f"  Attack +4, Shield +2, Max Hull +15 (fully repaired!)")


class Alien:
    """
    Represents an alien enemy encountered on a planet.
    Uses: OOP, strings, integers, tuples
    """

    def __init__(self, name, hull, attack, shield, xp_reward, credit_range):
        self.name = name
        self.hull = hull
        self.attack = attack
        self.shield = shield
        self.xp_reward = xp_reward
        self.credit_range = credit_range    # Tuple: (min, max) credits dropped
        self.is_alive = True

    def take_damage(self, damage):
        """Reduce alien hull by damage - shield."""
        actual = max(damage - self.shield, 1)
        self.hull -= actual
        print(f"  >> {self.name} took {actual} damage! Hull left: {max(self.hull, 0)}")
        if self.hull <= 0:
            self.hull = 0
            self.is_alive = False

    def drop_credits(self):
        """
        Return random credit drop using the credit_range tuple.
        Uses: tuple indexing, random module
        """
        return random.randint(self.credit_range[0], self.credit_range[1])


class SpaceStation:
    """
    A space station where the player can buy supplies.
    Uses: OOP, dictionary, for loop, exception handling
    """

    def __init__(self, station_name):
        self.station_name = station_name

        # Dictionary: item name -> price in credits
        self.stock = {
            "Repair Kit":    20,
            "Fuel Canister": 15,
            "Laser Upgrade": 35,
            "Shield Booster": 28,
        }

    def display_stock(self):
        """Show all items for sale. Uses: dictionary, for loop."""
        print(f"\n  === {self.station_name} Supply Shop ===")
        # Control loop: for loop over dictionary items
        for item, price in self.stock.items():
            print(f"    {item:<20} : {price} credits")

    def purchase(self, ship, item_name):
        """
        Buy an item from the station.
        Uses: dictionary lookup, exception handling (KeyError), conditionals
        """
        # Exception handling: if player types something not in the dictionary
        try:
            price = self.stock[item_name]
        except KeyError:
            print(f"  >> '{item_name}' is not stocked here.")
            return

        if ship.credits < price:
            print(f"  >> Not enough credits! Need {price}, have {ship.credits}.")
        else:
            ship.credits -= price
            # Apply item effects immediately or store in cargo
            if item_name == "Fuel Canister":
                ship.fuel = min(ship.fuel + 40, ship.max_fuel)
                print(f"  >> Fuel refilled! Fuel: {ship.fuel}/{ship.max_fuel}")
            elif item_name == "Laser Upgrade":
                ship.attack += 5
                print(f"  >> Laser upgraded! Attack is now {ship.attack}.")
            elif item_name == "Shield Booster":
                ship.shield += 3
                print(f"  >> Shield boosted! Shield is now {ship.shield}.")
            else:
                ship.collect_item(item_name)
            print(f"  >> Purchased '{item_name}' for {price} credits. Remaining: {ship.credits}")


# ============================================================
# GLOBAL DATA STRUCTURES
# ============================================================

# Tuple: Planet data — tuples are immutable, great for fixed data
# Each entry: (planet_name, description, fuel_cost, has_alien, has_loot)
PLANETS = (
    ("Earth Orbit",   "You leave Earth's atmosphere. Stars fill your viewport.",   5,  False, False),
    ("Mars",          "The red planet looms ahead. A Martian scout ship attacks!", 15, True,  True),
    ("Asteroid Belt", "Rocks everywhere! A Space Pirate ambushes you!",            20, True,  False),
    ("Jupiter",       "Gas giant! A massive alien cruiser emerges from the clouds.",25, True,  True),
    ("Kepler-22b",    "An alien homeworld. Their War Commander intercepts you!",   30, True,  True),
)

# Dictionary: ship type -> (attack_bonus, shield_bonus, starting_item, fuel_bonus)
SHIP_TYPES = {
    "Fighter": (6,  2, "Laser Upgrade",  0),
    "Scout":   (3,  1, "Fuel Canister",  20),
    "Hauler":  (2,  4, "Repair Kit",     0),
}

# List: possible random discoveries on safe planets
SPACE_DISCOVERIES = [
    "You spot a floating supply crate — it contains a Repair Kit!",
    "Cosmic radiation hits your hull — you lose 5 hull points.",
    "You receive a distress signal but it turns out to be a false alarm.",
    "A friendly alien trader gives you 15 bonus credits!",
    "You find an abandoned probe with ancient star maps. (+10 XP)",
    "A micro-meteor shower pings your hull but causes no damage.",
]

# List of alien types per planet index
ALIEN_NAMES = [
    None,                   # Earth Orbit — no alien
    "Martian Scout",
    "Space Pirate",
    "Jovian Cruiser",
    "Kepler War Commander",
]


# ============================================================
# FUNCTIONS
# ============================================================

def print_intro():
    """Print the game title screen. Uses: strings, print."""
    print("\n" + "*" * 50)
    print("        SPACE EXPLORER")
    print("    A Text-Based Space Adventure")
    print("*" * 50)
    print("\n  Your mission: Explore 5 planets,")
    print("  defeat alien threats, and return")
    print("  to Earth in one piece. Good luck!\n")


def get_valid_input(prompt, valid_choices):
    """
    Keep asking until user gives a valid answer.
    Uses: while loop (control loop), string, conditional, exception handling
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in valid_choices:
            return answer
        print(f"  >> Invalid input. Choose from: {valid_choices}")


def create_ship():
    """
    Ask player for ship name and type, return a Spaceship object.
    Uses: OOP, dictionary, list, for loop, string, exception handling
    """
    print("\n--- SHIP REGISTRATION ---")

    # Exception handling: blank name not allowed
    while True:
        name = input("Name your spaceship: ").strip()
        if name == "":
            print("  >> Ship name cannot be blank!")
        else:
            break

    # Show ship types from the dictionary
    print("\nChoose your ship type:")
    type_names = list(SHIP_TYPES.keys())    # dict keys -> list
    for i, stype in enumerate(type_names, start=1):
        atk, shld, item, fuel = SHIP_TYPES[stype]
        print(f"  {i}. {stype:<10} | +{atk} Attack, +{shld} Shield, starts with '{item}'" +
              (f", +{fuel} Fuel" if fuel else ""))

    choice = get_valid_input("Enter number (1/2/3): ", ["1", "2", "3"])
    chosen_type = type_names[int(choice) - 1]

    # Build ship and apply bonuses
    ship = Spaceship(name, chosen_type)
    atk, shld, start_item, fuel_bonus = SHIP_TYPES[chosen_type]
    ship.attack += atk
    ship.shield += shld
    ship.fuel = min(ship.fuel + fuel_bonus, ship.max_fuel)
    ship.collect_item(start_item)
    ship.collect_item("Repair Kit")    # Everyone starts with one repair kit

    print(f"\n  Launch sequence ready — welcome aboard, Captain!")
    ship.show_status()
    return ship


def spawn_alien(planet_index):
    """
    Create the right alien for each planet.
    Uses: conditionals, OOP, tuples (credit_range), integers
    Returns an Alien object.
    """
    if planet_index == 1:
        return Alien("Martian Scout",       hull=22, attack=7,  shield=1, xp_reward=18, credit_range=(8,  15))
    elif planet_index == 2:
        return Alien("Space Pirate",        hull=30, attack=10, shield=2, xp_reward=25, credit_range=(12, 22))
    elif planet_index == 3:
        return Alien("Jovian Cruiser",      hull=45, attack=13, shield=4, xp_reward=35, credit_range=(18, 30))
    else:
        return Alien("Kepler War Commander",hull=65, attack=17, shield=6, xp_reward=60, credit_range=(30, 50))


def combat(ship, alien):
    """
    Run a turn-based space battle.
    Uses: while loop, conditionals, OOP methods, random, float
    Returns: "won", "dead", or "escaped"
    """
    print(f"\n  *** SPACE BATTLE: {ship.name} vs {alien.name}! ***")
    print(f"  Alien Hull: {alien.hull}  |  Your Hull: {ship.hull}")

    # Control loop: while — fight until one side is destroyed
    while ship.is_operational and alien.is_alive:
        print("\n  What's your move?")
        print("    [1] Fire Lasers")
        print("    [2] Use Repair Kit")
        print("    [3] Attempt Warp Escape")

        move = get_valid_input("  Your choice: ", ["1", "2", "3"])

        if move == "1":
            # Float used here: random damage multiplier
            multiplier = random.uniform(0.85, 1.20)      # float: all data types
            damage = int(ship.attack * multiplier)
            print(f"  >> Firing lasers! {damage} base damage!")
            alien.take_damage(damage)

        elif move == "2":
            ship.use_repair_kit()

        elif move == "3":
            # 35% chance to warp away
            if random.random() < 0.35:
                print("  >> Warp drive engaged — you escaped!")
                return "escaped"
            else:
                print("  >> Warp drive failed! Couldn't escape!")

        # Alien fires back if still alive
        if alien.is_alive:
            alien_shot = random.randint(alien.attack - 2, alien.attack + 3)
            print(f"  >> {alien.name} fires back!")
            ship.take_damage(alien_shot)

    if not ship.is_operational:
        return "dead"

    # Victory
    credits_earned = alien.drop_credits()
    ship.credits += credits_earned
    ship.gain_experience(alien.xp_reward)
    print(f"\n  >> {alien.name} destroyed!")
    print(f"  >> Salvaged {credits_earned} credits and earned {alien.xp_reward} XP!")
    return "won"


def random_space_event(ship):
    """
    Trigger a random event in space.
    Uses: list, random.choice(), conditionals, string matching
    """
    event = random.choice(SPACE_DISCOVERIES)
    print(f"\n  *** Space Event: {event} ***")

    if "Repair Kit" in event:
        ship.collect_item("Repair Kit")
    elif "lose 5 hull" in event:
        ship.hull = max(ship.hull - 5, 1)
        print(f"  >> Hull is now {ship.hull}/{ship.max_hull}.")
    elif "15 bonus credits" in event:
        ship.credits += 15
    elif "+10 XP" in event:
        ship.gain_experience(10)


def dock_at_station(ship, planet_name):
    """
    Let the player shop at a space station.
    Uses: OOP, while loop, string, conditionals
    """
    station = SpaceStation(f"{planet_name} Station")
    print(f"\n  === Docking at {station.station_name} ===")
    print(f"  Your credits: {ship.credits}")

    docked = True
    while docked:
        station.display_stock()
        print("\n    [b] Buy something")
        print("    [d] Depart station")

        choice = get_valid_input("  Your choice: ", ["b", "d"])

        if choice == "b":
            item = input("  Enter item name: ").strip()
            station.purchase(ship, item)
        else:
            docked = False
            print("  >> Departing station. Safe travels!")


def visit_planet(ship, planet_index):
    """
    Handle everything that happens when landing on a planet.
    Uses: tuple unpacking, conditionals, functions, OOP
    Returns True if ship survives, False if destroyed.
    """
    planet_name, description, fuel_cost, has_alien, has_loot = PLANETS[planet_index]

    print(f"\n{'=' * 50}")
    print(f"  PLANET {planet_index + 1}: {planet_name.upper()}")
    print(f"  {description}")
    print(f"{'=' * 50}")

    # Burn fuel to travel there
    if planet_index > 0:
        ship.use_fuel(fuel_cost)
        if ship.fuel <= 0:
            print("\n  *** OUT OF FUEL! Stranded in space! GAME OVER ***")
            return False

    # Safe planet — random event instead of battle
    if not has_alien:
        random_space_event(ship)
        return True

    # Fight the alien
    alien = spawn_alien(planet_index)
    result = combat(ship, alien)

    if result == "dead":
        return False

    # Loot drop on certain planets
    if has_loot and result == "won":
        print("\n  *** You find wreckage to salvage! ***")
        loot_options = ["Repair Kit", "Fuel Canister", "Shield Booster", "Laser Upgrade"]
        loot = random.choice(loot_options)
        if loot == "Fuel Canister":
            ship.fuel = min(ship.fuel + 40, ship.max_fuel)
            print(f"  >> Salvaged a Fuel Canister! Fuel: {ship.fuel}/{ship.max_fuel}")
        elif loot == "Shield Booster":
            ship.shield += 2
            print(f"  >> Salvaged a Shield Booster! Shield: {ship.shield}")
        elif loot == "Laser Upgrade":
            ship.attack += 3
            print(f"  >> Salvaged a Laser Upgrade! Attack: {ship.attack}")
        else:
            ship.collect_item(loot)

    return True


def final_score(ship, victory):
    """
    Display the end-game summary.
    Uses: OOP, strings, boolean, integers, f-strings
    """
    print("\n" + "*" * 50)
    if victory:
        print("  *** MISSION COMPLETE! YOU MADE IT HOME! ***")
    else:
        print("  *** SHIP DESTROYED. MISSION FAILED. ***")
    print("*" * 50)

    ship.show_status()
    ship.show_cargo()

    # Calculate a final score — uses arithmetic and integers
    score = (ship.level * 200) + (ship.credits * 2) + ship.hull
    print(f"\n  FINAL SCORE : {score} points")
    print(f"  Final Level : {ship.level}")
    print(f"  Credits Left: {ship.credits}")
    print("\n  Thanks for playing Space Explorer!")


# ============================================================
# MAIN GAME LOOP
# ============================================================

def main():
    """
    The main game loop — ties everything together.
    Uses: functions, for loop (control loop), conditionals, OOP
    """
    print_intro()

    # Step 1: Create the player's ship
    ship = create_ship()

    input("\n  Press Enter to launch into space...")

    # Step 2: Control loop — for loop through each planet in the PLANETS tuple
    for planet_index in range(len(PLANETS)):

        # Offer docking at a space station every 2 planets (not at the very start)
        if planet_index > 0 and planet_index % 2 == 0:
            planet_name = PLANETS[planet_index][0]
            print(f"\n  A space station is in range near {planet_name}!")
            dock_choice = get_valid_input("  Dock and resupply? (y/n): ", ["y", "n"])
            if dock_choice == "y":
                dock_at_station(ship, planet_name)

        # Show current status before travel
        ship.show_status()
        input(f"\n  Press Enter to travel to {PLANETS[planet_index][0]}...")

        # Visit the planet
        survived = visit_planet(ship, planet_index)

        if not survived:
            final_score(ship, victory=False)
            return

        # Player can check cargo between planets
        cargo_choice = get_valid_input("\n  Check cargo hold? (y/n): ", ["y", "n"])
        if cargo_choice == "y":
            ship.show_cargo()

    # Survived all planets — return to Earth!
    print("\n  *** All planets explored! Setting course for Earth! ***")
    final_score(ship, victory=True)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
