from z3 import *

# Base constraints
articles = ['G','H','J','Q','R','S','Y']
finance = {'G','H','J'}
nutrition = {'Q','R','S'}
# Position variables 1..7
pos = {a: Int(f'pos_{a}') for a in articles}
base = Solver()
# domain
for a in articles:
    base.add(pos[a] >= 1, pos[a] <= 7)
base.add(Distinct([pos[a] for a in articles]))
# consecutive topic constraint: no two consecutive same topic
for i in range(1,7):
    for a in articles:
        for b in articles:
            if a==b: continue
            same = (a in finance and b in finance) or (a in nutrition and b in nutrition)
            if same:
                base.add(Not(And(pos[a]==i, pos[b]==i+1)))
# S earlier than Q only if Q is third
base.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
# S earlier than Y
base.add(pos['S'] < pos['Y'])
# J earlier than G, G earlier than R
base.add(pos['J'] < pos['G'])
base.add(pos['G'] < pos['R'])

# Option constraints
option_constraints = {
    'A': pos['H'] == 4,
    'B': pos['H'] == 6,
    'C': pos['R'] == 4,
    'D': pos['R'] == 7,
    'E': pos['Y'] == 5,
}

found_options = []
for letter, constr in option_constraints.items():
    solver = Solver()
    solver.append(base.assertions())
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # get a model
        m = solver.model()
        # add blocking clause to see if another distinct solution exists
        solver.push()
        solver.add(Or([pos[a] != m[pos[a]] for a in articles]))
        if solver.check() == unsat:
            # unique solution
            found_options.append(letter)
        solver.pop()
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