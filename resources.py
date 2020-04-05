from sys import stdout, exit
from time import sleep
import random
CURRENCY = "Ϟ"

monsterAdjectives = ["A mean-looking", "A violent-looking", "An aggressive-looking", "An intimidating", "A blood soaked", "A battle scarred", "A vicious-looking"]
noMoveDescs = ["Dense forest stops you from moving in that direction.",
                "Thick brambles prevent you from entering that part of the forest.",
                "A sheer cliff stops you from moving that way.",
                "Fallen boulders and debris are blocking that path."]

def printOut(*args, pause=0.03, startNL=False, endNL=True):
    if startNL:
        print("\n")

    for arg in args:
        for letter in arg:
            stdout.write(letter)
            stdout.flush()
            sleep(pause)

    if endNL:
        print("\n")

def get_key(val, dictionary):
    for x, y in dictionary.items():
        if y == val:
            return x
    return False

def coordsToIndex(coords):
    return coords[0]*5 + coords[1]

def jsonToInstance(jsonList): ## Returns an instance of the object from a json dict
    target = jsonList[0]["class"]

    if target == "Shield":
        return Shield()
    if target == "Weapon":
        return Weapon()
    if target == "Money":
        return Money()
    if target == "Food":
        return Food()
    if target == "Key":
        return Key()
    if target == "Monster":
        return Monster()
    if target == "Chest":
        return Chest()
    if target == "Clearing":
        return Clearing()
    if target == "Path":
        return Path()

def describe(obj): ## Not used with Clearing
    printOut(obj.description)
    if obj.__class__.__name__ == "Path":
        if obj.code != False:
            printOut("Scratched into the mud on the floor you can make out four numbers.\n", endNL=False)
            for num in str(obj.code):
                print("..." + str(num) + "...")
                sleep(0.5)

        for ting in obj.contains:
            if ting.__class__.__name__ == "NPC":
                printOut("A merchant stands by the side of the road, offering to buy and sell goods.")

def describeClearing(clearing): ## Only used with Clearing
    printOut(clearing.description)

    for ting in clearing.contains:
        if ting.__class__.__name__ == "Monster":
            printOut(random.choice(monsterAdjectives) + " " + ting.species + ", named " + ting.name + " is watching you menacingly.")
        elif ting.__class__.__name__ == "Chest":
            printOut("A small, wooden chest lies in the middle of the clearing.")
        else:
            printOut("A " + ting.name + " lies on the floor.")

