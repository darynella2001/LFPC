import re
import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 
import pylab

str = '''P={
1. S-aS
2. S-cD
3. D-bR
4. R-aR
5. R-b
6. R-cS }'''

start=str.find('P={') + len('P={')
end = str.find(" }")
new_string = str[start:end]
 
# print(new_string)
s = re.split('[0-9]. ', new_string)
# print(s)
s.remove('\n')
# print(s)

nodes = []
rest = []
for i in s:
    nodes.append(i[0])
    rest.append(i[2:])

# print(nodes)
# print(rest)
right =[]
right = [i.replace('\n','') for i in rest]

map = {}   
for n in nodes:
    map[n] = {}

for i in range(len(nodes)):
    non = list(right[i])[0]
    terminal = ''
    if len(list(right[i])) == 2:
        terminal = list(right[i])[1]
    map[nodes[i]][non] = terminal
print(map)

def accepts(transitions,initial,accepting,s):
    state = initial
    for c in s:
        state = transitions[state][c]
    return state in accepting

#checking the word
try: 
    if accepts(map,'S',{''}, 'acbab'):
        print('Accepted')
except KeyError:        
    print('Rejected')


#drawing
G = nx.DiGraph()

G.add_edges_from([('S', 'D'), ('R','S')], label='c')
G.add_edges_from([('D', 'R')],  label='b')
G.add_edges_from([('R', 'R*')],  label='a,b loop')
G.add_edges_from([('S', 'S*')],  label='a loop')

edge_colors=['black' for edge in G.edges()]
for index, tuple in enumerate(G.edges()):
  # element_one = tuple[0]
  element_two = tuple[1]
  if len(element_two) == 2:
    edge_colors[index] = 'yellow'

val_map = {'D':0.5, 
           'R':0.0,  #final state
           'S*':0.5,
           'R*':0.0, #final state
           'S':1.0}  #initial state

values = [val_map.get(node, 1.5) for node in G.nodes()]
edge_labels = dict([((u,v,), d['label']) for u, v, d in G.edges(data=True)])

pos = nx.spring_layout(G)
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
node_labels = {node:node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels)
nx.draw(G, pos, node_color = values, node_size = 500, edge_color=edge_colors)
labels=['transition', 'self-loop']
plt.legend(labels)
plt.show()