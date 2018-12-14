#
# Script to generate valid puzzles for Tweedledee and Tweedledum
#

# Set up the 'goal' set - pairs of ordered pairs
bro = ['Tweedledee', 'Tweedledum']
card = ['black', 'red']
dums = []
dees = []

for c in card:
    dums = dums + [('Tweedledum', c)]
    dees = dees + [('Tweedledee', c)]

goals = []

for dum in dums:
    for dee in dees:
        goals = goals + [(dum, dee)]
        goals = goals + [(dee, dum)]

# Set up the truth functions

bro0Truths = []
bro1Truths = []
for g in goals:
    if g[0][1] == 'red':
        bro0Truths.append(g)
    if g[1][1] == 'red':
        bro1Truths.append(g)

# list/set utils

def complement(listOfGoals):
    return [g for g in goals if g not in listOfGoals]

def intersect(a, b):
    return [item for item in a if item in b]
    
def union(a, b):
    return list(a) + [item for item in b if item not in a] 

bro0Lies = complement(bro0Truths)
bro1Lies = complement(bro1Truths)

# functions that help extract sets from goal set

def broForName(number, name):
    blist = []
    for g in goals:
        if g[number][0] == name:
            blist.append(g)
    return blist

def broForCard(number, card):
    blist = []
    for g in goals:
        if g[number][1] == card:
            blist.append(g)
    return blist


# define statement types
def selfStatement(number, name, card):
    return {'text': "My name is " + name + ", and I have a " + card + " card.", 'list': intersect(broForName(number, name),broForCard(number,card))}

def selfOrStatement(number, name, card):
    return {'text': "Either my name is " + name + ", or I have a " + card + " card.", 'list': union(broForName(number, name),broForCard(number,card))}

def otherStatement(number, name, card):
    return {'text': "My brother's name is " + name + ", and he has a " + card + " card.", 'list': intersect(broForName(number, name),broForCard(number,card))}

def otherOrStatement(number, name, card):
    return {'text': "Either my brother's name is " + name + ", or he has a " + card + " card.", 'list': union(broForName(number, name),broForCard(number,card))}

def selfNameStatement(number, name):
    return {'text': "My name is " + name + ".", 'list': broForName(number, name)}

def otherNameStatement(number, name):
    return {'text': "My brother's name is " + name + ".", 'list': broForName(number, name)}

def selfCardStatement(number, card):
    return {'text': "I have a " + card + " card.", 'list': broForCard(number, card)}

def otherCardStatement(number, card):
    return {'text': "My brother has a " + card + " card.", 'list': broForCard(number, card)}

#create lists of statements for each brother

bro0Statements = []
for b in bro:
    for c in card:
        bro0Statements.append(selfStatement(0,b,c))
        bro0Statements.append(otherStatement(1,b,c))
        bro0Statements.append(selfOrStatement(0,b,c))
        bro0Statements.append(otherOrStatement(1,b,c))
for b in bro:
    bro0Statements.append(selfNameStatement(0,b))
    bro0Statements.append(otherNameStatement(1,b))
for c in card:
    bro0Statements.append(selfCardStatement(0,c))
    bro0Statements.append(otherCardStatement(1,c))

bro1Statements = []
for b in bro:
    for c in card:
        bro1Statements.append(selfStatement(1,b,c))
        bro1Statements.append(otherStatement(0,b,c))
        bro1Statements.append(selfOrStatement(1,b,c))
        bro1Statements.append(otherOrStatement(0,b,c))
for b in bro:
    bro1Statements.append(selfNameStatement(1,b))
    bro1Statements.append(otherNameStatement(0,b))
for c in card:
    bro1Statements.append(selfCardStatement(1,c))
    bro1Statements.append(otherCardStatement(0,c))

