# read the input string
INPUT = open('lab3.txt').read()
# split the string into an array of strings
input_array = INPUT.split('\n')

#function that returns a dictionary with splitted productions ({'S': ['abAB], 'C':['AS'] ...})
def productions(arr):
    map = {}
    for i in input_array:
        # split the rule
        x = i.split('->')
        # add the nonterminal to the map 
        if not x[0] in map:
            # create an empty array for each nonterminal symbol
            map[x[0]] = []
        # apend to the array the corresponding terminals
        map[x[0]].append(x[1])
    return map

def check_empty(map):
    for k, v in rules.items():
        for j in v:
            if j == '$':
                return True, k
    return False, -1

def get_absence_power_set(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in get_absence_power_set(seq[1:]):
            yield [seq[0]] + item
            yield item

# function that substituates epsilon 
def change(str, substr, mask):
    result = []
    for m in mask:
        modified = str
        pos = 1
        for i in m:
            for _ in range(i):
                pos = modified.find(substr, pos - i)
            modified = modified[:pos] + modified[pos + 1:]
        result.append(modified)
    return result

# function that eliminates epsilon-productions
def eliminate_empty_productions(map):
    prod = map.copy()
    #check for epsilon productions
    check_eps, eps_key = check_empty(rules)
    if check_eps:
        prod[eps_key].remove('$')
        if len(prod[eps_key]) == 0:
            del prod[eps_key]

    for key in prod:
        for i, el in enumerate(prod[key]):
            if eps_key in el:
                if eps_key in prod:
                    # count the number of the nonterminal symbol that derives in eps, on the rightt side of each production, if exists
                    count = el.count(eps_key)
                    # the array of distinct appereances of the nonterminal symbol on the rightt side
                    arr = []
                    for i in range(1, count + 1):
                        arr.append(i)
                    # create power subsets of absent nonterminals
                    sub_sets=[]
                    for i in get_absence_power_set(arr):
                        sub_sets.append(i)
                    # substitute the nonterminal that derives in eps, in order to get new productions
                    to_add = change(el, eps_key, sub_sets)[:-1]
                    # add the new productions
                    prod[key] = prod[key] + to_add
                else:
                    if(len(prod[key][i])) == 1:
                        prod[key].remove(eps_key)
                    else:
                        prod[key][i] = el.replace(eps_key, '')
    check_eps, eps_key = check_empty(prod)
    return prod
         
# function that checks for unit productions 
def check_unit(key, map):
    for el in map[key]:
        if len(el) == 1 and el in map:
                #if X->Y, return True and Y
                return True, el
    return False, -1

# function that removes the unit productions and adds the new ones
def remove(key, initial_value, map):
    is_unit, unit = check_unit(initial_value, map)

    if is_unit:
        map = remove(initial_value, unit, map)
    
    # eliminate the unit profuction
    map[key].remove(initial_value)
    # add the new productions after substituting
    map[key] = map[key] + map[initial_value]
    return map

# function that eliminates all unit productions
def eliminate_unit_productions(map):
    prod = map.copy()
    # traverse the keys S, A, B, C
    for key in prod:
        # check for unit productions
        is_unit, unit = check_unit(key, prod)
        # remove them if exists
        if is_unit:
            prod = remove(key, unit, prod)
    return prod

# function that eliminates inaccessible symbols
def eliminate_inaccessible_symbols(map):
    prod = map.copy()
    accessed_keys = set()

    for key, value in prod.items():
        for i in value:
            for symbol in i:
                # find the accessed nonterminals
                if symbol in prod:
                    accessed_keys.add(symbol) 

    # find and delete the inaccessible symbols 
    for key in list(prod):
        if key not in accessed_keys:
            del prod[key]
    return prod

# function that eliminates all nonproductive symbols
def eliminate_nonroductive_symbols(map):
    prod = map.copy()
    productive_symbols = set()
    # find the nonterminals that derive in a terminal
    for key in prod:
        for el in prod[key]:
            if(len(el)==1) and (el not in prod):
                productive_symbols.add(key)

    i = 1
    while i:
        for key in prod:
            if key in productive_symbols:
                continue
            for el in prod[key]:
                # checking each letter in part from left side of production
                for letter in el:
                    if letter in productive_symbols:
                        # if the letter (nonterminal symbol) is in the set, we add the key of this production, as it has a path from one to another nonterminal
                        productive_symbols.add(key)
                        i += 1
        i -= 1

    for key in list(prod):
        # delete the key and values of a nonproductive
        if key not in productive_symbols:
            del prod[key]

            for innerkey in list(prod):
                for el in prod[innerkey]:
                    if key in el:
                        prod[innerkey].remove(el)
    return prod

def new_symbol(pos, map):
    letters = string.ascii_uppercase
    while letters[pos] in map:
        pos -= 1
    return letters[pos], pos

import string 
def has_terminal(str):
    for letter in str:
        if letter in string.ascii_lowercase:
           return True
    return False

# function that normalizes the grammar 
def chomsky(map):
    prod = map.copy()
    temp = {}
    terminals = string.ascii_lowercase
    letters_counter = len(string.ascii_uppercase) - 1

    u = 1
    while u:
        for key in list(prod):
            for i, el in enumerate(prod[key]):
                # letter=el[1:]
                if len(el) > 2 :
                    if el in temp:
                        # if the el exists in the dictionary temp, which contains the new symbols and their productions, ex: {'abAB':'ZB'}
                        # then it simply assigns
                        prod[key][i] = temp[el]
                    else:
                        # otherwise it creates a new nonterminal symbol 
                        new_letter, letters_counter = new_symbol(letters_counter, prod)
                        # assigns it in temp{}
                        temp[el] = el[0] + new_letter
                        # reduces the length by one of the right side of production rule                     
                        prod[new_letter] = [el[1:]]
                        prod[key][i] = temp[el]
                        u += 1
        u -= 1
    # temp ={}
    for key in list(prod):
        for i, el in enumerate(prod[key]):
            if (len(el) == 2) and has_terminal:
                if el in temp:
                    # if the el exists in the dictionary temp, which contains the new symbols and their productions, ex: {'abAB':'ZB'}
                    # then it simply assigns 
                    prod[key][i] = temp[el]
                else:
                    for letter in el:
                        if letter in terminals:
                            if letter in temp:
                                prod[key][i] = prod[key][i].replace(letter, temp[letter])
                            else:
                                # otherwise creates a new nonterminal symbol
                                new_letter, letters_counter = new_symbol(letters_counter, prod)
                                # assigns it in temp{}
                                temp[letter] = new_letter
                                prod[temp[letter]] = [letter]
                                # replaces the terminals in productions of legth = 2 with new nonterminal
                                prod[key][i] = prod[key][i].replace(letter, temp[letter])
                    temp[el] = prod[key][i]
    # delete duplicates by converting the list to set and then back to list
    for key, value in prod.items():
        prod[key] = list(set(value))
    return prod

rules = productions(input_array)
rules = eliminate_empty_productions(rules)
rules = eliminate_unit_productions(rules)
rules = eliminate_inaccessible_symbols(rules)
rules = eliminate_nonroductive_symbols(rules)
rules = chomsky(rules)

print('The Chomsky Normal Form of the grammar:')
for key in rules:
    print(key, '->', rules[key])

