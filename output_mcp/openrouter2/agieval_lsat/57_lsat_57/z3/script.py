from z3 import *

# Constants for ambassadors
JARAMILLO = 0
KAYNE = 1
LANDON = 2
NOVETZKE = 3
ONG = 4

solver = Solver()

# Variables for each country assignment
assign_V = Int('assign_V')  # Venezuela
assign_Y = Int('assign_Y')  # Yemen
assign_Z = Int('assign_Z')  # Zambia

# Domain constraints
solver.add(assign_V >= 0, assign_V <= 4)
solver.add(assign_Y >= 0, assign_Y <= 4)
solver.add(assign_Z >= 0, assign_Z <= 4)

# Distinctness: one ambassador per country, no repeats
solver.add(Distinct(assign_V, assign_Y, assign_Z))

# Kayne is assigned to Yemen (given in question)
solver.add(assign_Y == KAYNE)

# Exactly one of Kayne or Novetzke is assigned to any country
solver.add(Sum([If(assign_V == KAYNE, 1, 0),
                If(assign_Y == KAYNE, 1, 0),
                If(assign_Z == KAYNE, 1, 0),
                If(assign_V == NOVETZKE, 1, 0),
                If(assign_Y == NOVETZKE, 1, 0),
                If(assign_Z == NOVETZKE, 1, 0)]) == 1)

# If Jaramillo is assigned, then Kayne is assigned (already satisfied by Kayne in Yemen)
solver.add(Implies(Or(assign_V == JARAMILLO,
                     assign_Y == JARAMILLO,
                     assign_Z == JARAMILLO),
                   Or(assign_V == KAYNE,
                      assign_Y == KAYNE,
                      assign_Z == KAYNE)))

# If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
solver.add(Implies(assign_V == ONG, assign_Y != KAYNE))

# Landon can only be assigned to Zambia
solver.add(assign_V != LANDON)
solver.add(assign_Y != LANDON)

# Option constraints
opt_a_constr = assign_V == JARAMILLO
opt_b_constr = assign_Z == LANDON
opt_c_constr = assign_Z == ONG
opt_d_constr = And(assign_V != JARAMILLO, assign_Y != JARAMILLO, assign_Z != JARAMILLO)
opt_e_constr = And(assign_V != ONG, assign_Y != ONG, assign_Z != ONG)

# Evaluate options
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