class NPC:
    def __init__(self, selling=False):
        self.selling = selling
        self.synonyms = ["merchant", "npc", "shop", "man", "person", "woman"]
        self.description = "A humble merchant, offering to buy or sell food, weapons and armour."

    def interact(self, player):
        printOut("Type 1 to buy from the merchant.\nType 2 to sell to the merchant.\nType 3 to go back.")
        answer = input(">>> ")

        while answer not in ["1", "2", "3"]:
            printOut("I'm not sure I understand.")
            printOut("Type 1 to buy from the merchant.\nType 2 to sell to the merchant.\nType 3 to go back.")
            answer = input(">>> ")

        if answer == "1":
            r = "QWERTY"
            printOut("I'm selling:\n", endNL=False)
            for cost, item in self.selling.items():
                printOut(item[0].name + "(x" + str(item[1]) + ") - " + CURRENCY + str(cost) + " each.\n", endNL=False)
            printOut("\nWhat would you like to buy?")
            item = input(">>> ")
            found = False
            for x in self.selling.values():
                if item.lower().strip() == x[0].name.lower():
                    found = True
                    actual = x

            if found:
                price = get_key(actual, self.selling)

                printOut("How many would you like? (Type 0 to exit)")
                quantity = int(input(">>> "))

                while quantity > actual[1] or player.money - (price * quantity) < 0:
                    if quantity > actual[1]:
                        printOut("I don't have that many " + actual[0].name + "s.")
                        printOut("How many would you like? (Type 0 to exit)")
                        quantity = int(input(">>> "))
                    else:
                        printOut("You don't have enough money to buy that many.")
                        printOut("How many would you like? (Type 0 to exit)")
                        quantity = int(input(">>> "))

                if quantity != 0:
                    for i in range(1,quantity+1):
                        player.pickUp(actual[0],False)
                        player.money -= price
                        actual[1] -= 1
                        if actual[1] == 0:
                            self.selling.pop(price)
                    if quantity > 1:
                        printOut(str(quantity) + " " + actual[0].name + "s added to inventory.")
                    else:
                        printOut(actual[0].name + " added to inventory.")
                    printOut("Buy or sell something else?")
                    r = input(">>> ")
                else:
                    printOut("Buy or sell something else?")
                    r = input(">>> ")
            else:
                printOut("Sorry, I'm not selling that.")
                printOut("Buy or sell something else?")
                r = input(">>> ")

            if r in ["yes", "ye", "y"]:
                self.interact(player)
            else:
                printOut("Goodbye then.")

        elif answer == "2":
            printOut("What would you like to sell?")
            selling = input(">>> ")
            r = "L"

            found = False
            for item in player.inventory:
                if selling.lower() in item.synonyms:
                    actual = item
                    found = True

            if not found:
                printOut("You don't have one of those in your inventory.")
                self.interact(player)
            else:
                printOut("I'll buy each " + actual.name + " for " + CURRENCY + str(actual.cost) + ".\nDo you want to continue?")
                answer = input(">>> ").lower()
                if answer in ["yes", "y", "ye"]:
                    number = 0
                    for item in player.inventory:
                        if item.name == actual.name:
                            number += 1

                    printOut("How many do you want to sell? (You have " + str(number) + ")")
                    quantity = int(input(">>> "))
                    while quantity > number:
                        printOut("You don't have that many.")
                        printOut("How many would you like to sell?")
                        quantity = int(input(">>> "))

                    for i in range(0,quantity):
                        player.inventory.remove(actual)

                        found = False
                        for item in self.selling.values():
                            if item[0] == actual:
                                item[1] += 1
                                found = True
                        if not found:
                            self.selling[actual.cost+10] = [actual, 1]

                        a = actual.__class__.__name__
                        if a == "Shield":
                            player.shield = False
                        elif a == "Weapon":
                            player.weapon = Weapon("Fist", "They're your hands. What more do you want to know?", ["hands", "fists", "knuckles"], 0, "Body", 0, 0)
                        player.money += actual.cost

                    printOut("Sold!\nYou now have " + CURRENCY + str(player.money) + ".")
                    printOut("Buy or sell something else?")
                    r = input(">>> ")
                else:
                    printOut("Ok then, would you like to buy or sell something else?")
                    r = input(">>> ")

                if r.lower() in ["yes", "ye", "y"]:
                    self.interact(player)
                else:
                    printOut("Goodbye then.")

        elif answer == "3":
            printOut("Have a nice day.")

