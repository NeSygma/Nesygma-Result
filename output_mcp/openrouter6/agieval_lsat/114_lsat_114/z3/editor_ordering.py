from z3 import *

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
topics = {a: 0 if a in ['G', 'H', 'J'] else 1 if a in ['Q', 'R', 'S'] else 2 for a in articles}

# Position variables for each article
pos = {a: Int(f'pos_{a}') for a in articles}

solver = Solver()

# Basic constraints: positions between 1 and 7
for a in articles:
    solver.add(1 <= pos[a], pos[a] <= 7)

# All positions distinct
solver.add(Distinct([pos[a] for a in articles]))

# Ordering constraints
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])
solver.add(pos['S'] < pos['Y'])

# S < Q only if Q is third
solver.add(Or(pos['S'] >= pos['Q'], pos['Q'] == 3))

# Exactly one article per position
for p in range(1, 8):
    solver.add(Sum([If(pos[a] == p, 1, 0) for a in articles]) == 1)

# Adjacency constraint: consecutive positions must have different topics
def topic_at(p):
    # Build an If chain to get the topic at position p
    expr = None
    for a in articles:
        t = topics[a]
        if expr is None:
            expr = If(pos[a] == p, t, 0)
        else:
            expr = If(pos[a] == p, t, expr)
    return expr

for p in range(1, 7):
    solver.add(topic_at(p) != topic_at(p+1))

# Now check each option for S's position
options = [('A', 1), ('B', 3), ('C', 4), ('D', 5), ('E', 6)]
impossible = []

for letter, s_pos in options:
    solver.push()
    solver.add(pos['S'] == s_pos)
    result = solver.check()
    if result == unsat:
        impossible.append(letter)
    solver.pop()

# Determine answer
if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found impossible: {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")