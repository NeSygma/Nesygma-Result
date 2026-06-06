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
            same_topic = Or(
                And(a in finance, b in finance),
                And(a in nutrition, b in nutrition),
                And(a in wildlife, b in wildlife)
            )
            solver.add(Implies(Abs(pos[a] - pos[b]) == 1, Not(same_topic)))

# S can be earlier than Q only if Q is third
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Test each position for S
options = {
    'A': pos['S'] == 1,  # first
    'B': pos['S'] == 3,  # third
    'C': pos['S'] == 4,  # fourth
    'D': pos['S'] == 5,  # fifth
    'E': pos['S'] == 6,  # sixth
}

possible_positions = []
impossible_positions = []

for letter, constr in options.items():
    s = Solver()
    # Copy all base constraints
    for a in articles:
        s.add(pos[a] >= 1, pos[a] <= 7)
    s.add(Distinct([pos[a] for a in articles]))
    for a in articles:
        for b in articles:
            if a < b:
                same_topic = Or(
                    And(a in finance, b in finance),
                    And(a in nutrition, b in nutrition),
                    And(a in wildlife, b in wildlife)
                )
                s.add(Implies(Abs(pos[a] - pos[b]) == 1, Not(same_topic)))
    s.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
    s.add(pos['S'] < pos['Y'])
    s.add(pos['J'] < pos['G'])
    s.add(pos['G'] < pos['R'])
    
    s.add(constr)
    if s.check() == sat:
        possible_positions.append(letter)
    else:
        impossible_positions.append(letter)

print(f"Possible positions for S: {possible_positions}")
print(f"Impossible positions for S: {impossible_positions}")

if len(impossible_positions) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_positions[0]}")
elif len(impossible_positions) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible positions {impossible_positions}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible positions found")