class Monster:
    def __init__(self, name=False, description=False, HP=False, lethality=False, resistance=False, drops=False, species=False, weapon=False, aggro=False, shield=False):
        self.name = name
        self.description = description
        self.HP = HP
        self.lethality = lethality
        self.resistance = resistance
        self.drops = drops
        self.species = species
        self.weapon = weapon
        self.aggro = aggro
        self.shield = shield

        self.synonyms = []

    def getSynonyms(self):
        self.synonyms = [self.name.lower(), self.species.lower(), "monster"]

    def attack(self, player):
        if random.randint(1, 6-self.aggro) == 1:
            multiplier = self.weapon.generateCrit()
            damage = self.lethality * multiplier
        else:
            damage = 0
        return damage

    def printRebound(self, player):
        printOut(random.choice(["You block the " + self.species + "'s " + self.weapon.name + " with your shield, sending a shock through its arm.",
                                "The " + self.species + "'s " + self.weapon.name + " bounces off your shield and collides with its shoulde",
                                "The " + self.species + "'s wrist snaps as its " + self.weapon.name + " is stopped abruptly by your shield."]) + "\n", endNL=False)

    def defend(self, player, damage):
        self.takeDamage = ["Your " + player.weapon.name + " connects with the monster's shoulder, causing a deep cut.",
                            "You strike the " + self.species + " in the side of the head, causing a torrent of blood to flow.",
                            "The " + self.species + " staggers as you sweep its legs with your " + player.weapon.name + ".",
                            "A blow to the chest of the " + self.species + " causes it to fall to one knee before clambering back to its feet.",
                            "The " + self.species + " grunts as your " + player.weapon.name + " collides with its stomach."]

        self.dodge = ["The " + self.species + " sees your attack coming and nimbly dodges out of the way",
                        "Anticipating an attack, the " + self.species + " steps out of the path of your " + player.weapon.name + ".",
                        "With unexpected ease, " + self.name + " dances away from your " + player.weapon.name + ".",
                        "Your " + player.weapon.name + " brushes past the " + self.species + "'s head but it does no damage."]

        crit = 1
        if self.shield != False:
            crit = self.shield.generateCrit()

        if crit == 1:
            if random.randint(1,40-self.resistance) == 1:
                crit = 2

        if crit == 1:
            total = damage - self.resistance + random.randint(-4,4)
            printOut(random.choice(self.takeDamage))
            printOut("It loses " + str(total) + " HP")
            self.HP -= total
        elif crit == 2:
            printOut(random.choice(self.dodge))
        else:
            total = -random.randint(1,self.shield.strength)
            player.printRebound(self)
            print("You lose " + str(-total) + " HP.")
            player.HP += total

    def poke(self, player):
        if random.randint(1, 6-self.aggro) == 1:
            return True
        return False

    def die(self, player, location, playerKilled=True):
        self.death = []

        if playerKilled:
            printOut("As your last blow connects, the " + self.species + " disappears into a cloud of thick, black smoke.")
        else:
            printOut("The shock from the self-inflicted damage to the " + self.species + " causes it to collapse to the floor, disappearing into a thick cloud of black smoke.")

        location.contains.remove(self)
        location.contains.append(self.drops)
        location.contains.append(self.weapon)
        if self.shield != False:
            location.contains.append(self.shield)

        if self.drops.__class__.__name__ == "Money":
            printOut("Where the " + self.species + " once stood, a small bag of money now lies.")
        else:
            printOut("Where the " + self.species + " once stood, a " + self.drops.name + " now lies.")
        if self.shield != False:
            location.contains.append(self.shield)
            printOut("The " + self.species + "'s " + self.weapon.name + " lies on the floor along with its shield.")
        else:
            printOut("The " + self.species + "'s " + self.weapon.name + " now lies on the floor")

class Shield:
    def __init__(self, name=False, description=False, synonyms=False, critChance=False, strength=False, weight=False, cost=False):
        self.name = name
        self.description = description
        self.synonyms = synonyms
        self.critChance = critChance
        self.strength = strength
        self.weight = weight
        self.cost = cost

    def generateCrit(self):
        if random.randint(1, 15-self.critChance) == 1:
            return 2
        elif random.randint(1, 25-self.critChance) == 1:
            return 3
        else:
            return 1

class Weapon:
    def __init__(self, name=False, description=False, synonyms=False, critChance=False, group=False, weight=False, cost=False):
        self.name = name
        self.description = description
        self.synonyms = synonyms
        self.critChance = critChance
        self.group = group
        self.weight = weight
        self.cost = cost

    def generateCrit(self):
        if random.randint(1, 15-self.critChance) == 1:
            return 1.5
        elif random.randint(1, 25-self.critChance) == 1:
            return 2
        else:
            return 1

