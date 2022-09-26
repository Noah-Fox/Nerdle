import random
import numpy as np

digits = ['0','1','2','3','4','5','6','7','8','9']
operators = ['+','*','-','/','=']
mathOps = ['+','*','-','/']
allChars = ['0','1','2','3','4','5','6','7','8','9','+','*','-','/','=']




#returns an 8-char string equation, which is valid, but not necessarily true
def makeSolution():
    #creates ~13.5% true (or modifiably true) equations
    testEq = ""
    lastChar = ''
    canUseChars = []

    equalPos = random.randrange(4,7)
    opAmount = 1
    if equalPos > 4 and random.choice([True,False]):
        opAmount = 2
    
    opOnePos = -1
    opTwoPos = -1
    if (opAmount == 1):
        if (equalPos == 4):
            opOnePos = random.choice([1,2])
        elif (equalPos == 5):
            opOnePos = random.choice([2,3])
        else:
            opOnePos = 3
    elif (equalPos == 5):
        opOnePos = 1
        opTwoPos = 3
    else:
        opOnePos = random.choice([0,1,2])
        if (opOnePos < 2):
            opOnePos = 1
            opTwoPos = random.choice([3,4])
        else:
            opTwoPos = 4

    for x in range(8):
        canUseChars = []
        if x == opOnePos or x == opTwoPos:
            canUseChars = mathOps 
        elif x == equalPos:
            canUseChars = ["="]
        else:
            #all nonzero digits
            canUseChars = [str(i) for i in range(1,10)]
            #zero is possible if not in first position or following operator
            if x != 0 and lastChar not in operators:
                canUseChars.append("0")
        
        lastChar = random.choice(canUseChars)
        
        testEq += lastChar
    return testEq

#utilizes the makeSolution() and isTrueEquation() functions to return an 8-char true equation
def makeEquation():
    while True:
        testEq = makeSolution()
        tested = isTrueEquation(testEq)
        if tested[0]:
            return tested[1]    
    

#check if an equation is valid, regardless of its truth status
def isValidEquation(equation: str):
    #causes of invalidity:
    # -operators after equal sign           
    # -two operators in a row               
    # -operator in first or last position   
    # -leading zero in num                  
    # -length doesn't equal 8               

    #length doesn't equal 8
    if len(equation) != 8:
        return False
    
    #operator in first or last position
    if equation[0] in operators or equation[7] in operators:
        return False 
    
    #leading zero in first number
    if equation[0] == '0':
        return False 
    
    
    afterEquals = False 
    for i in range(7):
        #two operators in a row
        if equation[i] in operators and equation[i+1] in operators:
            return False 
        if equation[i] == '=':
            afterEquals = True 
        #operator after equals sign
        if afterEquals and equation[i+1] in operators:
            return False 
        #leading zero in number
        if equation[i] in operators and equation[i+1] == '0':
            return False 
    return afterEquals  


#check if an equation is true, or if its answer can be changed to make it true
#returns a tuple containing bool for if it's true, and equation, which can be updated to make it true
def isTrueEquation(testEq):
    if not isValidEquation(testEq):
        return False,testEq
    
    leftParts = [testEq[0]]
    ans = ""
    afterEqual = False 
    for i in testEq[1:]:
        if i == "=":
            afterEqual = True 
        elif not afterEqual:
            if i in operators:
                leftParts.append(i)
            elif leftParts[-1][0] in operators:
                leftParts.append(i)
            else:
                leftParts[-1] += i 
        else:
            ans += i
    
    while len(leftParts) > 1:
        doneOp = False 
        for i in range(len(leftParts)):
            if not doneOp and leftParts[i] in mathOps and (leftParts[i] == "*" or leftParts[i] == "/"):
                leftParts[i] = doOp(leftParts[i-1],leftParts[i],leftParts[i+1])
                doneOp = True 
                del leftParts[i+1]
                del leftParts[i-1]
        if not doneOp:
            for i in range(len(leftParts)):
                if not doneOp and leftParts[i] in mathOps:
                    leftParts[i] = doOp(leftParts[i-1],leftParts[i],leftParts[i+1])
                    doneOp = True 
                    del leftParts[i+1]
                    del leftParts[i-1]
    
    if np.floor(float(leftParts[0])) != float(leftParts[0]) or int(leftParts[0]) < 0:
        return False,testEq 
    
    if digitAmount(int(leftParts[0])) != digitAmount(int(ans)):
        return False,testEq

    ansDigAmount = digitAmount(int(ans))
    changedEq = testEq[0:8-ansDigAmount]
    changedEq += str(int(leftParts[0]))
    return True,changedEq 
    
