"""
The country of Examplania has coins that are worth 1, 5, 10, 25, 100, and 500 currency units. At the Zeroth Bank of 
Examplania, you are trained to make various amounts of money by using as many 500 coins as possible, then as many 100 
coins as possible, and so on down.

For instance, if you want to give someone 468, you would give them four 100 coins, two 25 coins, one 10 coin, 
one 5 coin, and three 1 coins, for a total of 11 coins.

Write a function to return the number of coins you use to make a given amount of change.

change(0) => 0
change(12) => 3
change(468) => 11
change(123456) => 254
"""

def change_bad(amount: int) -> int:
    # set the default number of coins to zero. this covers the case when amount = 0.
    total_coins = 0
    
    # define a list of coin values. the order of this list is important, since it is evaluated from
    # first to last. as such, the coins should be in decending order.
    coin_list = [500, 100, 25, 10, 5, 1]
    
    # for each coin value in the coin list, we will count the number of those coins that "fit" into the given amount.
    for coin_value in coin_list:
        # to figure out how many coins "fit" into the amount, we keep deducting that coin value from the amount until we
        # can't deduct any more. this is known as "division implemented by repeated subtraction"
        while amount >= coin_value:
            amount -= coin_value
            # each time that we deduct a coin value from the amount, we increment the total coin count
            total_coins += 1

    return total_coins


def change_ok(amount: int) -> int:
    import math
    total_coins = 0

    coin_list = [500, 100, 25, 10, 5, 1]
    for coin_value in coin_list:
        # to figure out how many coins "fit" into the amount, we divide the amount by the coin value and 
        # round down with the floor function
        num_coins = math.floor(amount / coin_value)
        total_coins += num_coins
        # the amount is then reduced by the number of coins multiplied by their coin value
        amount -= (num_coins * coin_value)

    return total_coins

def change_best(amount: int) -> int:
    total_coins = 0

    coin_list = [500, 100, 25, 10, 5, 1]
    for coin_value in coin_list:
        # this does the same thing as change_ok(), but it uses the native Python math operators to accomplish this. specifically, it
        # uses // as floor division and % as modulus 
        total_coins += (amount // coin_value)
        amount %= coin_value

    return total_coins

assert change_best(0) == 0
assert change_best(12) == 3
assert change_best(468) == 11
assert change_best(123456) == 254

print(change_best(1231122313112))
print("Tests Completed Successfully!")