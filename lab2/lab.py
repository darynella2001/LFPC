import pandas as pd

"""
Varianta 32

Q={q0, q1, q2}
VT={a, b, c}
F={q2}
 (q0, a ) = q0,
 (q0, a ) = q1,
 (q1, c ) = q0,
 (q1, b ) = q1,
 (q1, a ) = q2,
 (q2, a ) = q2 
"""


transitions = [
    '0-a-0',
    '0-a-1',
    '1-c-0',
    '1-b-1',
    '1-a-2',
    '2-a-2'
]


def getNFA(transitions):
    nfa = {}
    for tr in transitions:
        x = tr.split('-')

        if not x[0] in nfa:
            nfa[x[0]] = {}

        if not x[1] in nfa[x[0]]:
            nfa[x[0]][x[1]] = ''

        nfa[x[0]][x[1]] += x[2]
    return nfa


def NFAtoDFA(nfa):
    states = []
    values = []

#copy the states
    for state in nfa:
        states.append(state)

#searching for new states

    for state in nfa:
        for value in nfa[state]:
            #if the length of a state is bigger than 1, we add the new state
            if len(nfa[state][value]) > 1:
                if not nfa[state][value] in states:
                    states.append(nfa[state][value])
            else:
                if not nfa[state][value][0] in states:
                    states.append(nfa[state][value][0])

    for state in nfa:
        for value in nfa[state]:
            if not value in values:
                values.append(value)

    for state in states:
        if not state in nfa:
            #spliting the states into an array
            #example q0q1 = ['0','1']
            newState = list(state)
            for value in values:
                val = []

#add the transitions of the new state
                for st in newState:
                    if value in nfa[st]:
                        val.append(nfa[st][value])
#we add the new state in the global dict keyed by states
                if not state in nfa:
                    nfa[state] = {}
#add the elements of the list to the inner dict which is keyed by alphabet elements
#the values in the inner dict are joined as all the transitions from the formed state are considered
                nfa[state][value] = ''.join(set(''.join(val)))
                states.append(''.join(set(''.join(val))))
    return nfa

print("NFA:")
nfa = getNFA(transitions)

import copy
dict1 = copy.deepcopy(nfa)

#writing the table in a beautiful form :D
for keys in dict1:
  if keys.isdigit():
    dict1['q'+ keys] = dict1[keys]
    del dict1[keys]

for val in dict1.values():
  for x, y in val.items():
    if len(y) == 2:
      new_x = 'q' + y[0] + 'q' + y[1]
      val[x] = new_x

    if len(y)==1:
      new_x='q' + y
      val[x] = new_x

NFA = pd.DataFrame(dict1)
NFA = NFA.fillna("-")
print(NFA.transpose())

print("\nNFA to DFA:")
dfa = NFAtoDFA(nfa)
# print(dfa)
dict2 = copy.deepcopy(dfa)

#writing the table in a beautiful form :D
for keys in dict2:
  if keys.isdigit():
    if len(keys) == 3:
      dict2['q'+ keys[0] + 'q' + keys[1] + 'q' + keys[2]] = dict2[keys]
      del dict2[keys]
    if len(keys) == 2:
      dict2['q'+ keys[0] + 'q' + keys[1]] = dict2[keys]
      del dict2[keys]
    if len(keys) == 1:
      dict2['q'+ keys] = dict2[keys]
      del dict2[keys]

for val in dict2.values():
  for x, y in val.items():
    if len(y) == 3:
      new_x = 'q' + y[0] + 'q' + y[1] + 'q' + y[2]
      val[x] = new_x

    if len(y) == 2:
      new_x = 'q' + y[0] + 'q' + y[1]
      val[x] = new_x

    if len(y)==1:
      new_x='q' + y
      val[x] = new_x
    
DFA = pd.DataFrame(dict2)
DFA = DFA.fillna("-")
print(DFA.transpose())