class Chest:
    def __init__(self, contains=False, locked=False, unlockCode=False, unlockKey=False):
        self.contains = [contains]
        self.locked = locked
        self.unlockCode = unlockCode
        self.unlockKey = unlockKey
        self.synonyms = ["box", "chest", "container", "crate"]
        self.description = "An old but sturdy chest, it looks like it could contain something valuable."

    def unlock(self, player, location):
        if not self.locked:
            printOut("This chest is not locked.")
        else:
            if self.unlockCode != False:
                print(self.unlockCode)
                printOut("The padlock on this chest must be unlocked with a code.\nWhat is the code?")
                answer = input(">>>")
                try:
                    int(answer)
                    integer = True
                except:
                    integer = False

                if integer:
                    if int(answer) == self.unlockCode:
                        self.locked = False
                        printOut("Correct, the padlock on the chest clicks open.")
                        self.open()
                    else:
                        printOut("Incorrect! Try again?")
                        answer = input(">>> ").lower()
                        if answer == "yes" or answer == "y":
                            self.unlock(player, location)
                else:
                    printOut("Incorrect! Try again?")
                    answer = input(">>> ").lower()
                    if answer == "yes" or answer == "y":
                        self.unlock(player, location)
            elif self.unlockKey != False:
                printOut("The padlock on this chest must be unlocked with the " + self.unlockKey.name + ".")
                ##if self.unlockKey in player.inventory:
                if True:
                    printOut("Unlock the chest?")
                    answer = input(">>> ").lower()
                    if answer == "yes" or "y":
                        self.locked = False
                        printOut("The padlock on the chest clicks open.")
                        self.open()
                    else:
                        printOut("Come back later if you do.")
                else:
                    printOut("You don't have that key. Come back later when you do.")

    def open(self):
        if self.contains.__class__.__name__ == "Money":
            printOut("The chest contains a bag of coins worth " + self.contains.name + ".")
        else:
            printOut("The chest contains a " + self.contains.name + ".")

    def plunder(self, player):
        if self.locked:
            printOut("This chest is locked, unlock it to access what's inside.")
        else:
            if self.contains == "Empty":
                printOut("This chest is empty.")
            else:
                self.open()
                printOut("Do you want to pick up the " + self.contains.name + "?")
                answer = input(">>> ").lower()

                if answer in ["yes", "ye", "y"]:
                    player.pickUp(self.contains, container=False)
                    self.contains = "Empty"
                else:
                    printOut("Come back later if you do.")

class Money:
    def __init__(self, name=False, value=False):
        self.name = name
        self.value = value
        self.synonyms = ["gold", "money", "coins", "cash"]

class Food:
    def __init__(self, name=False, description=False, synonyms=False, HP=False, weight=False, cost=False):
        self.name = name
        self.description = description
        self.synonyms = synonyms
        self.HP = HP
        self.weight = weight
        self.cost = cost

    def eat(self, player):
        if self.HP > 0:
            printOut("You eat the " + self.name + ". Your health increases by " + str(self.HP) + " points.")
            player.HP += self.HP
            printOut("You now have " + str(player.HP) + " health points.")
        else:
            printOut("You eat the " + self.name + ". Your health drops by " + str(self.HP) + " points.")
            player.HP -= self.HP
            printOut("You now have " + str(player.HP) + " health points.")