#perform a mathematical equation, given a character of an operator, and char or any numerical type for nums
def doOp(num1,op,num2):
    if type(num1) == str:
        num1 = int(num1)
    if type(num2) == str:
        num2 = int(num2)
    
    if op == "+":
        return num1 + num2 
    if op == "*":
        return num1 * num2 
    if op == "-":
        return num1 - num2 
    if op == "/":
        return num1 / num2
    return -1

#return amount of digits in num
def digitAmount(num):
    digs = 0
    while num > 0:
        num = np.floor(num/10)
        digs += 1
    return digs

#prints info about efficiency of the makeSolution() function
def testEfficiency(testAmount):
    printAll = False
    trueEqs = []
    validEqs = []
    for i in range(testAmount):
        madeEq = makeSolution()
        tested = isTrueEquation(madeEq)
        if tested[0]:
            trueEqs.append(tested[1])
        else:
            validEqs.append(madeEq)

    if printAll:
        print("Valid Equations:")
        for i in validEqs:
            print(i)
        print("True Equations:")
        for i in trueEqs:
            print(i)

    print()
    print(len(trueEqs),"true equations")
    print(len(validEqs),"valid and untrue equations")
    print(np.round(100*len(trueEqs)/testAmount,2),"% true equations",sep='')

def isValidGuess(guess):
    tested = isTrueEquation(guess)
    return tested[0] and tested[1] == guess 

#inputs solution and player's guess
#outputs 8-char string, containing:
#  0 - char is not in solution
#  1 - char is in solution in another place
#  2 - char is in correct place
#  3 - all 3's if invalid guess
def checkGuess(solution,guess):
    if not isValidGuess(guess):
        return "33333333"
    
    charInSol = {}
    for i in allChars:
        charInSol[i] = 0

    checked = ""
    for i in range(8):
        if guess[i] == solution[i]:
            checked += "2"
        else:
            checked += "0"
            charInSol[solution[i]] += 1
    finalChecked = ""
    for i in range(8):
        if checked[i] == "2":
            finalChecked += "2"
        elif charInSol[guess[i]] > 0:
            finalChecked += "1"
            charInSol[guess[i]] -= 1
        else:
            finalChecked += "0"

    return finalChecked


