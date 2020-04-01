from sys import stdout, getsizeof
from time import sleep
import random, json, time, os
import Map_builder as mb
import resources as res


###################
###################
#### FUNCTIONS ####
##   |   |   |   ##
##   |   |   |   ##
##   |   |   |   ##
##   V   V   V   ##
###################
###################

player = res.Player()
map = []

CURRENCY = "Ϟ"

SYNONYMS = {1 : ["inventory", "i"],
            2 : ["statistics", "stats", "stat"],
            3 : ["north", "n", "nort", "nor", "no"],
            4 : ["east", "e", "eas", "ea"],
            5 : ["south", "s", "sout", "sou", "so"],
            6 : ["west", "w", "wes", "we"],
            7 : ["go", "move", "walk", "run", "proceed", "advance"],
            8 : ["help", "commands", "moves"],
            9 : ["attack", "kill", "stab", "hit", "harm", "damage", "strike", "assault", "fight"],
            10 : ["save"],
            11 : ["observe"],
            12 : ["look", "describe", "inspect", "examine"],
            13 : ["talk", "address", "speak", "converse"],
            14 : ["eat", "consume", "ingest", "devour"],
            15 : ["take", "pick", "obtain", "get", "steal"],
            16 : ["open", "raid", "unlock"],
            17 : ["drop", "offload"]}

def parse(player, commands):
    for x in SYNONYMS.values():
        if commands[0] in x:
            return res.get_key(x, SYNONYMS)
    return None

def listToObj(obj, attrs):
    i = 0
    if obj.__class__.__name__ == "Monster":
        for x in attrs:
            print(x, type(x))
            print("\n")
    for attr, value in obj.__dict__.items():
        if type(attrs[i]) == int:
            setattr(obj, attr, int(attrs[i]))
        else:
            setattr(obj, attr, attrs[i])
        i += 1
    return obj

def jsonToList(obj):
    values = []
    for x, y in obj.items():
        values.append(y)
    return values

def loadGame():
    if os.stat("RPG_game_saves.json").st_size == 0:
        printOut("No games saved on this computer.")
    else:
        found = False
        with open("RPG_game_saves.json", "r+") as file:
            saves = json.load(file)

        printOut("What is the name of the save?")
        saveName = input(">>> ")

        while found == False:
            for attr, value in saves.items():
                if attr == saveName:
                    found = True

            if not found:
                printOut("Save name not found, try again?")
                answer = input(">>> ").lower()
                if answer not in ["yes", "y", "ye"]:
                    found = "End"
                else:
                    printOut("What is the name of the save?")
                    saveName = input(">>> ")

            if found == True:
                targetPlayer = saves[saveName][0]
                targetMap = saves[saveName][1]

                ## Load player data
                playerList = []
                for attr in list(targetPlayer.items())[1:]:
                    if attr[0] == "inventory":
                        temp = []
                        for item in attr[1]:
                            values = jsonToList(item)
                            obj = res.jsonToInstance([item])
                            add = listToObj(obj, values)
                            temp.append(add)
                        playerList.append(temp)
                    elif attr[0] == "weapon":
                        values = jsonToList(attr[1])
                        add = listToObj(res.Weapon(), values[1:])
                        playerList.append(add)
                    elif attr[0] == "shield":
                        if attr[1] == False:
                            playerList.append(False)
                        else:
                            values = jsonToList(attr[1])
                            add = listToObj(res.Shield(), values[1:])
                            playerList.append(add)
                    else:
                        playerList.append(attr[1])

                player = res.Player()
                i = 0
                for attr in list(player.__dict__.keys())[1:]:
                    setattr(player, attr, playerList[i])
                    i += 1

                ## Load map data
                decerealMap = []
                for cell in targetMap:
                    cellTemp = [list(cell.items())[0][1]]
                    for thing in list(cell.items())[1:]:
                        if thing[0] == "contains":
                            if type(thing[1]) == list:
                                temp = []
                                for item in thing[1]:
                                    values = jsonToList(item)
                                    add = listToObj(res.jsonToInstance([item]), values[1:])
                                    temp.append(add)
                                cellTemp.append(temp)
                            else:
                                temp = []
                                if len(thing[1]) != 0:
                                    for attr, value in thing[1].items():
                                        if attr == "selling":
                                            sellingDict = {}
                                            for good in value:
                                                values = jsonToList(value[good])
                                                add = listToObj(res.jsonToInstance([value[good]]), values[1:])
                                                sellingDict[good] = add
                                            temp.append(sellingDict)
                                        elif attr == "drops":
                                            values = jsonToList(value)
                                            add = listToObj(res.jsonToInstance([value]), values[1:])
                                            temp.append(add)
                                        elif attr == "contains":
                                            values = jsonToList(value)
                                            add = listToObj(res.jsonToInstance([value]), values[1:])
                                            temp.append(add)
                                        else:
                                            temp.append(value)

                                    if temp[0] == "Monster":
                                        adding = res.Monster()                                                
                                    elif temp[0] == "Chest":
                                        adding = res.Chest()
                                    else:
                                        adding = res.NPC()

                                    i = 1
                                    for attr in list(adding.__dict__.keys())[1:]:
                                        setattr(adding, attr, temp[i])
                                        i += 1
                                    cellTemp.append([adding])
                                else:
                                    cellTemp.append([])
                            if add.__class__.__name__ == "Monster":
                                add.getSynonyms()
                        else:
                            cellTemp.append(thing[1])
                    decerealMap.append(cellTemp)

                map = []
                for decerealCell in decerealMap:
                    if decerealCell[0] == "clearing":
                        cellObj = res.Clearing()
                    else:
                        cellObj = res.Path()

                    i = 1
                    #print(list(cellObj.__dict__.keys()), "keys")
                    #print(decerealCell, "valeues")
                    for attr in list(cellObj.__dict__.keys()):
                        setattr(cellObj, attr, decerealCell[i])
                        i += 1
                    map.append(cellObj)

                return True, player, map
    return False

