from random import randrange
# https://docs.python.org/3.7/library/random.html

# define a function to generate <num_dice> random numbers from 1 to <dice_sides>, inclusive. this 
# works by calling random.randrange in a for loop inside of a list comprehension
def roll_dice(num_dice, num_sides):
    # get a random number from 1 to num_sides
    # do this num_dice times, (range 0 to num_dice)
    result = [randrange(1, num_sides + 1) for _ in range(num_dice)]
    return result

# roll the dice and save the outcome in <result>
result = roll_dice(num_dice=10, num_sides=20)

# print the sorted dice results
print(sorted(result))

