from z3 import *

solver = Solver()

# Constants for countries
V, Y, Z = 0, 1, 2

# Constants for candidates
J, K, L, N, O = 0, 1, 2, 3, 4

# Ambassador for each country: integer variables 0..4
amb = [Int(f'amb_{c}') for c in range(3)]

# Domain: each ambassador is one of the 5 candidates
for c in range(3):
    solver.add(amb[c] >= 0, amb[c] <= 4)

# No candidate assigned to more than one country
solver.add(Distinct(amb))

# --- Constraint 1: Either Kayne or Novetzke, but not both, is assigned ---
k_assigned = Or([amb[c] == K for c in range(3)])
n_assigned = Or([amb[c] == N for c in range(3)])
solver.add(Or(And(k_assigned, Not(n_assigned)), And(Not(k_assigned), n_assigned)))

# --- Constraint 2: If Jaramillo is assigned, then Kayne is assigned ---
j_assigned = Or([amb[c] == J for c in range(3)])
solver.add(Implies(j_assigned, k_assigned))

# --- Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen ---
solver.add(Implies(amb[V] == O, amb[Y] != K))

# --- Constraint 4: If Landon is assigned, it is to Zambia ---
l_assigned = Or([amb[c] == L for c in range(3)])
solver.add(Implies(l_assigned, amb[Z] == L))

# --- Question condition: Kayne is assigned to Yemen ---
solver.add(amb[Y] == K)

# --- Define options ---
# (A) Jaramillo is assigned to Venezuela
opt_a = (amb[V] == J)
# (B) Landon is assigned to Zambia
opt_b = (amb[Z] == L)
# (C) Ong is assigned to Zambia
opt_c = (amb[Z] == O)
# (D) Jaramillo is not assigned to an ambassadorship
opt_d = Not(j_assigned)
# (E) Ong is not assigned to an ambassadorship
o_assigned = Or([amb[c] == O for c in range(3)])
opt_e = Not(o_assigned)

# For "must be true": test if the NEGATION of each option is unsatisfiable
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))  # Test if option can be false
    if solver.check() == unsat:  # If false is impossible, option must be true
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