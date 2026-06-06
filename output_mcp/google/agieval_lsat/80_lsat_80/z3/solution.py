from z3 import *

# Businesses
# O: Optometrist, P: Pharmacy, R1: Restaurant 1, R2: Restaurant 2, S: Shoe store, T: Toy store, V: Veterinarian
businesses = ['O', 'P', 'R1', 'R2', 'S', 'T', 'V']
pos = {b: Int(b) for b in businesses}

solver = Solver()

# Domain constraints
for b in businesses:
    solver.add(pos[b] >= 1, pos[b] <= 7)

# All distinct
solver.add(Distinct([pos[b] for b in businesses]))

# Constraint 1: Pharmacy at one end, one restaurant at the other
# (P=1 and (R1=7 or R2=7)) or (P=7 and (R1=1 or R2=1))
solver.add(Or(
    And(pos['P'] == 1, Or(pos['R1'] == 7, pos['R2'] == 7)),
    And(pos['P'] == 7, Or(pos['R1'] == 1, pos['R2'] == 1))
))

# Constraint 2: Two restaurants separated by at least two other businesses
# |pos[R1] - pos[R2]| >= 3
solver.add(Abs(pos['R1'] - pos['R2']) >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
# If P=1, then O=2 or V=2. If P=7, then O=6 or V=6.
solver.add(Or(
    And(pos['P'] == 1, Or(pos['O'] == 2, pos['V'] == 2)),
    And(pos['P'] == 7, Or(pos['O'] == 6, pos['V'] == 6))
))

# Constraint 4: Toy store cannot be next to veterinarian
# |pos[T] - pos[V]| > 1
solver.add(Abs(pos['T'] - pos['V']) > 1)

# Constraint 5: Shoe store is in space 4
solver.add(pos['S'] == 4)

# Define options
# (A) The optometrist is next to a restaurant.
opt_a = Or(Abs(pos['O'] - pos['R1']) == 1, Abs(pos['O'] - pos['R2']) == 1)
# (B) The pharmacy is next to the veterinarian.
opt_b = Abs(pos['P'] - pos['V']) == 1
# (C) A restaurant is next to the toy store.
opt_c = Or(Abs(pos['R1'] - pos['T']) == 1, Abs(pos['R2'] - pos['T']) == 1)
# (D) The shoe store is next to the toy store.
opt_d = Abs(pos['S'] - pos['T']) == 1
# (E) The shoe store is next to the veterinarian.
opt_e = Abs(pos['S'] - pos['V']) == 1

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# Check which option MUST be true
# An option must be true if its negation is unsatisfiable
must_be_true = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")