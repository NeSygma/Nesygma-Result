from z3 import *

solver = Solver()

# Countries: 0=Venezuela, 1=Yemen, 2=Zambia
# Candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong

# Assignment: country -> candidate
assign = [Int(f'assign_{c}') for c in range(3)]

# Each assignment is a candidate (0-4)
for c in range(3):
    solver.add(assign[c] >= 0, assign[c] <= 4)

# All different (no ambassador assigned to more than one country)
solver.add(Distinct(assign))

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned
kayne_assigned = Or([assign[c] == 1 for c in range(3)])
novetzke_assigned = Or([assign[c] == 3 for c in range(3)])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned
jaramillo_assigned = Or([assign[c] == 0 for c in range(3)])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong(4) is assigned to Venezuela(0), then Kayne(1) is not assigned to Yemen(1)
solver.add(Implies(assign[0] == 4, assign[1] != 1))

# Constraint 4: If Landon(2) is assigned, it is to Zambia(2)
landon_assigned = Or([assign[c] == 2 for c in range(3)])
solver.add(Implies(landon_assigned, assign[2] == 2))

# Now test each option
# (A) Venezuela: Jaramillo(0) Yemen: Ong(4) Zambia: Novetzke(3)
opt_a_constr = And(assign[0] == 0, assign[1] == 4, assign[2] == 3)
# (B) Venezuela: Kayne(1) Yemen: Jaramillo(0) Zambia: Landon(2)
opt_b_constr = And(assign[0] == 1, assign[1] == 0, assign[2] == 2)
# (C) Venezuela: Landon(2) Yemen: Novetzke(3) Zambia: Ong(4)
opt_c_constr = And(assign[0] == 2, assign[1] == 3, assign[2] == 4)
# (D) Venezuela: Novetzke(3) Yemen: Jaramillo(0) Zambia: Kayne(1)
opt_d_constr = And(assign[0] == 3, assign[1] == 0, assign[2] == 1)
# (E) Venezuela: Ong(4) Yemen: Kayne(1) Zambia: Landon(2)
opt_e_constr = And(assign[0] == 4, assign[1] == 1, assign[2] == 2)

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