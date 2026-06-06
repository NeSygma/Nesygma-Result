from z3 import *

# Declare Bool variables for each scientist
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# Helper to count selected in a list
def count_selected(vars_list):
    return Sum([If(v, 1, 0) for v in vars_list])

# Base constraints
# Exactly 5 scientists selected
solver.add(count_selected([F, G, H, K, L, M, P, Q, R]) == 5)

# At least one of each type
bot_sum = count_selected([F, G, H])
chem_sum = count_selected([K, L, M])
zoo_sum = count_selected([P, Q, R])
solver.add(bot_sum >= 1)
solver.add(chem_sum >= 1)
solver.add(zoo_sum >= 1)

# If more than one botanist, then at most one zoologist
solver.add(Implies(bot_sum > 1, zoo_sum <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))
# K and M cannot both be selected
solver.add(Not(And(K, M)))
# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: M is the only chemist selected
solver.add(M == True)
solver.add(K == False)
solver.add(L == False)
solver.add(chem_sum == 1)  # redundant but explicit

# Define option constraints as the NEGATION of each answer choice
opt_a_constr = Or(Not(F), Not(G))          # not (F and G)
opt_b_constr = Or(Not(G), Not(H))          # not (G and H)
opt_c_constr = Or(Not(H), Not(P))          # not (H and P)
opt_d_constr = Or(Not(F), Not(G), Not(H))  # not (F and G and H)
opt_e_constr = Or(Not(P), Not(Q), Not(R))  # not (P and Q and R)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

all_letters = {"A", "B", "C", "D", "E"}
forced_options = all_letters - set(found_options)

if len(forced_options) == 1:
    print("STATUS: sat")
    answer = forced_options.pop()
    print(f"answer:{answer}")
elif len(forced_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options found {forced_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")