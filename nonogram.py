"""
A binary array is an array consisting of only the values 0 and 1. Given a binary array of any length, 
return an array of positive integers that represent the lengths of the sets of consecutive 1's in the 
input array, in order from left to right.

nonogramrow([]) => []
nonogramrow([0,0,0,0,0]) => []
nonogramrow([1,1,1,1,1]) => [5]
nonogramrow([0,1,1,1,1,1,0,1,1,1,1]) => [5,4]
nonogramrow([1,1,0,1,0,0,1,1,1,0,0]) => [2,1,3]
nonogramrow([0,0,0,0,1,1,0,0,1,0,1,1,1]) => [2,1,3]
nonogramrow([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]) => [1,1,1,1,1,1,1,1]

As a special case, nonogram puzzles usually represent the empty output ([]) as [0]. If you prefer 
to do it this way, that's fine, but 0 should not appear in the output in any other case.
"""

def nonogramrow(input_array):
    output_array = []
    count = 0

    for elem in input_array:
        count += elem
        if elem == 0 and count > 0:
            output_array.append(count)
            count = 0

    if count > 0:
        output_array.append(count)

    return output_array

assert nonogramrow([]) == []
assert nonogramrow([0,0,0,0,0]) == []
assert nonogramrow([1,1,1,1,1]) == [5]
assert nonogramrow([0,1,1,1,1,1,0,1,1,1,1]) == [5,4]
assert nonogramrow([1,1,0,1,0,0,1,1,1,0,0]) == [2,1,3]
assert nonogramrow([0,0,0,0,1,1,0,0,1,0,1,1,1]) == [2,1,3]
assert nonogramrow([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]) == [1,1,1,1,1,1,1,1]
print("Tests Completed Successfully!")