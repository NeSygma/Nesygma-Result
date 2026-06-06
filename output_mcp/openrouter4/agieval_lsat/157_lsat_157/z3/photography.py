from z3 import *

# Photographers: 0=not assigned, 1=Silva, 2=Thorne
frost, gonzalez, heideck, knutson, lai, mays = Ints('frost gonzalez heideck knutson lai mays')
photographers = [frost, gonzalez, heideck, knutson, lai, mays]

solver = Solver()

# Domain constraints: each photographer is either not assigned (0), Silva (1), or Thorne (2)
for p in photographers:
    solver.add(Or(p == 0, p == 1, p == 2))

# Constraint 1: Frost must be assigned together with Heideck to one of the graduation ceremonies.
solver.add(frost == heideck)
solver.add(frost != 0)

# Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies.
solver.add(Implies(And(lai != 0, mays != 0), lai != mays))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne.
solver.add(Implies(gonzalez == 1, lai == 2))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it.
solver.add(Implies(knutson != 2, And(heideck == 2, mays == 2)))

# At least 2 photographers at each ceremony
solver.add(Sum([If(p == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(p == 2, 1, 0) for p in photographers]) >= 2)

# Define the options
# Each option lists the COMPLETE assignment to Silva (exactly those photographers, no others at Silva)
options = {
    "A": {"listed": [frost, gonzalez, heideck, knutson], "unlisted": [lai, mays]},
    "B": {"listed": [frost, gonzalez, heideck], "unlisted": [knutson, lai, mays]},
    "C": {"listed": [gonzalez, knutson], "unlisted": [frost, heideck, lai, mays]},
    "D": {"listed": [heideck, lai], "unlisted": [frost, gonzalez, knutson, mays]},
    "E": {"listed": [knutson, mays], "unlisted": [frost, gonzalez, heideck, lai]},
}

found_options = []
for letter, opt in options.items():
    solver.push()
    # Listed photographers are assigned to Silva
    for p in opt["listed"]:
        solver.add(p == 1)
    # Unlisted photographers are NOT assigned to Silva
    for p in opt["unlisted"]:
        solver.add(p != 1)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT. Model:")
        for name, var in [("frost", frost), ("gonzalez", gonzalez), ("heideck", heideck), ("knutson", knutson), ("lai", lai), ("mays", mays)]:
            print(f"  {name} = {m[var]}")
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