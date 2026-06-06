from z3 import *

solver = Solver()

# Countries: Venezuela, Yemen, Zambia
# We'll assign each country an ambassador (0-4 representing the candidates)
# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4

Venezuela, Yemen, Zambia = Ints('Venezuela Yemen Zambia')

countries = [Venezuela, Yemen, Zambia]

# Domain: each country gets one of the 5 candidates
for c in countries:
    solver.add(c >= 0, c <= 4)

# Each candidate assigned to at most one country (distinct assignments)
solver.add(Distinct(countries))

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned to one of the ambassadorships.
# Exactly one of {Kayne, Novetzke} is assigned to some country.
solver.add(Sum([If(Venezuela == 1, 1, 0), If(Yemen == 1, 1, 0), If(Zambia == 1, 1, 0)]) + 
           Sum([If(Venezuela == 3, 1, 0), If(Yemen == 3, 1, 0), If(Zambia == 3, 1, 0)]) == 1)

# Constraint 2: If Jaramillo(0) is assigned to one of the ambassadorships, then so is Kayne(1).
# If Jaramillo is assigned somewhere, Kayne must be assigned somewhere.
solver.add(Implies(
    Or([Venezuela == 0, Yemen == 0, Zambia == 0]),
    Or([Venezuela == 1, Yemen == 1, Zambia == 1])
))

# Constraint 3: If Ong(4) is assigned as ambassador to Venezuela, Kayne(1) is not assigned as ambassador to Yemen.
solver.add(Implies(Venezuela == 4, Yemen != 1))

# Constraint 4: If Landon(2) is assigned to an ambassadorship, it is to Zambia.
solver.add(Implies(
    Or([Venezuela == 2, Yemen == 2, Zambia == 2]),
    Zambia == 2
))

# Additional condition: Kayne is assigned as ambassador to Yemen.
solver.add(Yemen == 1)

# Now evaluate each option
# Option A: Jaramillo is assigned as ambassador to Venezuela.
opt_a = (Venezuela == 0)

# Option B: Landon is assigned as ambassador to Zambia.
opt_b = (Zambia == 2)

# Option C: Ong is assigned as ambassador to Zambia.
opt_c = (Zambia == 4)

# Option D: Jaramillo is not assigned to an ambassadorship.
opt_d = And(Venezuela != 0, Yemen != 0, Zambia != 0)

# Option E: Ong is not assigned to an ambassadorship.
opt_e = And(Venezuela != 4, Yemen != 4, Zambia != 4)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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