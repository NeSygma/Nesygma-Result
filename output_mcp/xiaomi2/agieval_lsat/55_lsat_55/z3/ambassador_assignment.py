from z3 import *

solver = Solver()

# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
# Countries: 0=unassigned, 1=Venezuela, 2=Yemen, 3=Zambia
candidates = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']
assign = [Int(f'assign_{c}') for c in candidates]

# Each assignment is 0 (unassigned), 1 (Venezuela), 2 (Yemen), or 3 (Zambia)
for a in assign:
    solver.add(Or(a == 0, a == 1, a == 2, a == 3))

# Exactly 3 candidates are assigned (each to a distinct country)
# Countries 1, 2, 3 must each appear exactly once
for country in [1, 2, 3]:
    solver.add(Sum([If(a == country, 1, 0) for a in assign]) == 1)

# No candidate assigned to more than one country (already handled by single Int variable)

# Constraint 1: Exactly one of Kayne or Novetzke is assigned
solver.add(Xor(assign[1] != 0, assign[3] != 0))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(assign[0] != 0, assign[1] != 0))

# Constraint 3: If Ong is assigned to Venezuela, Kayne is NOT assigned to Yemen
solver.add(Implies(assign[4] == 1, assign[1] != 2))

# Constraint 4: If Landon is assigned, it is to Zambia
solver.add(Implies(assign[2] != 0, assign[2] == 3))

# Now check each answer choice for which pair could be the two NOT assigned
# (A) Jaramillo and Novetzke not assigned
opt_a = And(assign[0] == 0, assign[3] == 0)
# (B) Jaramillo and Ong not assigned
opt_b = And(assign[0] == 0, assign[4] == 0)
# (C) Kayne and Landon not assigned
opt_c = And(assign[1] == 0, assign[2] == 0)
# (D) Kayne and Novetzke not assigned
opt_d = And(assign[1] == 0, assign[3] == 0)
# (E) Landon and Ong not assigned
opt_e = And(assign[2] == 0, assign[4] == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: {[(candidates[i], m[assign[i]]) for i in range(5)]}")
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