def getJsonDumps(alist):
    if len(alist) == 0:
        currentDict = {}
    elif len(alist) == 1:
        currentDict = {"class" : alist[0].__class__.__name__}

    for obj in alist:
        for attr, value in obj.__dict__.items():
            if attr not in ["contains", "drops", "selling"]:
                if value.__class__.__name__ in ["Weapon", "Shield", "Money", "Key", "Food"]:
                    if value != False:
                        tempDict = {}
                        for x, y in value.__dict__.items():
                            tempDict[x] = y
                        currentDict[attr] = tempDict
                    else:
                        currentDict[attr] = value
                else:
                    currentDict[attr] = value
            elif attr == "selling":
                tempDict = {}
                for x, y in value.items():
                    jsonSellingDict = {}

                    jsonSellObj = getJsonDumps([y[0]])

                    tempDict[x] = jsonSellObj
                currentDict[attr] = tempDict
            else:
                jsonDumps = getJsonDumps([value] if attr == "drops" else value)
                currentDict[attr] = jsonDumps

    return currentDict

def saveGame(player, map):
    printOut("Enter a name for the save:")
    saveName = input(">>> ")

    if os.stat("RPG_game_saves.json").st_size == 0:
        saveNameAvaiable = True
    else:
        saveNameAvaiable = False

    while not saveNameAvaiable:
        with open("RPG_game_saves.json", "r+") as file:
            saves = json.load(file)
            for name, save in saves.items():
                if name == saveName:
                    printOut("That save name is already taken, please type a different one: ")
                    saveName = input(">>> ")
                    break
            else:
                saveNameAvaiable = True

    jsonMap = []
    for cell in map:
        if cell.__class__.__name__ == "Clearing":
            mapDict = {"class" : "clearing"}
        else:
            mapDict = {"class" : "path"}

        for attr, value in cell.__dict__.items():
            if attr != "contains":
                mapDict[attr] = value
            else:
                if len(value) == 1:
                    jsonDumps = getJsonDumps(value)
                    mapDict["contains"] = jsonDumps
                elif len(value) == 2:
                    jsonDump1 = getJsonDumps([value[0]])
                    jsonDump2 = getJsonDumps([value[1]])
                    mapDict["contains"] = [jsonDump1, jsonDump2]
                else:
                    mapDict["contains"] = getJsonDumps(value)

        jsonMap.append(mapDict)

    playerDict = {"class" : "player"}
    for attr, value in player.__dict__.items():
        if attr == "defaultValues":
            pass
        elif attr != "inventory":
            if attr == "shield":
                if value != False:
                    playerDict[attr] = getJsonDumps([value])
                else:
                    playerDict[attr] = False
            elif attr == "weapon":
                playerDict[attr] = getJsonDumps([value])
            else:
                playerDict[attr] = value
        else:
            temp = []
            for item in value:
                tempAdd = getJsonDumps([item])
                temp.append(tempAdd)
            playerDict[attr] = temp

    if os.stat("RPG_game_saves.json").st_size != 0:
        with open("RPG_game_saves.json", "r+") as file:
            loaded = json.load(file)
            for x, y in loaded.items():
                loaded[x] = y
            loaded[saveName] = [playerDict, jsonMap]

            add = json.dumps(loaded)
    else:
        add = json.dumps({saveName : [playerDict, jsonMap]}, indent=4)

    with open("RPG_game_saves.json", "w+") as file:
        file.write(add)

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

