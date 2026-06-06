from z3 import *

# Students
students = ['J', 'K', 'L', 'M', 'O']
# Plays
plays = ['S', 'T', 'U']

# Variables: S[student][play]
S = [[Bool(f'S_{s}_{p}') for p in plays] for s in students]
# Map student to index
s_idx = {s: i for i, s in enumerate(students)}

solver = Solver()

# Each student reviews at least one play
for i in range(5):
    solver.add(Or([S[i][j] for j in range(3)]))

# Condition 1: Kramer and Lopez each review fewer plays than Megregian
def count_plays(i):
    return Sum([If(S[i][j], 1, 0) for j in range(3)])

solver.add(count_plays(s_idx['K']) < count_plays(s_idx['M']))
solver.add(count_plays(s_idx['L']) < count_plays(s_idx['M']))

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Not(And(S[s_idx['J']][p], S[s_idx['L']][p])))
    solver.add(Not(And(S[s_idx['J']][p], S[s_idx['M']][p])))

# Condition 3: Kramer and O'Neill both review Tamerlane
solver.add(S[s_idx['K']][plays.index('T')])
solver.add(S[s_idx['O']][plays.index('T')])

# Condition 4: Exactly two of the students review exactly the same play or plays as each other.
# This means there is exactly one pair (i, j) with i < j such that S[i] == S[j],
# and no other pairs exist.
def same_set(i, j):
    return And([S[i][p] == S[j][p] for p in range(3)])

pairs = []
for i in range(5):
    for j in range(i + 1, 5):
        pairs.append(same_set(i, j))

# Exactly one pair is true
solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)

# Question: Which one of the following could be an accurate and complete list of the students who review Tamerlane?
# Options:
# (A) Jiang, Kramer
# (B) Kramer, O'Neill
# (C) Kramer, Lopez, O'Neill
# (D) Kramer, Megregian, O'Neill
# (E) Lopez, Megregian, O'Neill

def get_t_reviewers():
    return [students[i] for i in range(5) if S[i][plays.index('T')]]

options = {
    "A": ['J', 'K'],
    "B": ['K', 'O'],
    "C": ['K', 'L', 'O'],
    "D": ['K', 'M', 'O'],
    "E": ['L', 'M', 'O']
}

found_options = []
for label, reviewers in options.items():
    solver.push()
    # Constraint: T_reviewers == reviewers
    for i in range(5):
        if students[i] in reviewers:
            solver.add(S[i][plays.index('T')])
        else:
            solver.add(Not(S[i][plays.index('T')]))
    
    if solver.check() == sat:
        found_options.append(label)
    solver.pop()

print(f"Found options: {found_options}")