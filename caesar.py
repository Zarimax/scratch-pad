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