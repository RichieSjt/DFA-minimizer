# DFA-minimizer
First partial project made during the computational maths course.


## Functionality
**A program that reads from a file the elements that define an DFA and builds the
equivalent minimized DFA. The program specifies if a string is accepted or not by the
DFA.**

The transition table will be defined in a txt file. The file shall be defined as follows:
- The first line indicates the set of states of the automata separated by commas.
- The second line indicates the alphabet symbols separated by commas.
- The third line indicates the initial state.
- The fourth line indicates the set of final states separated by commas.
- The following lines indicate the evaluation of the extended transition function with the
elements of the alphabet in the following format:

state, symbol = > state

Example, the following line

`q0, a = > q1`

indicates that the DFA processes the following: `δ(q0,a) = q1`

It is not necessary that all transitions are specified in this file. An evaluation may not appear if a
state indicating that the result of that evaluation is the empty set

The outcome of this process is a minified version of the inputed DFA.

## Dependencies
The functionality of this project relies on networkx and matplotlib libraries for the minified DFA visualization.

You can install them by using Python's PIP with the following commands:

`pip install networkx`

`pip install matplotlib`

#### Important note
> This program doesn't validate the values in the input file, it assumes that they were built correctly.

## Built with
![Python Badge](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white)
![Networkx Badge](https://img.shields.io/badge/Networkx-FF7E0E?style=flat-square&logoColor=white)
![Matplotlib Badge](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logoColor=white)
