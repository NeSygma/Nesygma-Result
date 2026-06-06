from z3 import *

# Decision variables for positions (1..7)
O = Int('O')  # Optometrist
P = Int('P')  # Pharmacy
R1 = Int('R1')  # Restaurant 1
R2 = Int('R2')  # Restaurant 2
S = Int('S')  # Shoe store
T = Int('T')  # Toy store
V = Int('V')  # Veterinarian

solver = Solver()

# Domain constraints
vars = [O, P, R1, R2, S, T, V]
for v in vars:
    solver.add(v >= 1, v <= 7)

# All distinct
solver.add(Distinct(vars))

# Given condition: Veterinarian is in space 5
solver.add(V == 5)

# Pharmacy at an end (1 or 7)
solver.add(Or(P == 1, P == 7))

# One restaurant at the opposite end
# If P==1 then some restaurant ==7, else if P==7 then some restaurant ==1
solver.add(Or(And(P == 1, Or(R1 == 7, R2 == 7)),
               And(P == 7, Or(R1 == 1, R2 == 1))))

# Restaurants separated by at least two other businesses: distance >=3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Pharmacy adjacent to either optometrist or veterinarian
solver.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))

# Toy store not adjacent to veterinarian
solver.add(Abs(T - V) != 1)

# --- Multiple choice option constraints (negations) ---
# We will test the negation of each option; if the negation is UNSAT, the option must be true.
opt_a_constr = Not(O == 2)          # A: Optometrist is in space 2
opt_b_constr = Not(P == 7)          # B: Pharmacy is in space 7
opt_c_constr = Not(Or(R1 == 4, R2 == 4))  # C: A restaurant is in space 4
opt_d_constr = Not(S == 6)          # D: Shoe store is in space 6
opt_e_constr = Not(T == 3)          # E: Toy store is in space 3

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # The negation is satisfiable => the option is NOT forced
        found_options.append(letter)
    solver.pop()

# Options that are forced are those NOT in found_options
all_opts = {"A", "B", "C", "D", "E"}
forced = list(all_opts - set(found_options))

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: forced options {forced}, non‑forced {found_options}")