def solveNerdle(solution,dispProg=False):
    if dispProg:
        print(solution," <<< solution")
        print("   Step-by-step display of solution")
        print("   Press ENTER to continue to next step, 'a' to display all possible chars for each position")
    #2D list, all chars possible in each position
    posChars = []
    for i in range(8):
        posChars.append([str(x) for x in range(1,10)])
    for i in range(1,8):
        posChars[i].append("0")
    for i in range(1,7):
        posChars[i] += mathOps
    for i in range(4,8):
        posChars[i].append("=")
    
    #dictionary for each char, denoting how many times it can appear in the equation
    charAmounts = {}
    for i in digits:
        charAmounts[i] = 6
    for i in mathOps:
        charAmounts[i] = 2
    charAmounts["="] = 1

    attempts = 0
    
    while True:
        attempts += 1

        #make a guess
        guessAmount = 0
        guess = ""
        guessing = True 
        guessesMade = []
        while (guessing):
            #keep track of the amount of guesses made
            guessAmount += 1
            if guessAmount > 10000:
                if dispProg:
                    print("Too many guesses")
                    print("\t",guessesMade[0:50])
                return "FAILURE",-1

            guess = makeGuess(posChars)
            guessesMade.append(guess)

            
            
            #test if the guess is a true equation
            tested = isTrueEquation(guess)
            if (tested[0]):
                guess = tested[1]
                guessing = False 

        #check the score of the guess
        score = checkGuess(solution,guess)


        zeroScores = set()
        oneScores = set()
        twoScores = set()

        #go through each char guessed
        for i in range(8):
            #if its a twoScore, that's the only char that pos can be
            if score[i] == "2":
                posChars[i] = [guess[i]]
                twoScores.add(guess[i])
            else:
                #if it's not twoScore, that pos can't be that char
                if guess[i] in posChars[i]:
                    posChars[i].remove(guess[i])
                if score[i] == "1":
                    oneScores.add(guess[i])
                else:
                    zeroScores.add(guess[i])
        #go through every char that got a zeroScore
        while len(zeroScores) > 0:
            zScore = zeroScores.pop()
            #if there wasn't another of the same char that got a oneScore, then it doesn't
            #  exist anywhere that doesn't have the char as its only possible guess
            if zScore not in oneScores:
                for i in range(8):
                    if posChars[i] != [zScore] and zScore in posChars[i]:
                        posChars[i].remove(zScore)
        
        #if = got a twoScore, remove it from every other position, and remove operators after
        if "=" in twoScores:
            for i in range(8):
                if "=" in posChars[i] and len(posChars[i]) > 1:
                    posChars[i].remove("=")
            equalPos = guess.index("=")
            for i in range(equalPos+1,8):
                toRemove = []
                for x in posChars[i]:
                    if x in mathOps:
                        toRemove.append(x)
                for x in toRemove:
                    posChars[i].remove(x)
        
        #if any position can only be an op, then remove ops from adjacent positions
        for i in range(8):
            mustBeOp = True
            for x in posChars[i]:
                if x not in operators:
                    mustBeOp = False 
            if mustBeOp:
                for x in operators:
                    if x in posChars[i-1]:
                        posChars[i-1].remove(x)
                for x in operators:
                    if x in posChars[i+1]:
                        posChars[i+1].remove(x)

        #when dispProg is true, the program outputs progress and waits for user to continue it
        if dispProg:
            print("  ",guess)
            print("  ",score)
            #if 'a' is entered by user, print list of possible characters in each position
            if input() == "a":
                for i in allChars:
                    print(i+": ",end='')
                    for x in range(8):
                        if i in posChars[x]:
                            print(i,sep='',end='')
                            hasPrinted = True 
                        else:
                            print(" ",sep='',end='')
                    print()
                print()
        
        if guess == solution:
            return guess, attempts 

#returns a random possible solution, given possible characters for each position
def makeGuess(posChars):
    testEq = ""
    lastChar = ''
    canUseChars = []

    #find possible positions = can be in
    equalLeft = []
    for i in range(8):
        if "=" in posChars[i]:
            equalLeft.append(i)
    equalPos = random.choice(equalLeft)

    #find possible op positions
    opLeft = set()
    for i in range(1,equalPos-1):
        for x in mathOps:
            if x in posChars[i]:
                opLeft.add(i)
    opLeft = list(opLeft)
    
    opOnePos = -1
    opTwoPos = -1
    opAmount = 1
    #assign random position to first op
    opOnePos = random.choice(opLeft)
    opLeft.remove(opOnePos)

    if random.choice([True,False]):
        #set opTwoPos to any possible pos left
        while len(opLeft) > 0:
            possPos = random.choice(opLeft)
            opLeft.remove(possPos)
            if abs(possPos-opOnePos) > 1 and equalPos-possPos > 1:
                opTwoPos = possPos 
        if opTwoPos != -1:
            opAmount = 2
            #if ops are out of order, switch them
            if opTwoPos < opOnePos:
                tmp = opOnePos
                opOnePos = opTwoPos 
                opTwoPos = tmp 
    


    for x in range(8):
        canUseChars = []
        if x == opOnePos or x == opTwoPos:
            for i in mathOps:
                if i in posChars[x]:
                    canUseChars.append(i)
        elif x == equalPos:
            canUseChars = ["="]
        else:
            #all nonzero digits
            for b in [str(i) for i in range(1,10)]:
                if b in posChars[x]:
                    canUseChars.append(b)
            #zero is possible if not following operator
            if "0" in posChars[x] and x != opOnePos+1 and x != opTwoPos+1 and x != equalPos+1:
                canUseChars.append("0")
        
        try:
            lastChar = random.choice(canUseChars)
        except:
            return "00000000"
        
        testEq += lastChar
    return testEq