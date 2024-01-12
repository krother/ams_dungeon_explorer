"""
In the Guess the Number game, the player tries to guess a number 

that the computer has generated.

    1. The program randomly “rolls” a number between 1 and 100.
    2. Do not output the number.
    3. The player enters a number
    4. The program says whether the number was too big or too small.
    5. Repeat steps 3-5 until the correct number was guessed.
"""
from ast import While
import random
number = random.randint(a = 1, b = 1_000_000)
while True:
    player_number = int(input("please enter number: "))
    if(player_number == number):
        print("Player wins!")
        break
    elif(player_number > number):
        print("Too Big!")
    else:
        print("Too Small!")
   




