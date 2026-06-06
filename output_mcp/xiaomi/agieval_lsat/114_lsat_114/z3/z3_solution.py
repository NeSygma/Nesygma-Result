from z3 import *

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# Position variables (1-7)
pos = {a: Int(f'pos_{a}') for a in articles}

solver = Solver()

# Each article has a unique position from 1 to 7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

# Consecutive articles cannot cover the same topic
# For each pair of articles, if they are consecutive (diff = 1), they must be different topics
for a in articles:
    for b in articles:
        if a < b:
            # If positions differ by 1, they can't be same topic
            same_topic = Or(
                And(a in finance, b in finance),
                And(a in nutrition, b in nutrition),
                And(a in wildlife, b in wildlife)
            )
            solver.add(Implies(Abs(pos[a] - pos[b]) == 1, Not(same_topic)))

# S can be earlier than Q only if Q is third
# Equivalently: if S < Q then Q == 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now test each option: S could be in position X
# We need to find which position S CANNOT be in
# Test each position 1,3,4,5,6 (corresponding to A,B,C,D,E)

options = {
    'A': pos['S'] == 1,  # first
    'B': pos['S'] == 3,  # third
    'C': pos['S'] == 4,  # fourth
    'D': pos['S'] == 5,  # fifth
    'E': pos['S'] == 6,  # sixth
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
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