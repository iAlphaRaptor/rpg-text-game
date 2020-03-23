import resources as res, random
from sys import getsizeof


codes = [random.randint(1111,9999), random.randint(1111,9999)]
NPCs = []
chests = []
monsters = [res.Monster("Ba'kha", "An imposing dwarf, wearing dirty leather armour and brandishing a club.",100,10,7,res.Money(res.CURRENCY+"100",100),"dwarf",res.Weapon("Club","A thick, gnarled club, hewn from ancient oak.",["club"],5,"clubs",23,75),3,False),
            res.Monster("Grilgil", "An aggressive dwarf, stark naked but brandishing a mean-looking mace.",100,20,6,res.Money(res.CURRENCY+"100",100),"dwarf",res.Weapon("Mace", "A crude mace, the spiked ball look like it would do some damage.",["mace"],8,"mace",30,95),3,False),
            res.Monster("Chak'gor", "A battle-scarred orc, clad in bear skin and brandishing a dwarven blade.",175,20,13,res.Key("Bronze Key",5,20),"orc",res.Weapon("Dwarven Sword","A beautiful long-sword, evidently made by a master craftsman.",["dwarf sword","dwarven sword","dwarven blade"],9,"swords",25,125),2,res.Shield("Wooden Shield", "A basic shield made of thin wood planks.", ["wood shield", "wooden shield"],6,10,25,80)),
            res.Monster("Moblex", "A grimacing orc, adorned with beautiful armour and holding a shining axe.",175,15,17,res.Food("Golden Apple","A glittering apple, covered in pure gold.",["golden apple","gold apple"],40,8,50),"orc",res.Weapon("Metal Axe","A sturdy tomohawk with a jagged metal blade.",["metal axe"],5,"axe",27,85),3,res.Shield("Wooden Shield", "A basic shield made of thin wood planks.", ["wood shield", "wooden shield"],6,10,25,80)),
            res.Monster("Ta'chala", "A sly goblin wearing a small dagger at his belt and watching you with suspicion.",100,12,6,res.Money(res.CURRENCY+"100",100),"goblin",res.Weapon("Dagger","A small metal dagger with a precious jewel embedded in the handle.",["dagger"],6,"knife",16,85),2,False),
            res.Monster("Thali", "An elvish soldier, heavily armoured and brandishing a silver spear menacingly.",150,20,18,res.Key("Golden Key",5,50),"elf",res.Weapon("Silver Spear","A perfectly balanced spear, its taller than you and adorned with what looks like ivy leaves.",["silver spear"],9,"spear",30,125),4,res.Shield("Elven Shield","A beautiful, shield covered in depictions of a bygone era.",["elven shield","elf shield"],9,14,32,120)),
            res.Monster("Gaumus", "A towering giant. A massive hammer swings by his side.",200,17,16,res.Money(res.CURRENCY+"200",200),"giant",res.Weapon("Hammer","A nordic-style hammer, made of solid titanium and engraved with mystic runes.",["hammer"],7,"hammer",35,100),4,res.Shield("Wooden Shield", "A basic shield made of thin wood planks.", ["wood shield","wooden shield"],6,10,25,80)),
            res.Monster("Ulkith", "An important-looking dwarf, dressed in regal but heavily reinforced robes. He is leaning on a long broadsword.",150,18,13,res.Key("Gold Key", 5, 50),"elf",res.Weapon("Broadsword","A long and heavy sword, unwieldy to anyone not incredibly strong.",["broadsword"],9,"sword",40,110),3,False),
            res.Monster("Hallutarg", "A deformed troll, hunched over a gnarled staff.",150,14,7,res.Money(res.CURRENCY+"100",100),"troll",res.Weapon("Staff","The gnarled branch of an elder tree, carved into a makeshift weapon.",["staff","stick"],4,"clubs",19,40),3,False),
            res.Monster("Nightlin", "A dark and mysterious figure, wearing a long, black cloak and holding a scythe.",200,20,15,res.Food("Health Orb", "A swirling purple orb. It looks like it would restore a lot of HP.",["health orb","orb"],100,5,100),"ghost",res.Weapon("Scythe","A cruel scythe, with a long mahogany handle and a curved blade.",["scythe"],10,"scythe",29,150),5,False)]
paths = []
clearings = []
map = []

### NPC generator
NPCselling =   [[random.randint(30, 40), [res.Food("Apple","A shiny, red apple.",["apple"],20,7,33), random.randint(1,4)]],
                [random.randint(12, 25), [res.Food("Mushroom","A small, brown mushroom.\nIt looks edible.",["mushroom","fungus"],10,5,15), random.randint(1,4)]],
                [random.randint(30, 40), [res.Food("Banana","A slightly bruised but ripe banana.",["banana"],22,7,35), random.randint(1,4)]],
                [random.randint(42, 60), [res.Food("Bread","A small loaf of white bread.",["bread","loaf"],30,9,40), random.randint(1,3)]],
                [random.randint(42, 60), [res.Food("Ham","A haunch of cooked pork.",["pork","meat","haunch","ham"],35,10,40), random.randint(1,3)]],
                [random.randint(45, 65), [res.Food("Sandwich","Two pieces of bread and a few slices of cheese.",["sandwich"],40,9,40), random.randint(1,3)]],
                [random.randint(10, 17), [res.Food("Root","It appears to be some sort of edible root.",["root"],10,4,7), random.randint(1,4)]],
                [random.randint(110, 125), [res.Weapon("Bronze Sword","A dull, heavy sword made of bronze.",["bronze sword"],7,"swords",25,100), 1]],
                [random.randint(155, 170), [res.Weapon("Gold Sword","A shiny, ornate sword crafted from pure gold.",["gold sword"],10,"swords",35,150), 1]],
                [random.randint(75, 90), [res.Weapon("Club","A thick, gnarled club, hewn from ancient oak.",["club"],5,"clubs",23,75), 1]],
                [random.randint(80, 95), [res.Weapon("Stone Axe","A primative axe made from a sharpened stone.",["stone axe"],8,"axes",23,80), 1]],
                [random.randint(200, 225), [res.Weapon("Katana","A lithe, elegant sword crafted from crude steel.",["katana"],12,"swords",32,200), 1]],
                [random.randint(80, 100), [res.Shield("Wooden Shield", "A basic shield made of thin wood planks.", ["wood shield", "wooden shield"],6,10,25,80), 1]],
                [random.randint(95, 110), [res.Shield("Metal Shield", "A strong, metal shield, embossed with bronze symbols.", ["metal shield"],9,15,30,95), 1]],
                [random.randint(130, 150), [res.Shield("Diamond Shield", "A glittering shield crafted from purest crystal.", ["diamond shield"],12,20,35,130), 1]]]

