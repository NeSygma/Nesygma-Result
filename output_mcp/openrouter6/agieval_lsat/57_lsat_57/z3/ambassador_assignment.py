from z3 import *

solver = Solver()

# Countries: 0: Venezuela, 1: Yemen, 2: Zambia
# Candidates: 0: Jaramillo, 1: Kayne, 2: Landon, 3: Novetzke, 4: Ong

assign = [Int(f'assign_{i}') for i in range(3)]

# Each assignment is between 0 and 4
for i in range(3):
    solver.add(assign[i] >= 0)
    solver.add(assign[i] <= 4)

# All assignments are distinct
solver.add(Distinct(assign))

# Premise: Kayne assigned to Yemen (index 1)
solver.add(assign[1] == 1)

# Constraint 1: Exactly one of Kayne (1) or Novetzke (3) is assigned
is_kayne_assigned = Or([assign[i] == 1 for i in range(3)])
is_novetzke_assigned = Or([assign[i] == 3 for i in range(3)])
solver.add(is_kayne_assigned != is_novetzke_assigned)  # XOR

# Constraint 2: If Jaramillo assigned, then Kayne assigned
is_jaramillo_assigned = Or([assign[i] == 0 for i in range(3)])
solver.add(Implies(is_jaramillo_assigned, is_kayne_assigned))

# Constraint 3: If Ong assigned to Venezuela, then Kayne not assigned to Yemen
# Venezuela is index 0, Yemen is index 1
solver.add(Implies(assign[0] == 4, assign[1] != 1))

# Constraint 4: If Landon assigned, then assigned to Zambia (index 2)
# For each i, if assign[i] == 2 then i == 2
for i in range(3):
    solver.add(Implies(assign[i] == 2, i == 2))

# Now define options as constraints
opt_a_constr = assign[0] == 0  # Jaramillo to Venezuela
opt_b_constr = assign[2] == 2  # Landon to Zambia
opt_c_constr = assign[2] == 4  # Ong to Zambia
# Jaramillo not assigned: means Jaramillo not in assign
opt_d_constr = Not(Or([assign[i] == 0 for i in range(3)]))
# Ong not assigned: means Ong not in assign
opt_e_constr = Not(Or([assign[i] == 4 for i in range(3)]))

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