

import random

player = input("Please enter R, P or S (for [R]ock, [P]aper and [S]cissors) ")
player = player.upper()
computer = random.choice('RPS')
if (
    (player == "R" and computer == "S") or
    (player == "P" and computer == "R") or
    (player == "S" and computer == "P")
):
    print ("player wins")
elif player == computer:
    print("draw")
else: 
    print("computer wins")

print("computer chose:", computer)
