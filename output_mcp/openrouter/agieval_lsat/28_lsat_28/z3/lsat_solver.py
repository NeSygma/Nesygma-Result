from z3 import *

# Define Bool variables for each scientist
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# Helper to count selected of a list

def count_selected(vars_list):
    return Sum([If(v, 1, 0) for v in vars_list])

solver = Solver()

# Base constraints
# Exactly 5 selected
solver.add(count_selected([F,G,H,K,L,M,P,Q,R]) == 5)

# At least one of each type
solver.add(count_selected([F,G,H]) >= 1)  # botanists
solver.add(count_selected([K,L,M]) >= 1)  # chemists
solver.add(count_selected([P,Q,R]) >= 1)  # zoologists

# If more than one botanist then at most one zoologist
bot_cnt = count_selected([F,G,H])
zoo_cnt = count_selected([P,Q,R])
solver.add(Or(bot_cnt <= 1, zoo_cnt <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))
# K and M cannot both be selected
solver.add(Not(And(K, M)))
# If M selected then both P and R selected
solver.add(Implies(M, And(P, R)))

# Premise: P is the only zoologist selected
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Since R is false, M cannot be selected (because M -> R)
solver.add(M == False)

# Define option constraints (negations of the condition) to test if they can be violated
# Option A: If K selected then G cannot be selected. Negation: K and G
opt_a = And(K, G)
# Option B: If L selected then F cannot be selected. Negation: L and F
opt_b = And(L, F)
# Option C: If exactly one chemist selected, it must be K.
# Negation: exactly one chemist selected AND that chemist is not K (i.e., L or M). Since M is false, it's L.
opt_c = And(count_selected([K,L,M]) == 1, L == True)
# Option D: If exactly two chemists selected, F cannot be selected.
# Negation: exactly two chemists selected AND F selected.
opt_d = And(count_selected([K,L,M]) == 2, F == True)
# Option E: If exactly two chemists selected, G cannot be selected.
# Negation: exactly two chemists selected AND G selected.
opt_e = And(count_selected([K,L,M]) == 2, G == True)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    # Add the negation of the option; if this leads to UNSAT, the original option must be true.
    solver.add(constr)
    res = solver.check()
    if res == unsat:
        # The option cannot be violated, so it must be true.
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