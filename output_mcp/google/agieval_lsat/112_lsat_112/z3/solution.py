from z3 import *

# Articles
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
# Topics
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y

pos = {a: Int(f'pos_{a}') for a in articles}
solver = Solver()

# Positions are 1-7 and distinct
solver.add(Distinct([pos[a] for a in articles]))
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)

# Topic mapping
def get_topic(p):
    # Returns a Z3 expression for the topic at position p
    # 0: Finance, 1: Nutrition, 2: Wildlife
    return If(Or(p == pos['G'], p == pos['H'], p == pos['J']), 0,
           If(Or(p == pos['Q'], p == pos['R'], p == pos['S']), 1, 2))

# Condition 1: Consecutive articles cannot cover the same topic
for p in range(1, 7):
    solver.add(get_topic(p) != get_topic(p + 1))

# Condition 2: S can be earlier than Q only if Q is third
# S < Q => Q == 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Condition 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Condition 4: J < G < R
solver.add(pos['J'] < pos['G'], pos['G'] < pos['R'])

# Test options
options = [
    ("A", pos['G'] == 2),
    ("B", pos['H'] == 2),
    ("C", pos['S'] == 2),
    ("D", pos['R'] == 3),
    ("E", pos['Y'] == 3)
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