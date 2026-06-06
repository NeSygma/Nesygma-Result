from z3 import *

# Articles
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
# Topics
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y
topic_map = {'G': 'F', 'H': 'F', 'J': 'F', 'Q': 'N', 'R': 'N', 'S': 'N', 'Y': 'W'}

solver = Solver()

# pos[article] = position (1-7)
pos = {a: Int(f'pos_{a}') for a in articles}
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

# topic_at[p] = topic of article at position p
# We use an array or a function to map position to topic
# Since we have 7 positions, we can use a function
def get_topic(p):
    return If(Or([And(pos[a] == p, topic_map[a] == 'F') for a in articles]), 'F',
           If(Or([And(pos[a] == p, topic_map[a] == 'N') for a in articles]), 'N', 'W'))

# Condition 1: Consecutive articles cannot cover the same topic
for p in range(1, 7):
    solver.add(get_topic(p) != get_topic(p + 1))

# Condition 2: S can be earlier than Q only if Q is third.
# (pos[S] < pos[Q]) => (pos[Q] == 3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Condition 3: S must be earlier than Y.
solver.add(pos['S'] < pos['Y'])

# Condition 4: J must be earlier than G, and G must be earlier than R.
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Question constraint: J is third
solver.add(pos['J'] == 3)

# Test options
options = [
    ("A", pos['G'] == 4),
    ("B", pos['H'] == 6),
    ("C", pos['Q'] == 1),
    ("D", pos['S'] == 2),
    ("E", pos['Y'] == 5)
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