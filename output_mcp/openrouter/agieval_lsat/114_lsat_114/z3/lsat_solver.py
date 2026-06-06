from z3 import *

solver = Solver()
# Variables for positions 1..7
articles = ['G','H','J','Q','R','S','Y']
pos = {a: Int(a) for a in articles}
# Domain constraints
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
# All distinct
solver.add(Distinct([pos[a] for a in articles]))
# Topic mapping
finance = ['G','H','J']
nutrition = ['Q','R','S']
wildlife = ['Y']
# Consecutive same topic not allowed
for i in range(1,7):
    # For each pair of articles, if they occupy consecutive positions, their topics must differ
    # We'll enforce: for any two articles a,b, if |pos[a]-pos[b]| == 1 then topics differ
    # Use pairwise constraints
    for a in articles:
        for b in articles:
            if a < b:  # avoid duplicate
                # Define topic type: 0 finance,1 nutrition,2 wildlife
                def topic(x):
                    return If(Or([x == IntVal(v) for v in finance]), 0,
                          If(Or([x == IntVal(v) for v in nutrition]), 1, 2))
                # Not needed, we can directly encode using Or of combinations
                pass
# Instead, encode directly using implications for each pair of same-topic articles
# Finance pairs cannot be consecutive
for a in finance:
    for b in finance:
        if a < b:
            solver.add(Or(pos[a] - pos[b] != 1, pos[a] - pos[b] != -1))
# Nutrition pairs cannot be consecutive
for a in nutrition:
    for b in nutrition:
        if a < b:
            solver.add(Or(pos[a] - pos[b] != 1, pos[a] - pos[b] != -1))
# Wildlife only one article, no need
# Additional constraints
# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
# S earlier than Y
solver.add(pos['S'] < pos['Y'])
# J earlier than G, G earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Options mapping
options = [
    ("A", 1),  # first
    ("B", 3),  # third
    ("C", 4),  # fourth
    ("D", 5),  # fifth
    ("E", 6)   # sixth
]
found_options = []
for letter, p in options:
    solver.push()
    solver.add(pos['S'] == p)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")