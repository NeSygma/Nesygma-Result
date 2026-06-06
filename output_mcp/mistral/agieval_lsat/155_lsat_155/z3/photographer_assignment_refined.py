from z3 import *

# Base constraints solver
solver = Solver()

# Photographers: 0=not assigned, 1=Silva, 2=Thorne
frost = Int('frost')
gonzalez = Int('gonzalez')
heideck = Int('heideck')
knutson = Int('knutson')
lai = Int('lai')
mays = Int('mays')

# Each photographer is either not assigned, assigned to Silva, or assigned to Thorne
solver.add(frost >= 0, frost <= 2)
solver.add(gonzalez >= 0, gonzalez <= 2)
solver.add(heideck >= 0, heideck <= 2)
solver.add(knutson >= 0, knutson <= 2)
solver.add(lai >= 0, lai <= 2)
solver.add(mays >= 0, mays <= 2)

# Constraint 1: Each ceremony must have at least 2 photographers
silva_photographers = [frost, gonzalez, heideck, knutson, lai, mays]
silva_count = Sum([If(p == 1, 1, 0) for p in silva_photographers])
thorne_count = Sum([If(p == 2, 1, 0) for p in silva_photographers])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Constraint 2: Frost must be assigned together with Heideck to one of the ceremonies
# They must both be assigned to the same ceremony (not both unassigned)
solver.add(Or(And(frost == 1, heideck == 1), And(frost == 2, heideck == 2)))

# Constraint 3: If Lai and Mays are both assigned, they must be at different ceremonies
solver.add(Implies(And(lai != 0, mays != 0), lai != mays))

# Constraint 4: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(gonzalez == 1, lai == 2))

# Constraint 5: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(knutson != 2, And(heideck == 2, mays == 2)))

# Evaluate each option
found_options = []

# Option A: Silva: Gonzalez, Lai; Thorne: Frost, Heideck, Mays
solver.push()
solver.add(gonzalez == 1)
solver.add(lai == 1)
solver.add(frost == 2)
solver.add(heideck == 2)
solver.add(mays == 2)
solver.add(knutson == 0)  # Not assigned in A
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Silva: Gonzalez, Mays; Thorne: Knutson, Lai
solver.push()
solver.add(gonzalez == 1)
solver.add(mays == 1)
solver.add(knutson == 2)
solver.add(lai == 2)
solver.add(frost == 0)  # Not assigned in B
solver.add(heideck == 0)  # Not assigned in B
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Silva: Frost, Gonzalez, Heideck; Thorne: Knutson, Lai, Mays
solver.push()
solver.add(frost == 1)
solver.add(gonzalez == 1)
solver.add(heideck == 1)
solver.add(knutson == 2)
solver.add(lai == 2)
solver.add(mays == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Lai
solver.push()
solver.add(frost == 1)
solver.add(heideck == 1)
solver.add(mays == 1)
solver.add(gonzalez == 2)
solver.add(lai == 2)
solver.add(knutson == 0)  # Not assigned in D
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Silva: Frost, Heideck, Mays; Thorne: Gonzalez, Knutson, Lai
solver.push()
solver.add(frost == 1)
solver.add(heideck == 1)
solver.add(mays == 1)
solver.add(gonzalez == 2)
solver.add(knutson == 2)
solver.add(lai == 2)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")