from z3 import *

solver = Solver()

# Declare boolean variables
F, G, H, K, L, M, P, Q, R = Bools('F G H K L M P Q R')

# Base constraints: F, L, Q, R are selected
solver.add(F, L, Q, R)

# Exactly 5 scientists selected
selected_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0),
                      If(K, 1, 0), If(L, 1, 0), If(M, 1, 0),
                      If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(selected_count == 5)

# At least one of each type
solver.add(Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)]) >= 1)  # botanist
solver.add(Sum([If(K, 1, 0), If(L, 1, 0), If(M, 1, 0)]) >= 1)  # chemist
solver.add(Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)]) >= 1)  # zoologist

# Bot and zoo counts
bot_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zool_count = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
# If more than one botanist is selected, then at most one zoologist is selected
solver.add(Implies(bot_count > 1, zool_count <= 1))

# Additional constraints
solver.add(Not(And(F, K)))          # F and K cannot both be selected
solver.add(Not(And(K, M)))          # K and M cannot both be selected
solver.add(Implies(M, And(P, R)))   # If M selected, then P and R must be selected

# Options mapping
options = [('A', G), ('B', H), ('C', K), ('D', M), ('E', P)]

found_options = []
for letter, var in options:
    solver.push()
    solver.add(var)  # force this option to be selected
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')