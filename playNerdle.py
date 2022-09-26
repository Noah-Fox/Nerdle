#text-based version of the game
#User inputs 8-char equation, program outputs score of each char
#   2 - correct char in the position
#   1 - correct char in wrong position
#   0 - incorrect char

import nerdle as nd

solution = nd.makeEquation()

print("Welcome to Nerdle!\nGuess the equation to win!")
print("Enter 'X' to give up")


guess = ""
gaveUp = False

while guess != solution:
    print("Enter a guess:")
    guess = input()
    if (guess == "X"):
        print("\nThe solution is:\n  ",solution)
        guess = solution
        gaveUp = True
    else:
        checked = nd.checkGuess(solution,guess)
        if (checked[0] == "3"):
            print("Invalid equation\n")
        else:
            print(nd.checkGuess(solution,guess),"\n")
    
if not gaveUp:
    print("CORRECT")