from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
topics = {
    'G': 'finance',
    'H': 'finance',
    'J': 'finance',
    'Q': 'nutrition',
    'R': 'nutrition',
    'S': 'nutrition',
    'Y': 'wildlife'
}

# Create a solver
solver = Solver()

# Position variables for each article (1-7)
positions = {art: Int(f'pos_{art}') for art in articles}

# Each position is unique and in 1..7
solver.add(Distinct(list(positions.values())))
for art in articles:
    solver.add(positions[art] >= 1, positions[art] <= 7)

# Constraint: Consecutive articles cannot cover the same topic
for i in range(1, 7):
    for art1 in articles:
        for art2 in articles:
            if topics[art1] == topics[art2]:
                # If two articles have the same topic, their positions cannot be consecutive
                solver.add(Not(And(positions[art1] == i, positions[art2] == i + 1)))
                solver.add(Not(And(positions[art1] == i + 1, positions[art2] == i)))

# Constraint: S must be earlier than Y
solver.add(positions['S'] < positions['Y'])

# Constraint: J must be earlier than G, and G must be earlier than R
solver.add(positions['J'] < positions['G'])
solver.add(positions['G'] < positions['R'])

# Constraint: S can be earlier than Q only if Q is third
# Equivalent to: If S < Q then Q == 3
# Which is equivalent to: Q != 3 or S >= Q
solver.add(Or(positions['Q'] == 3, positions['S'] >= positions['Q']))

# Given condition for this question: J is third
solver.add(positions['J'] == 3)

# Now test each option
found_options = []

# Option A: G is fourth
solver.push()
solver.add(positions['G'] == 4)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is sixth
solver.push()
solver.add(positions['H'] == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is first
solver.push()
solver.add(positions['Q'] == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S is second
solver.push()
solver.add(positions['S'] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is fifth
solver.push()
solver.add(positions['Y'] == 5)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")