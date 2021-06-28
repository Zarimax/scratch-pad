"""
Given N, the number of phone prototypes you have, and H, the maximum height that needs to be tested, determine the 
maximum number of trials required by an optimal strategy to determine K.

phonedrop(1, 100) => 100
phonedrop(2, 100) => 14
phonedrop(3, 100) => 9
phonedrop(1, 1) => 1
phonedrop(2, 456) => 30
phonedrop(3, 456) => 14
phonedrop(4, 456) => 11
phonedrop(2, 789) => 40
phonedrop(3, 789) => 17
phonedrop(4, 789) => 12

You should be able to at least handle values of H up to 999.

similar problem here: https://datagenetics.com/blog/july22012/index.html
"""
answer_table = {}

def phonedrop(phones:int, height:int) -> int:
    if phones == 1 or height == 1:
        return height
    
    answer = answer_table.get((phones, height), 0)
    if answer > 0:
        return answer

    for floor in range(1, height):
        yes_break = 1 + phonedrop(phones-1, floor)
        no_break = 1 + phonedrop(phones, height-floor)
        answer = max(answer, min(yes_break, no_break))
    
    answer_table[(phones, height)] = answer
    return answer

for k in range(1, 1001):
    print(f"k={k}, drops={phonedrop(3, k)}")