for i in range(3):
    sellingNum = random.randint(3,5)
    currentSell = {}
    for j in range(sellingNum):
        chosen = random.choice(NPCselling)
        NPCselling.remove(chosen)
        currentSell[chosen[0]] = chosen[1]
    NPCs.append(res.NPC(currentSell))


### Chest generator
chestContains1 = [res.Food("Apple","A shiny, red apple.",["apple"],20,7,33),
                  res.Food("Mushroom","A small, brown mushroom.\nIt looks edible.",["mushroom","fungus"],10,5,15),
                  res.Food("Banana","A slightly bruised but ripe banana.",["banana"],22,7,35),
                  res.Food("Root","It appears to be some sort of edible root.",["root"],10,4,7),
                  res.Weapon("Club","A thick, gnarled club, hewn from ancient oak.",["club"],5,"clubs",23,75),
                  res.Money(res.CURRENCY+"50",50)]
chestContains2 = [res.Food("Sandwich","Two pieces of bread and a few slices of cheese.",["sandwich"],40,9,40),
                  res.Food("Ham","A haunch of cooked pork.",["pork","meat","haunch","ham"],35,10,40),
                  res.Weapon("Bronze Sword","A dull, heavy sword made of bronze.",["bronze sword"],7,"swords",25,100),
                  res.Shield("Wooden Shield", "A basic shield made of thin wood planks.", ["wood shield","wooden shield"],6,10,25,80),
                  res.Weapon("Stone Axe","A primative axe made from a sharpened stone.",["stone axe"],8,"axes",23,80),
                  res.Money(res.CURRENCY+"100",100)]
chestContains3 = [res.Weapon("Gold Sword","A shiny, ornate sword crafted from pure gold.",["gold sword"],10,"swords",35,150),
                  res.Weapon("Katana","A lithe, elegant sword crafted from crude steel.",["katana"],12,"swords",32,200),
                  res.Shield("Metal Shield", "A strong, metal shield, embossed with bronze symbols.", ["metal shield"],9,15,30,95),
                  res.Shield("Diamond Shield", "A glittering shield crafted from purest crystal.", ["diamond shield"],12,20,35,130),
                  res.Money(res.CURRENCY+"150",150)]

chestNum = 1
for i in range(5):
    chance = random.randint(1,10)
    if chance <= 5:
        c = random.choice(chestContains1)
        chestContains1.remove(c)
    elif chance <= 8:
        c = random.choice(chestContains2)
        chestContains2.remove(c)
    else:
        c = random.choice(chestContains3)
        chestContains3.remove(c)

    if chestNum == 1:
        chests.append(res.Chest(c, True, codes[0]))
    elif chestNum == 2:
        chests.append(res.Chest(c, True, codes[1]))
    elif chestNum == 3:
        chests.append(res.Chest(c, True, False, res.Key("Bronze Key", 5, 20)))
    elif chestNum == 4:
        chests.append(res.Chest(c, True, False, res.Key("Silver Key", 5, 30)))
    else:
        chests.append(res.Chest(c, True, False, res.Key("Gold Key", 5, 50)))
    chestNum += 1


### Path Generator
for i in range(3):
    paths.append(res.Path([NPCs.pop()]))
for i in range(2):
    paths.append(res.Path([],codes.pop()))


### Clearing Generator
for i in range(20):
    clearings.append(res.Clearing("You are in a large, open area of grass, surrounded by trees.", []))
while len(chests) > 0 or len(monsters) > 0:
    for x in clearings:
        seed = random.randint(1,3)
        if seed == 2 and len(monsters) > 0 and "Monster" not in [x.__class__.__name__ for x in x.contains]:
            add = random.choice(monsters)
            x.contains.append(add)
            monsters.remove(add)
        elif seed == 3 and len(chests) > 0 and "Chest" not in [x.__class__.__name__ for x in x.contains]:
            add = random.choice(chests)
            x.contains.append(add)
            chests.remove(add)


### Map Generator
def generateMap():
    if len(map) == 0:
        while len(clearings) > 0 or len(paths) > 0:
            seed = random.randint(1,5)
            if seed in [1,2,3] and len(clearings) > 0:
                chosen = random.choice(clearings)
                map.append(chosen)
                clearings.remove(chosen)
            elif seed == 4 and len(paths) > 0:
                chosen = random.choice(paths)
                map.append(chosen)
                paths.remove(chosen)

    return map
