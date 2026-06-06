from z3 import *

# Articles
articles = ['G','H','J','Q','R','S','Y']
# Create position variables
pos = {a: Int(f'pos_{a}') for a in articles}
# Topic mapping: finance=1, nutrition=2, wildlife=3
topic = {
    'G': 1,
    'H': 1,
    'J': 1,
    'Q': 2,
    'R': 2,
    'S': 2,
    'Y': 3,
}

solver = Solver()
# Domain constraints: positions 1..7 distinct
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

# Consecutive articles cannot have same topic
for a in articles:
    for b in articles:
        if a != b:
            # If positions differ by 1, topics must differ
            solver.add(Or(Abs(pos[a] - pos[b]) != 1, topic[a] != topic[b]))

# S earlier than Q only if Q is third: (posS < posQ) -> posQ == 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
# S earlier than Y
solver.add(pos['S'] < pos['Y'])
# J earlier than G
solver.add(pos['J'] < pos['G'])
# G earlier than R
solver.add(pos['G'] < pos['R'])

# Define option constraints
options = {}
options['A'] = ['H','S','J','Q','Y','G','R']
options['B'] = ['J','Q','G','H','S','Y','R']
options['C'] = ['Q','J','S','H','Y','G','R']
options['D'] = ['Q','J','Y','S','G','R','H']
options['E'] = ['S','G','Q','J','Y','R','H']

opt_constraints = {}
for letter, order in options.items():
    cons = []
    for idx, art in enumerate(order, start=1):
        cons.append(pos[art] == idx)
    opt_constraints[letter] = And(cons)

found_options = []
for letter, constr in [(l, opt_constraints[l]) for l in ['A','B','C','D','E']]:
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