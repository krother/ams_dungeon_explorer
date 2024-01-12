
import random

player = input("Please enter R, P or S (for [R]ock, [P]aper and [S]cissors) ")
computer = random.choice('RPS')
if player == "R" and computer == "S":
    print("player wins")
elif player == "P" and computer == "R":
    print("player wins")
elif player == "S" and computer == "P":
    print ("player wins")
elif player == computer:
    print("draw")
else: 
    print("computer wins")
