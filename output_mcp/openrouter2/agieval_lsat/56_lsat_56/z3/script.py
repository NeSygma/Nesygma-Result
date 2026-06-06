from z3 import *

solver = Solver()

# Ambassador indices
J = 0
K = 1
L = 2
N = 3
O = 4
all_ambassadors = [J, K, L, N, O]

# Variables for each country
amb_V, amb_Y, amb_Z = Ints('amb_V amb_Y amb_Z')

# Domain constraints
solver.add(amb_V >= 0, amb_V < 5)
solver.add(amb_Y >= 0, amb_Y < 5)
solver.add(amb_Z >= 0, amb_Z < 5)

# Distinct ambassadors for each country
solver.add(Distinct(amb_V, amb_Y, amb_Z))

# Base constraints
Kayne_assigned = Or(amb_V == K, amb_Y == K, amb_Z == K)
Novetzke_assigned = Or(amb_V == N, amb_Y == N, amb_Z == N)
solver.add(Kayne_assigned != Novetzke_assigned)

Jaramillo_assigned = Or(amb_V == J, amb_Y == J, amb_Z == J)
solver.add(Implies(Jaramillo_assigned, Kayne_assigned))

solver.add(Implies(amb_V == O, amb_Y != K))

Landon_assigned = Or(amb_V == L, amb_Y == L, amb_Z == L)
solver.add(Implies(Landon_assigned, amb_Z == L))

# Ong assigned to Venezuela
solver.add(amb_V == O)

# Helper to create pair constraints

def pair_constraint(pair):
    constraints = []
    for a in pair:
        constraints.append(Or(amb_Y == a, amb_Z == a))
    for b in all_ambassadors:
        if b not in pair:
            constraints.append(amb_Y != b)
            constraints.append(amb_Z != b)
    return And(constraints)

opt_a_constr = pair_constraint([J, L])  # Jaramillo and Landon
opt_b_constr = pair_constraint([J, N])  # Jaramillo and Novetzke
opt_c_constr = pair_constraint([K, L])  # Kayne and Landon
opt_d_constr = pair_constraint([K, N])  # Kayne and Novetzke
opt_e_constr = pair_constraint([L, N])  # Landon and Novetzke

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