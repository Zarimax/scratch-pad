"""
i = 10
while i > 0:
    print(i)
    i -= 1
"""
for i in range(10, 0, -1):
    print(i)
    
#this is the code I texted you about:  
file = open("/usercode/files/books.txt", "r")

names = list(file.readlines())

"""this for loop didn't work when the if and else conditions were in the reverse order
of course when they were in the reverse order the if conditon read 'if line = names[len(names)-1]:'
so it captured the last element of the list, instead of everything other than the last element. 
Also, I have since learnt there that you index the last element of a list using list[-1] rather than
the ugly method using the length of the list that appears below... but I'm sure there is a lot else
that's wrong with this! Like my attempt to use the docstring notation for example... """

for line in names:
    if line != names[len(names)-1]:
        print(line[0]+str(len(line)-1))
    else:
        print(line[0]+str(len(line)))

file.close()
