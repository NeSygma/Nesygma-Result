from z3 import *

# Articles and their topics
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y

# Create position variables for each article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
positions = {article: Int(f'pos_{article}') for article in articles}

# Create topic variables for each position (1-7)
topics = [Int(f'topic_{i}') for i in range(1, 8)]  # 1=finance, 2=nutrition, 3=wildlife

solver = Solver()

# Constraint 1: Each article has a unique position between 1 and 7
for article in articles:
    solver.add(positions[article] >= 1)
    solver.add(positions[article] <= 7)

# All positions are distinct
solver.add(Distinct(list(positions.values())))

# Constraint 2: Map topics to positions based on articles
# For each position, determine the topic based on which article is there
for i in range(1, 8):
    # If position i has article G, H, or J → topic = 1 (finance)
    # If position i has article Q, R, or S → topic = 2 (nutrition)
    # If position i has article Y → topic = 3 (wildlife)
    solver.add(Or(
        [And(positions['G'] == i, topics[i-1] == 1),
         And(positions['H'] == i, topics[i-1] == 1),
         And(positions['J'] == i, topics[i-1] == 1),
         And(positions['Q'] == i, topics[i-1] == 2),
         And(positions['R'] == i, topics[i-1] == 2),
         And(positions['S'] == i, topics[i-1] == 2),
         And(positions['Y'] == i, topics[i-1] == 3)]))

# Constraint 3: Consecutive articles cannot cover the same topic
for i in range(1, 7):
    solver.add(topics[i-1] != topics[i])

# Constraint 4: S can be earlier than Q only if Q is third
# This means: If S < Q, then Q must be at position 3
solver.add(Implies(positions['S'] < positions['Q'], positions['Q'] == 3))

# Constraint 5: S must be earlier than Y
solver.add(positions['S'] < positions['Y'])

# Constraint 6: J must be earlier than G, and G must be earlier than R
solver.add(positions['J'] < positions['G'])
solver.add(positions['G'] < positions['R'])

# Additional condition: J is third
solver.add(positions['J'] == 3)

# Now evaluate each answer choice
found_options = []

# Option A: G is fourth
opt_a = (positions['G'] == 4)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: H is sixth
opt_b = (positions['H'] == 6)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Q is first
opt_c = (positions['Q'] == 1)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: S is second
opt_d = (positions['S'] == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Y is fifth
opt_e = (positions['Y'] == 5)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")