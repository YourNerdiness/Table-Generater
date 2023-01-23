import random
import copy

NUM_PREFERENCES = 3
TABLE_SIZES = []
FIXED_POINTS = []

def keyExists(dictToSearch, key):

    try:

        temp = dictToSearch[key]

    except KeyError as e:

        return False

    return True

keyFound = list()

def getKeyFromVal(dictToSearch, value):

    for name in dictToSearch:

        if name in keyFound:

            continue

        if dictToSearch[name] == value:

            keyFound.append(name)

            return name
    
    raise KeyError("Could not find key from value.")

def sortDict(dictToSort):

    global keyFound
    keyFound = list()

    sortedValues = list(dictToSort.values())

    sortedValues.sort(reverse=True)

    toReturn = dict()

    for value in sortedValues:

        toReturn[getKeyFromVal(dictToSort, value)] = value

    return toReturn

def getPreferences():

    toReturn = dict()

    i = 0
    while True:

        name = str(input("Enter name: ")).lower().replace(" ", "")
        preferences = list()

        if name == "done":

            break

        elif name == "count":

            continue

        else:

            i += 1

        for j in range(NUM_PREFERENCES):

            preferences.append((str(input("Enter preference #{}: "
                                .format(j + 1))).lower().replace(" ", "")))

        toReturn[name] = preferences

    return toReturn

preferenceDict = getPreferences()

placed = list()

arrangement = list()

for i in range(len(TABLE_SIZES)):

    arrangement.append([])

for i in range(len(arrangement)):

    if FIXED_POINTS[i][0] != None:

        for j in range(min(len(FIXED_POINTS[i]), TABLE_SIZES[i])):

            arrangement[i].append(FIXED_POINTS[i][j])

            placed.append(FIXED_POINTS[i][j])

i = 0
for table in arrangement:

    if len(table) == 0:

        randName = None

        mutual = False
        j = 0
        while len(table) < TABLE_SIZES[i]:

            randName = random.choice(list(preferenceDict.keys()))

            while randName in placed:

                randName = random.choice(list(preferenceDict.keys()))

            for preference in preferenceDict[randName]:

                if preference in placed:

                    continue

                if preferenceDict[preference].count(randName) >= 1:

                    if len(table) < TABLE_SIZES[i]:

                        mutual = True

                        table.append(preference)
                        placed.append(preference)

            j += 1

            if j > 2*len(preferenceDict.keys()):

                break

        table.append(randName)
        placed.append(randName)

        if not mutual:

            randName = random.choice(list(preferenceDict.keys()))

            while randName in placed:

                randName = random.choice(list(preferenceDict.keys()))

            table.append(randName)
            placed.append(randName)

    elif len(table) == 1:

        name = table[0]

        mutual = False
        j = 0
        while not mutual and len(table) < TABLE_SIZES[i]:

            for preference in preferenceDict[name]:

                if preference in placed:

                    continue

                if preferenceDict[preference].count(name) >= 1:

                    if len(table) < TABLE_SIZES[i]:

                        mutual = True

                        table.append(preference)

            j += 1

            if j > 2*len(preferenceDict.keys()):

                break

        if not mutual:

            randName = random.choice(list(preferenceDict.keys()))

            while randName in placed:

                randName = random.choice(list(preferenceDict.keys()))

            table.append(randName)
            placed.append(randName)

    potententialNames = copy.deepcopy(table)

    while len(table) < TABLE_SIZES[i]:

        frequencyDict = dict()

        for name in potententialNames:

            preferenceScore = NUM_PREFERENCES

            for preference in preferenceDict[name]:

                if preference in placed:

                    continue

                if not keyExists(frequencyDict, preference):

                    frequencyDict[preference] = preferenceScore

                else:

                    frequencyDict[preference] += preferenceScore

                preferenceScore -= 1

        sFrequencyDict = sortDict(frequencyDict)

        popularNames = list(sFrequencyDict.keys())

        found = False
        n = 0
        while n < len(popularNames):

            if popularNames[n] in placed:

                n += 1

                continue

            table.append(popularNames[n])
            placed.append(popularNames[n])
            potententialNames.append(popularNames[n])

            found = True

            break

        if not found:

            potNameLen = len(potententialNames)

            for l in range(potNameLen):

                for preference in preferenceDict[potententialNames[l]]:
                
                    potententialNames.append(preference)

    i += 1

for table in arrangement:

    print(table)
 