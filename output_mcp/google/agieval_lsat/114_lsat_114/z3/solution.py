from z3 import *

solver = Solver()

# Articles: G, H, J (Finance: 0), Q, R, S (Nutrition: 1), Y (Wildlife: 2)
# Positions: 1 to 7
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
pos = {a: Int(f'pos_{a}') for a in articles}

# Domain constraints
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

# Topic mapping
def get_topic(a):
    if a in ['G', 'H', 'J']: return 0
    if a in ['Q', 'R', 'S']: return 1
    return 2

# Topic at position p
def topic_at(p):
    return If(Or([And(pos[a] == p, get_topic(a) == 0) for a in articles]), 0,
           If(Or([And(pos[a] == p, get_topic(a) == 1) for a in articles]), 1, 2))

# Condition 1: Consecutive articles cannot cover the same topic
for p in range(1, 7):
    solver.add(topic_at(p) != topic_at(p + 1))

# Condition 2: S < Q only if Q is 3rd
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Condition 3: S < Y
solver.add(pos['S'] < pos['Y'])

# Condition 4: J < G < R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Options: (A)1, (B)3, (C)4, (D)5, (E)6
options = [("A", 1), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]

# We want to find the position that is NOT possible (UNSAT)
# The question asks "S could be in any of the following positions EXCEPT:"
# So we look for the one that is UNSAT.

impossible_options = []
for letter, p in options:
    solver.push()
    solver.add(pos['S'] == p)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")