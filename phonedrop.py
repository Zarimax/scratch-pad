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

# worst case: 1 phone. starting at each floor, must test each floor in ascending order.
#  so for phone=1, drops=height
# best case: X phones, where X >= log2(height). in this case, a binary search can be
#  performed. so for phone=10, heights up to 1024 can be searched with 10 drops
# this function solves for cases with X phones, where X > 1 and X < log2(height)
# this can be implemented two ways:
#   MIN across all floors of (the MAX of the lower floors, (EXCLUSIVE of current floor), versus upper floors)
#   MAX across all floors of (the MIN of the lower floors, (INCLUSIVE of current floor), versus upper floors)
#  these end up being mathematically equivalent, although it is not intuitive
#  https://math.stackexchange.com/questions/602553/how-to-invert-max-and-min-operators-in-equations
#  

def phonedrop(phones:int, height:int) -> int:
    if phones == 1 or height == 1:
        return height
    
    answer = answer_table.get((phones, height), 0)
    if answer > 0:
        return answer

    for floor in range(1, height):
        yes_break = 1 + phonedrop(phones-1, floor) # delete upper floors and search lower floors
        no_break = 1 + phonedrop(phones, height-floor) # delete lower floors and search upper floors
        answer = max(answer, min(yes_break, no_break))
    
    answer_table[(phones, height)] = answer
    return answer

#start_phones = 3
#start_height = 100
#print(f"drops={phonedrop(phones=start_phones, height=start_height)}\n\n")
#for i in range(1, 101):
#    print(f"i={i} drops={phonedrop(phones=3, height=i)}")

import random

Start = 9
Stop = 99
limit = 10

rlist = [random.randint(Start, Stop) for iter in range(limit)]
print(rlist)

global_min = 999999999
global_max = 0

for i in range(0, len(rlist)):
    # take the MAX of the inclusive MINs
    local_min = min(sum(rlist[:i]), sum(rlist[i:]))
    if local_min > global_max:
        global_max = local_min

    # take the MIN of the exclusive MAXs
    local_max = max(sum(rlist[:i]), sum(rlist[i+1:]))
    if local_max < global_min:
        global_min = local_max

    print(f"bottom: {rlist[:i]} top: {rlist[i:]} min: {local_min}")
    print(f"bottom: {rlist[:i]} top: {rlist[i+1:]} max: {local_max}")

print(f"global_min={global_min} global_max={global_max}")