import math

def change(amount: int) -> int:
    """
    The country of Examplania has coins that are worth 1, 5, 10, 25, 100, and 500 currency units. At the Zeroth Bank of 
    Examplania, you are trained to make various amounts of money by using as many ¤500 coins as possible, then as many ¤100 
    coins as possible, and so on down.

    For instance, if you want to give someone ¤468, you would give them four ¤100 coins, two ¤25 coins, one ¤10 coin, 
    one ¤5 coin, and three ¤1 coins, for a total of 11 coins.

    Write a function to return the number of coins you use to make a given amount of change.

    change(0) => 0
    change(12) => 3
    change(468) => 11
    change(123456) => 254
    """

    total_coins = 0

    coin_list = [500, 100, 25, 10, 5, 1]
    for coin_value in coin_list:
        num_coins = math.floor(amount / coin_value)
        total_coins += num_coins
        amount -= (num_coins * coin_value)

    return total_coins

#amount = int(input("Enter your value: "))
assert change(0) == 0
assert change(12) == 3
assert change(468) == 11
assert change(123456) == 254

def caesar(input: str, shift: int) -> str:
    """
    Given a string of lowercase letters and a number, return a string with each letter Caesar shifted by the given amount.

    caesar("a", 1) => "b"
    caesar("abcz", 1) => "bcda"
    caesar("irk", 13) => "vex"
    caesar("fusion", 6) => "layout"
    caesar("dailyprogrammer", 6) => "jgorevxumxgsskx"
    caesar("jgorevxumxgsskx", 20) => "dailyprogrammer"
    """
    def do_shift(c, shift):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        iloc = alphabet.find(c)
        return alphabet[(iloc + shift) % len(alphabet)]
     
    shifted_input = [do_shift(c, shift) for c in input]
    return ''.join(shifted_input)

assert caesar("a", 1) == "b"
assert caesar("abcz", 1) == "bcda"
assert caesar("irk", 13) == "vex"
assert caesar("fusion", 6) == "layout"
assert caesar("dailyprogrammer", 6) == "jgorevxumxgsskx"
assert caesar("jgorevxumxgsskx", 20) == "dailyprogrammer"