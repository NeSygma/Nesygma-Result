from z3 import *

# Create solver
solver = Solver()

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']
all_articles = finance + nutrition + wildlife  # ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Position variables (1-7)
pos = {article: Int(f'pos_{article}') for article in all_articles}

# Each article gets a unique position from 1 to 7
for article in all_articles:
    solver.add(pos[article] >= 1)
    solver.add(pos[article] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[article] for article in all_articles]))

# Constraint 1: Consecutive articles cannot cover the same topic
# We need to ensure that for any two articles with same topic, their positions are not consecutive
# For each topic, ensure no two articles have consecutive positions
def no_consecutive_same_topic(topic_articles):
    constraints = []
    for i in range(len(topic_articles)):
        for j in range(i+1, len(topic_articles)):
            a1, a2 = topic_articles[i], topic_articles[j]
            # They cannot be consecutive: |pos[a1] - pos[a2]| != 1
            constraints.append(Or(pos[a1] - pos[a2] != 1, pos[a2] - pos[a1] != 1))
    return constraints

solver.add(no_consecutive_same_topic(finance))
solver.add(no_consecutive_same_topic(nutrition))
# Y is alone in wildlife, so no constraint needed

# Constraint 2: S can be earlier than Q only if Q is third
# This means: If pos[S] < pos[Q], then pos[Q] == 3
# In Z3: Implies(pos[S] < pos[Q], pos[Q] == 3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now test each option using the required skeleton
found_options = []

# Option A: G is second
opt_a_constr = (pos['G'] == 2)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: H is second
opt_b_constr = (pos['H'] == 2)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: S is second
opt_c_constr = (pos['S'] == 2)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: R is third
opt_d_constr = (pos['R'] == 3)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Y is third
opt_e_constr = (pos['Y'] == 3)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results according to the required logic
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")