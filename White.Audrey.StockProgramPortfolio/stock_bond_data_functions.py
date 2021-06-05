
#should return list of data from a text file
def populate_data_from_file(data, file):
    try:
        for x in file:
            data.append(x.rstrip())
        return data
    except TypeError:
        print({f'Cannnot use .append() or rstrip() if {file} is not a file with text'})



#splits a string into a list, this is useful for working with string from a file
def split_file_string(new_list, data):
    try:
        for x in data:
            c = x.split()
            new_list.append(c) 
        return new_list
    except TypeError:
        print({f'Cannnot use .split() on values within {data} if not a string'})

#further separates a list by commas
def split_file_list(new_list, data):
    try:
        for x in data:
            new_list.append(x[0].split(","))
        return new_list
    except TypeError:
        print({f'Cannnot use .append() on values within {data} if not a list'})


#prints exception when file not found
def check_to_write_file(file):
    try:
        new_file = open(file, 'w')
        return new_file
    except TypeError:
        print({f'Sorry, {file} is not a file'})
    except FileNotFoundError:
        print({f'Sorry, the file {file} does not exist'})

#prints exception when file not found
def check_to_read_file(file):
    try:
        new_file = open(file, 'r')
        return new_file
    except TypeError:
        print({f'Sorry, {file} is not a file'})
    except FileNotFoundError:
        print({f'Sorry, the file {file} does not exist'})


