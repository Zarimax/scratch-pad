"""
The ABACABA sequence is defined as follows: the first iteration is the first letter of the alphabet (a). To form the 
second iteration, you take the second letter (b) and put the first iteration (just a in this case) before and after it, 
to get aba. For each subsequent iteration, place a copy of the previous iteration on either side of the next letter of 
the alphabet.

Here are the first 5 iterations of the sequence:

a
aba
abacaba
abacabadabacaba
abacabadabacabaeabacabadabacaba

The 26th and final iteration (i.e. the one that adds the z) is 67,108,863 characters long. If you use one byte for 
each character, this takes up just under 64 megabytes of space.
"""
def abacaba(n):
    r = ""
    for i in range(n):
        r = r + chr(97 + i) + r

    return r


assert abacaba(1) == "a"
assert abacaba(2) == "aba"
assert abacaba(3) == "abacaba"
assert abacaba(4) == "abacabadabacaba"
assert abacaba(5) == "abacabadabacabaeabacabadabacaba"

if __name__ == "__main__":
    print(abacaba(5))