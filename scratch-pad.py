def book_codes1():    
    #this is the code I texted you about:  
    file = open("books.txt", "r")

    names = list(file.readlines())

    # Rick: readlines() has a behavior where it will read the newline characters on each line. So the actual list
    # that you get back looks like this:
    """
        ['Consider Phlebas\n', 'The Player of Games\n', 'Use of Weapons\n', 
        'The State of the Art\n', 'Excession\n', 'Inversions\n', 'Look to Windward\n', 
        'Matter\n', 'Surface Detail\n', 'The Hydrogen Sonata']
    """
    # the newline characters, (\n), count as characters when running len()

    """this for loop didn't work when the if and else conditions were in the reverse order
    of course when they were in the reverse order the if conditon read 'if line = names[len(names)-1]:'
    so it captured the last element of the list, instead of everything other than the last element. 
    Also, I have since learnt there that you index the last element of a list using list[-1] rather than
    the ugly method using the length of the list that appears below... but I'm sure there is a lot else
    that's wrong with this! Like my attempt to use the docstring notation for example... """

    # Rick: you are trying to filter out the newline characters here, but there is a much easier way
    # to do that. See book_codes2() below
    for line in names:
        if line != names[len(names)-1]:
            print(line[0]+str(len(line)-1))
        else:
            print(line[0]+str(len(line)))

    file.close()

def book_codes2():
    # Rick: first, using this "with open(..) as file" construction is a best practice because it limits the
    # scope of the file handler. the scope of variables is a big topic, but in this case it means that the
    # file will be automatically closed when the statement ends, (so you don't need an extra file.close() call)
    with open("books.txt",'r') as file:
        # Rick: here we do the following:
        #  1) read the whole file as a single string
        #  2) split that string into a list of strings which are delimited by the newline character. During the split,
        #     the newline character is dropped. This leaves us with a plain list of book names.
        #  3) print the first character of each book name + the length of the book name
        book_list = file.read().split('\n')
        for book in book_list:
            print(book[0] + str(len(book)))

book_codes2()
