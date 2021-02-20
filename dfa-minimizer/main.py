# Authors:
# RichieSjt https://github.com/RichieSjt
# EduardoHerreraJ https://github.com/EduardoHerreraJ

import re
import collections.abc
import itertools
import networkx as nx
import matplotlib.pyplot as plt

def generate_graph(dfa, transitions):
    #method to generate the graph of the DFA
    G = nx.MultiDiGraph()
    All_labels = dict()

    for i in range(len(states)):
        #Add each state as a node to the graph
        G.add_node(states[i])
        for transition in transitions:
            if transition[0] == states[i]:
                #Add each transition as an edge of the graph
                G.add_edge(states[i],transition[2]) 
                #Generate the label of each edge
                All_labels[(states[i],transition[2])]=transition[1]

    #Give a circular position to our graph
    pos = nx.circular_layout(G)
    plt.figure()
    #Draw each node 
    nx.draw(G,pos, with_labels=1,node_size=1000,connectionstyle='arc3, rad = 0.1',labels={node:node for node in G.nodes()})
    #Draw each edge
    nx.draw_networkx_edge_labels(G,pos,edge_labels=All_labels,font_color='red')
    #Show the graph
    plt.show()

def update(d, u):
    #Update a dictionary without overwriting previous keys
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def generate_dfa(states, transitions):
    #Generate a dfa in the format "{state:{alphabet:transition, alphabet:transition}}""
    transition_temp = dict()
    dfa = dict()

    #Obtaining the transitions for each state
    for i in range(len(states)):
        current_state = states[i]
        for transition in transitions:
            #Checking all transitions and only extracting the ones that belong to the current state
            if transition[0] == current_state:
                transition_temp.update({transition[1]: transition[2]})
        #Creating a temporal dictionary to add it to the main dfa dictionary
        row = {current_state: transition_temp}
        update(dfa, row)
        row.clear()
        transition_temp.clear()
    
    return dfa

def search_repeated_transitions(dfa, initial_states, final_states):
    repeated = list()

    #Comparing every state with each other only once
    for i, j in itertools.combinations(dfa, 2):
        if dfa[i] == dfa[j]:
            if (i not in final_states and j not in final_states) or (i in final_states and j in final_states):
                #Making sure to not add duplicate states
                if i not in repeated: repeated.append(i)
                if j not in repeated: repeated.append(j)
    return repeated

def update_states(dfa, states):
    #updating the states when the automata changes due to minimization
    states.clear()
    for key in dfa:
        states.append(key)
    return

def replace_keys(repeated_equal):
    letter = letters.pop(0)

    #Deleting the repeated state keys from the dfa and adding the new ones
    for r in repeated_equal:
        contents_temp = dfa[r]
        del dfa[r]
        row = {"q" + letter: contents_temp}
        update(dfa, row)
    
    #Updating the states list now that the repeated states have been substituted
    update_states(dfa, states)

    #Overwritting the content from the alphabet keys to match the now substitutes of the repeated keys
    for s in states:
        for l in alphabet:
            #Catching a KeyError in case a transition was not specified by the user
            try:
                if dfa[s][l] in repeated_equal:
                    dfa[s][l] = 'q' + letter
            except KeyError:
                pass
    return

def minimize_dfa(dfa, alphabet, states, initial_states, final_states):

    #Obtaining the states that have the same transitions    
    repeated = search_repeated_transitions(dfa, initial_states, final_states)

    #Repeating the process of minimization until there are no states with the same transitions
    while repeated:
        repeated_equal = list()
        
        while repeated:
            contents = dfa[repeated[0]]
            #Obtaining the states that have the same contents
            repeated_equal = [k for k,v in dfa.items() if v == contents and k in repeated]
            repeated = [e for e in repeated if e not in repeated_equal]
            #Replacing those states with the minimized states
            replace_keys(repeated_equal)
            repeated_equal.clear()

        repeated = search_repeated_transitions(dfa, initial_states, final_states)

    return dfa

def accepts(dfa, initial, final_states, s):
    #Testing if the String is accepted

    state = initial
    for c in s:
        #Catching a KeyError in case a transition was not specified by the user
        try:
            state = dfa[state][c]
        except KeyError:
            pass
    return state in final_states


#Select the text file we want to read
file = open("test4.txt", "r")

transitions = list()

for idx, line in enumerate(file):
    #- The first line indicates the set of states of the automata separated by commas
    if idx == 0: states = line.rstrip('\n').split(",")
    #The second line indicates the alphabet symbols separated by commas
    elif idx == 1: alphabet = line.rstrip('\n').split(",")
    #The third line indicates the initial state
    elif idx == 2: initial_states = line.rstrip('\n').split(",")
    #The fourth line indicates the set of final states separated by commas
    elif idx == 3: final_states = line.rstrip('\n').split(",")
    #The following lines indicate the evaluation of the extended transition function with the elements of the alphabet in the following format:
    else: transitions.append(re.split(',|=>', line.rstrip('\n')))

#Create a list of letters for the minimization
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']

dfa = generate_dfa(states, transitions)

print("\nInitial dfa\n",dfa)

#Read the String we want to test
word = input ("\nEnter String: ") 
print("\nThe automata accepts the string:", accepts(dfa, initial_states[0], final_states, word))

dfa_graph = generate_graph(dfa, transitions)

minimized_dfa = minimize_dfa(dfa, alphabet, states, initial_states, final_states)

print("\nMinimized dfa\n", minimized_dfa)