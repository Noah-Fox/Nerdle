#runs the solveNerdle() function 1000 times, then outputs the outcomes of the trials
#enter 'z' to skip trials, or press ENTER to go through one step at a time

import numpy as np
import nerdle as nd


showProg = True
amounts = []
while len(amounts) < 1000:
    sol = nd.makeEquation()
    solved = nd.solveNerdle(sol,showProg)
    if solved[0] == "FAILURE":
        print(solved[0],sol)
    else:
        amounts.append(solved[1])
    
    if showProg:
        print("Enter 'z' to skip, any other key to continue",end=' ')
    if showProg and input() == "z":
        showProg = False

print("Average amount of attempts:",np.average(amounts))
print("Max amount of attempts:",np.max(amounts))
print("Min amount of attempts:",np.min(amounts))

counted = 0
print("Distribution of amounts of attempts:")
for i in range(1,9):
    counted += amounts.count(i)
    print(" ",i," - ",amounts.count(i))
print("  9+ - ",len(amounts)-counted)

