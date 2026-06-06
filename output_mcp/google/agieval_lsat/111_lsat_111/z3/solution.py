from z3 import *

# Articles: G, H, J (Finance), Q, R, S (Nutrition), Y (Wildlife)
# Topics: 0: Finance, 1: Nutrition, 2: Wildlife
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
topic_map = {'G': 0, 'H': 0, 'J': 0, 'Q': 1, 'R': 1, 'S': 1, 'Y': 2}

# Positions 1-7
pos = {a: Int(f'pos_{a}') for a in articles}
solver = Solver()

# Domain constraints
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

# Topic at each position
# topic_at[p] is the topic at position p
topic_at = [Int(f'topic_at_{p}') for p in range(1, 8)]
for p in range(1, 8):
    # topic_at[p-1] is the topic of the article at position p
    solver.add(Or([And(pos[a] == p, topic_at[p-1] == topic_map[a]) for a in articles]))

# Condition 1: Consecutive articles cannot cover the same topic
for p in range(6):
    solver.add(topic_at[p] != topic_at[p+1])

# Condition 2: S < Q only if Q is 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Condition 3: S < Y
solver.add(pos['S'] < pos['Y'])

# Condition 4: J < G < R
solver.add(pos['J'] < pos['G'], pos['G'] < pos['R'])

# Question: G is 4th
solver.add(pos['G'] == 4)

# Test options
options = [
    ('A', pos['H'] == 5),
    ('B', pos['J'] == 1),
    ('C', pos['Q'] == 2),
    ('D', pos['S'] == 5),
    ('E', pos['Y'] == 6)
]

found_options = []
for letter, constr in options:
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