def checkDeath(player, monster):
    if player.HP <= 0:
        return "player"
    if monster.HP <= 0:
        return "monster"
    return False

def main(player, map):
    move = input(">>> ").lower().strip().split(" ")
    moveNum = parse(player, move)
    location = map[res.coordsToIndex(player.location)]
    currentMonsterPresent = False
    playerDead = False
    attackable = False

    for thing in location.contains:
        if thing.__class__.__name__ == "Monster":
            currentMonster = thing
            currentMonsterPresent = True

    if not playerDead:
        if moveNum == None:
            printOut("You cannot do that at the moment.")
        else:
            if moveNum == 1:
                printOut("Your inventory:")
                for i in player.inventory:
                    printOut(i.name + "\n", endNL=False)
                print("")
            elif moveNum == 2:
                printOut("Your current stats:\n\nHealth:  " + str(player.HP) + "\nStrength:  " + str(player.strength) + "\nLethality:  " + str(player.lethality) + "\nResistance:  " + str(player.resistance) + "\nMoney:  " + CURRENCY + str(player.money))
            elif moveNum == 3:
                player.move("0", map)
            elif moveNum == 4:
                player.move("1", map)
            elif moveNum == 5:
                player.move("2", map)
            elif moveNum == 6:
                 player.move("3", map)
            elif moveNum == 7:
                number = parse(player, [move[1]])
                player.move(str(number-3), map)
            elif moveNum == 8:
                printOut(helpScreen)
            elif moveNum == 9:
                monster = False
                for thing in location.contains:
                    if thing.__class__.__name__ == "Monster":
                        monsterObj = thing
                        monster = True

                if monster:
                    if move[1] in monsterObj.synonyms:
                        damage = player.attack()
                        monsterObj.defend(player, damage)
                        attackable = True
                    else:
                        if move[1] in ["me", "myself"]:
                            printOut("Suicide is never an option.")
                        else:
                            printOut("You make a valiant effort to kill the " + move[1] + " but, since there isn't one, you don't succeed.")
                else:
                    if move[1] in ["me", "myself"]:
                        printOut("Suicide is never an option.")
                    else:
                        printOut("You make a valiant effort to kill the " + move[1] + " but, since there isn't one, you don't succeed.")
            elif moveNum == 10:
                saveGame(player, map)
            elif moveNum == 11:
                if location.__class__.__name__ == "Clearing":
                    res.describeClearing(location)
                else:
                    res.describe(location)
            elif moveNum == 12:
                target = ""
                if len(move) == 1:
                    printOut("Please specify what you want to describe.")
                else:
                    if move[0] == "look":
                        if len(move[2:]) == 1:
                            target = move[-1]
                        else:
                            target = move[-2] + " " + move[-1]
                    else:
                        if len(move[1:]) == 1:
                            target = move[-1]
                        else:
                            for i in move[1:]:
                                target = move[-2] + " " + move[-1]

                    if target in ["area", "surroundings", "place", "surrounding", "environment"]:
                        if location.__class__.__name__ == "Clearing":
                            describeClearing(location)
                        else:
                            describe(location)
                    else:
                        final = False
                        for item in player.inventory:
                            if item.name.lower() == target:
                                final = item
                        for item in location.contains:
                            if target in item.synonyms:
                                final = item

                        if not final:
                            printOut("I can't see a " + target + " nearby.")
                        else:
                            printOut(final.description)
            elif moveNum == 13:
                if move[0] == "address":
                    playerTarget = move[1]
                elif move[0] != "address" and len(move) == 1:
                    printOut("You babble something incoherently.")
                elif move[0] != "address" and move[1] in ["to", "with"]:
                    printOut("What do you want to talk to?")
                    playerTarget = input(">>> ")
                else:
                    playerTarget = move[2]

                targets = []
                monstersTarg = []
                for i in location.contains:
                    if i.__class__.__name__ == "NPC":
                        targets.append(i)
                    elif i.__class__.__name__ == "Monster":
                        monstersTarg.append(i)

                if len(targets) == 0:
                    if len(monstersTarg) == 0:
                        if playerTarget in res.NPC({69 : "Nice"}).synonyms:
                            printOut("There is no one else to talk to here.")
                        else:
                            printOut(random.choice(["You talk to the " + playerTarget + " and nothing happens, strangely.",
                                                        "Why would you want to talk to that?",
                                                        "On the verge of madness, you attempt to make conversation with a " + playerTarget + "."]))
                    else:
                        if monsterTargs[0].poke():
                            printOut("Your words seem to provoke the " + monstersTarg[0].species + ".")
                            attackable = True
                        else:
                            printOut("The " + monstersTarg[0].species + " grunts at you incoherently.")
                else:
                    talked = False
                    for person in targets:
                        if playerTarget in person.synonyms:
                            person.interact(player)
                            talked = True

                    if not talked:
                        if playerTarget in ["me", "myself"]:
                            printOut(random.choice(["Your voice echoes around the forest.",
                                                    "You talk to yourself, no one hears you.",
                                                    "I'm not sure what that achieved."]))
                        else:
                            printOut(random.choice(["You talk to the " + playerTarget + " and nothing happens, strangely.",
                                                    "I don't think that would achieve anything.",
                                                    "On the verge of madness, you attempt to make conversation with a " + playerTarget + "."]))
            elif moveNum == 14:
                target = []
                for i in player.inventory:
                    if i.__class__.__name__ == "Food":
                        target.append(i)

                eaten = False
                for food in target:
                    if move[1] in food.synonyms:
                        food.eat(player)
                        eaten = True

                if not eaten:
                    if move[1] in ["me", "myself"]:
                        printOut(random.choice(["I don't think autocannibalism is the way forward.",
                                                "Autocannibalism won't get you anywhere.",
                                                "Autosarcophagy doesn't help anyone, you know."]))
                    else:
                        printOut(random.choice(["I don't think that would be good for you.",
                                                "10/10 doctors recommend you don't do that."]))
            elif moveNum == 15:
                target = 0
                if move[0] == "pick":
                    if len(move[2:]) == 1:
                        target = move[-1]
                    else:
                        target = move[-2] + " " + move[-1]
                else:
                    if len(move[1:]) == 1:
                        target = move[-1]
                    else:
                        for i in move[1:]:
                            target = move[-2] + " " + move[-1]

                actual = "hmmm"

                for item in location.contains:
                    if target in item.synonyms:
                        actual = item

                if actual == "hmmm":
                    if target in res.Money("hi", "bye").synonyms:
                        printOut("I can't see any money here.")
                    else:
                        printOut("I can't see a " + target + " here.")
                else:
                    if actual.__class__.__name__ in ["Monster", "NPC", "Chest"]:
                        printOut("I'm not sure that would fit in your bag.")
                    else:
                        player.pickUp(actual, location.contains)
            elif moveNum == 16:
                chestPresent = False
                for thing in location.contains:
                    if thing.__class__.__name__ == "Chest":
                        chestPresent = True
                        target = thing

                if move[1] not in res.Chest(1,2).synonyms:
                    printOut("I'm not sure its possible to " + move[0] + " a " + move[1] + ".")
                else:
                    if not chestPresent:
                        printOut("I can't see a chest nearby.")
                    else:
                        if target.locked:
                            target.unlock(player, location)
                        else:
                            target.plunder(player)
            elif moveNum == 17:
                actual = False
                for thang in player.inventory:
                    if move[1] in thang.synonyms:
                        actual = move[1]

                if actual != False:
                    player.inventory.remove(actual)
                    location.contains.append(actual)
                    printOut("Dropped " + actual.name + ".")
                else:
                    printOut("There isn't a " + move[1].name + " in your inventory which you can drop.")

    if currentMonsterPresent:
        check = checkDeath(player, currentMonster)
        if check == "player":
            playerDead = True
            player.die(currentMonster, selfKilled=True)
        elif check == "monster":
            currentMonster.die(player, location, playerKilled=True)
            currentMonsterPresent = False

    if currentMonsterPresent:
        if attackable:
            damage = currentMonster.attack(player)
            player.defend(currentMonster, damage)

        check = checkDeath(player, currentMonster)
        if check == "player":
            playerDead = True
            player.die(currentMonster)
        elif check == "monster":
            currentMonster.die(player, location)

