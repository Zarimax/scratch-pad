from random import randint

num_dice = input("Number of dice to roll: ")
sides_dice = input("Number of sides: ")

for i in range(int(num_dice)):
    print(randint(1, int(sides_dice)))