# function to solve a puzzle given statements
def goalFromStatements(b0_statement, b1_statement):
    puzzle = {}
    b0s = b0_statement['list']
    b1s = b1_statement['list']
    b0t = intersect(b0s, bro0Truths)
    b0l = intersect(complement(b0s), bro0Lies)
    b0 = union(b0t, b0l)
    b1t = intersect(b1s, bro1Truths) 
    b1l = intersect(complement(b1s), bro1Lies)
    b1 = union(b1t, b1l)
    hiddenGoal = intersect(b0,b1)
    if (len(hiddenGoal) == 1):
        explain = ""
        explain += "If the first brother is telling the truth, " + textFromGoal(0,b0t)
        explain += "<br> If the first brother is lying, " + textFromGoal(0,b0l)
        explain += "<br> If the second brother is telling the truth, " + textFromGoal(1,b1t)
        explain += "<br> If the second brother is lying, " + textFromGoal(1,b1l)
        explain += "<br> So, overall, we can determine that " + textFromGoal(0, hiddenGoal)
        puzzle['bro0_text'] = b0_statement['text']
        puzzle['bro1_text'] = b1_statement['text']
        puzzle['solution'] = hiddenGoal[0]
        puzzle['explanation'] = explain
        return puzzle
    else:
        return None

def optionsFromGoals(i, goals):
    #firstPass = [g[i][j] for g in goals]
    #secondPass = []
    #for g in firstPass:
    #    if g not in secondPass:
    #        secondPass.append(g)
    #return secondPass
    return [g[i] for g in goals]

def otherName(name):
    if name == "Tweedledee":
        return "Tweedledum"
    else:
        return "Tweedledee"

def textFromGoal(index, goalList):
    if (len(goalList) == 0):
        return "there cannot be any solutions."
    bro = ""
    other = ""
    if (index == 0):
        bro = "first"
        other = "second"
    else :
        bro = "second"
        other = "first"
    firstBro = optionsFromGoals(index, goalList)
    secondBro = optionsFromGoals((index +1)%2, goalList)
    
    txt = "the " + bro + " brother could be "
    firstBro = reduceList(firstBro)
    txt += combinedList(firstBro)
    #if len(broNames) == 2:
    #    txt += "be either " + prettyList(broNames, "or")
    #else:
    #    txt += "only be " + broNames[0]
    #    txt += " and the " + other + " brother must be " + otherName(broNames[0])
    
    #txt += "; the " + bro + " brother's card must be " + prettyList(broCards, "or")
    #txt += "; and the " + other + " brother's card must be " + prettyList(otherCards, "or")    
    #txt += "."
    txt += "; and the other brother could be "
    secondBro = reduceList(secondBro)
    txt += combinedList(secondBro)
    txt += "."
    return txt        

def reduceList(broList):
    copy = []
    for b in broList:
        if (notInList(copy, b)):
            copy.append(b) 
    return copy 
            
def notInList(broList, b):
    for a in broList:
        if (a[0] == b[0]) & (a[1] == b[1]):
            return False
    return True

def combinedList(broList):
    combined = []
    for b in broList:
        combined.append(b[0] + " holding a " + b[1] + " card")
    return prettyList(combined, "or")

def prettyList(list, conj):
    isFirst = True;
    result = ""        
    count = 1
    size = len(list)
    for s in list:
        if not isFirst and size > 2:
            result += ", "
        isFirst  = False
        if count == size and size > 1:
            if (size == 2):
                result += " "
            result += conj + " "
        count = count +1
        result += s
    return result

# puzzle json
def jsonForPuzzle(puzzle):
    json = '{"bro0": "' + puzzle['bro0_text'] + '", ' 
    json += ' "bro1": "' + puzzle['bro1_text'] + '", '  
    json += ' "bro0_name": "' + puzzle['solution'][0][0] + '", '  
    json += ' "bro1_name": "' + puzzle['solution'][1][0] + '", '  
    json += ' "bro0_card": "' + puzzle['solution'][0][1] + '", '  
    json += ' "bro1_card": "' + puzzle['solution'][1][1] + '", '     
    json += ' "solution": "' + str(puzzle['solution']) + '", '
    json += ' "explanation": "' + puzzle['explanation'] + '", '  
    json += ' "id": "' + str(puzzle['id']) + '"}' + '\n'
    return json

#generate all statement combinations and solve
count = 0;
validPuzzles = []
for s in bro0Statements:
    for t in bro1Statements:
        p = goalFromStatements(s,t)
        if (p != None):
            count = count + 1          
            p['id'] = count
            validPuzzles.append(jsonForPuzzle(p))

# write out the puzzles
result = "["
first = True
for p in validPuzzles:
    if not first:
        result += ", \n"
    else:
        first = False
    result += p
result += "]"
print("There were " + str(count) + " puzzles generated")

f = open("../data/deeDum.json","w")
f.write( result )
f.close()
