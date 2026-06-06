from z3 import *

# Declare Bool variables for each scientist
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# Helper to sum Bool variables as integers
def bool_sum(vars_list):
    return Sum([If(v, 1, 0) for v in vars_list])

# Base constraints
base = []
# Exactly 5 selected
base.append(bool_sum([F,G,H,K,L,M,P,Q,R]) == 5)
# At least one of each type
base.append(bool_sum([F,G,H]) >= 1)  # botanists
base.append(bool_sum([K,L,M]) >= 1)  # chemists
base.append(bool_sum([P,Q,R]) >= 1)  # zoologists
# If more than one botanist then at most one zoologist
base.append(Implies(bool_sum([F,G,H]) >= 2, bool_sum([P,Q,R]) <= 1))
# F and K cannot both be selected
base.append(Or(Not(F), Not(K)))
# K and M cannot both be selected
base.append(Or(Not(K), Not(M)))
# If M selected then both P and R must be selected
base.append(Implies(M, And(P, R)))

# Function to create constraint for a given selection set
def selection_constraint(selected_set):
    # selected_set is a set of variable names as strings
    mapping = {
        'F': F, 'G': G, 'H': H,
        'K': K, 'L': L, 'M': M,
        'P': P, 'Q': Q, 'R': R
    }
    constraints = []
    for name, var in mapping.items():
        if name in selected_set:
            constraints.append(var == True)
        else:
            constraints.append(var == False)
    return And(constraints)

# Define each option's selection set
opt_a_set = {'F','G','K','P','Q'}
opt_b_set = {'G','H','K','L','M'}
opt_c_set = {'G','H','K','L','R'}
opt_d_set = {'H','K','M','P','R'}
opt_e_set = {'H','L','M','P','Q'}

opt_a_constr = selection_constraint(opt_a_set)
opt_b_constr = selection_constraint(opt_b_set)
opt_c_constr = selection_constraint(opt_c_set)
opt_d_constr = selection_constraint(opt_d_set)
opt_e_constr = selection_constraint(opt_e_set)

solver = Solver()
# Add base constraints
for c in base:
    solver.add(c)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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