def startGame(map, player):
    if player == False:
        #printOut("What is your name?")
        #name = input(">>> ")
        name = "1"
        player = res.Player(name)

        i = 0
        for thing in list(player.__dict__.keys())[2:]:
            setattr(player, thing, player.defaultValues[i])
            i += 1

        #printOut("Welcome " + name  + ".")


    if len(map) == 0:
        map = mb.generateMap()

    location = map[res.coordsToIndex(player.location)]
    #if location.__class__.__name__ == "Clearing":
    #    res.describeClearing(location)
    #else:
    #    res.describe(location)

    while True:
        main(player, map)

#####################
#####################
####  MAIN GAME  ####
###   |   |   |   ###
###   |   |   |   ###
###   V   V   V   ###
#####################
#####################

commands = """\n            ---- PLAY ----
            ---- HELP ----
            ---- LOAD ----"""

helpScreen = """\nA list of useful commands:
-- Save                  - Save the current gamestate for later use.
-- Inventory / i         - Displays what you are currently holding.
-- Stats                 - Lists your current statistics.
-- Observe               - Describes your surroundings in detail.
-- Look at [item]        - Look at a specific thing in your inventory or in the surroundings.
-- Take/Pick up [item]   - Add an item to your inventory, as long as you have enough room.
-- Drop [item]           - Drop an item from your inventory onto the floor.
-- Talk to [person]      - Starts a conversation with the specified person.
-- Attack [monster]      - Attacks the specified monster with whatever weapon you are currently holding.
-- North/East/South/West - Move in the specified direction.
     n / e / s / w

Multiple other commands can also be understood, type what you want to do and see if the program understands.
N.B. Please describe items using only one or two words to avoid the game getting confused."""

#printOut(commands)
answer = input(">>> ").lower()
start = False

while not start:
    if answer == "play":
        start = True
        startGame(map, False)
    elif answer == "help":
        printOut(helpScreen, pause=0.02)
        answer = input(">>> ")
    elif answer == "load":
        loaded, player, map = loadGame()
        if loaded:
            start = True
            startGame(map, player)
        else:
            printOut(commands, pause=0.02)
            answer = input(">>> ").lower()
    else:
        printOut("Sorry, I don't understand that command.")
        answer = input(">>> ")

##startGame()
