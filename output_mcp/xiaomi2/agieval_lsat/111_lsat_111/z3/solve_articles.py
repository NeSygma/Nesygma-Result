from z3 import *

solver = Solver()

# Position variables for each article (1-7)
pos = {}
for art in ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']:
    pos[art] = Int(f'pos_{art}')

# All positions are 1-7 and distinct
for art in pos:
    solver.add(pos[art] >= 1, pos[art] <= 7)
solver.add(Distinct([pos[art] for art in pos]))

# G is fourth (given condition)
solver.add(pos['G'] == 4)

# Constraint 1: Consecutive articles cannot cover the same topic
# Finance: G, H, J | Nutrition: Q, R, S | Wildlife: Y
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']

for p in range(1, 7):  # positions p and p+1
    # Not both finance at consecutive positions
    both_finance = And(
        Or([pos[a] == p for a in finance]),
        Or([pos[a] == p + 1 for a in finance])
    )
    solver.add(Not(both_finance))
    
    # Not both nutrition at consecutive positions
    both_nutrition = And(
        Or([pos[a] == p for a in nutrition]),
        Or([pos[a] == p + 1 for a in nutrition])
    )
    solver.add(Not(both_nutrition))

# Constraint 2: S can be earlier than Q only if Q is third
# If S < Q, then Q == 3. Equivalently: S >= Q OR Q == 3
solver.add(Or(pos['S'] >= pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J < G < R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Define answer choice constraints
opt_a = (pos['H'] == 5)  # H is fifth
opt_b = (pos['J'] == 1)  # J is first
opt_c = (pos['Q'] == 2)  # Q is second
opt_d = (pos['S'] == 5)  # S is fifth
opt_e = (pos['Y'] == 6)  # Y is sixth

found_options = []
option_models = {}
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        option_models[letter] = solver.model()
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
    m = option_models[found_options[0]]
    for art in ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']:
        print(f"  pos_{art} = {m[pos[art]]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")