class Player:
    def __init__(self, name=False):
        self.defaultValues = [[0,0],
                              [Food("Apple", "Shiny fruit", ["apple"], 20, 5, 10)],
                              0,
                              50,
                              100,
                              15,
                              15,
                              100,
                              Shield("Wooden Shield", "woooood", ["shield"], 2, 20, 20, 75),
                              Weapon("Fist", "They're your hands. What more do you want to know?", ["hands", "fists", "knuckles"], 0, "Body", 0, 0)]
        self.name = name
        self.location = False
        self.inventory = [Key("Gold Key", 5, 50), Key("Silver Key", 5, 50), Key("Bronze Key", 5, 50)]
        self.inventoryWeight = False
        self.HP = False
        self.strength = False
        self.lethality = False
        self.resistance = False
        self.money = False
        self.shield = False
        self.weapon = False

    def move(self, index, map):
        moved = False
        if index == "0": ## North
            if self.location[0] - 1 < 0:
                printOut(random.choice(noMoveDescs))
            else:
                self.location[0] -= 1
                moved = "north"
        elif index == "1": ## East
            if self.location[1] + 1 >= 5:
                printOut(random.choice(noMoveDescs))
            else:
                self.location[1] += 1
                moved = "east"
        elif index == "2": ## South
            if self.location[0] + 1 >= 5:
                printOut(random.choice(noMoveDescs))
            else:
                self.location[0] += 1
                moved = "south"
        elif index == "3": ## West
            if self.location[1] - 1 < 0:
                printOut(random.choice(noMoveDescs))
            else:
                self.location[1] -= 1
                moved = "west"

        if moved != False:
            location = map[coordsToIndex(self.location)]
            if location.__class__.__name__ == "Clearing":
                describeClearing(location)
            else:
                describe(location)

    def attack(self):
        multiplier = self.weapon.generateCrit()
        damage = self.lethality * multiplier

        return damage

    def printRebound(self, monster):
        printOut(random.choice(["The " + monster.species + "'s shield absorbs your blow and sends a jolt through your body.",
                                "Your " + self.weapon.name + " bounces off the " + monster.species + "'s shield and strikes your torso.",
                                "The " + monster.species + " blocks your attack with its shield, causing a jarring shock through your arm."]) + "\n", endNL=False)

    def defend(self, monster, damage):
        self.takeDamage = ["The " + monster.species + "'s " + monster.weapon.name + " strikes your chest, winding you and knocking you back.",
                            "You stagger backwards as the " + monster.species + "'s " + monster.weapon.name + " connects with your knee.",
                            "The " + monster.species + "'s " + monster.weapon.name + " smashes into your head, filling your vision with black stars.",
                            "The " + monster.weapon.name + " of the " + monster.species + " hits your forehead. You are temporarily blinded by a torrent of blood.",
                            "You are knocked to the ground by the " + monster.species + "'s " + monster.weapon.name + ", but you manage to slowly regain your footing."]

        self.dodge = ["Somehow you manage to dodge the " + monster.species + "'s attack and you take no damage.",
                        "An unseen force pushes you out of the path of the " + monster.species + "'s " + monster.weapon.name + ".",
                        "With remarkable grace, you roll away from " + monster.name + "'s " + monster.weapon.name + ".",
                        "The " + monster.species + "'s " + monster.weapon.name + " whistles past your ear but you escape unscathed. For now."]

        crit = 1
        if self.shield != False:
            crit = self.shield.generateCrit()

        if crit == 1:
            if random.randint(1,40-self.resistance) == 1:
                crit = 2

        if crit == 1:
            total = damage - self.resistance + random.randint(-4,4)
            printOut(random.choice(self.takeDamage))
            printOut("You lose " + str(-total) + " HP")
            self.HP += total
        elif crit == 2:
            printOut(random.choice(self.dodge))
        else:
            total = -random.randint(1,self.shield.strength)

            monster.printRebound(self)
            print("The " + monster.species + " loses " + str(-total) + " HP.")
            monster.HP += total

    def pickUp(self, target, container=False, display=True):
        if target.name[0] == CURRENCY:
            self.money += target.value
            printOut(CURRENCY + str(target.value) + " added to balance.\nYou now have " + CURRENCY + str(self.money))
        elif target.__class__.__name__ == "Weapon":
            self.weapon = target

            for item in self.inventory:
                if item.__class__.__name__ == "Weapon":
                    self.inventory.remove(item)

            self.inventory.append(target)
            self.inventoryWeight += target.weight
            if display:
                printOut(target.name + " added to your inventory.")
        elif target.__class__.__name__ == "Shield":
            self.shield = target

            for item in self.inventory:
                if item.__class__.__name__ == "Shield":
                    self.inventory.remove(item)

            self.inventory.append(target)
            self.inventoryWeight += target.weight
            if display:
                printOut(target.name + " added to your inventory.")
        else:
            if self.inventoryWeight + target.weight > self.strength:
                printOut("You are not strong enough to carry that.\nDrop something else first.")
            else:
                self.inventory.append(target)
                self.inventoryWeight += target.weight
                if display:
                    printOut(target.name + " added to your inventory.")

        if container != False:
            container.remove(target)

    def die(self, monster, selfKilled=False):
        if selfKilled:
            printOut("You tried your hardest to defeat the " + monster.species + " but in the end, you caused your own demise.\n", endNL=False)
        else:
            printOut("Despite your best efforts to defeat the " + monster.species + ", it easily overpowers you.\n", endNL=False)
        printOut("You drop to the ground as your vision slowly fades to black.", pause=0.04)

        score = self.lethality + self.resistance + self.money + self.strength
        printOut("\nFinal score: " + str(score))

        printOut("Game design and creation by Max Waring.\nThank you for playing.")
        exit()

class Path:
    def __init__(self, contains=False, code=False):
        self.description = "You are on a small muddy track which leads into the forest in all directions."
        self.contains = contains
        self.code = code

class Clearing:
    def __init__(self, description=False, contains=False):
        self.description = description
        self.contains = contains

    def describe(self):
        printOut(self.descriptions[self.state])

class Key:
    def __init__(self, name=False, weight=False, cost=False):
        self.name = name
        self.weight = weight
        self.cost = cost
