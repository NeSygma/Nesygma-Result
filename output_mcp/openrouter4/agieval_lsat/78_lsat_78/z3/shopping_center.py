from z3 import *

solver = Solver()

# Define variables for each business: position 1-7
P = Int('Pharmacy')
O = Int('Optometrist')
V = Int('Veterinarian')
S = Int('ShoeStore')
T = Int('ToyStore')
# Two restaurants
R1 = Int('Restaurant1')
R2 = Int('Restaurant2')

businesses = [P, O, V, S, T, R1, R2]

# Domain: positions 1 through 7
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All distinct positions
solver.add(Distinct(businesses))

# Constraint 1: Pharmacy at one end, one restaurant at the other
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: The two restaurants separated by at least two other businesses
solver.add(Abs(R1 - R2) >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 4: Toy store cannot be next to veterinarian
solver.add(Abs(T - V) != 1)

# Given: Veterinarian is in space 5
solver.add(V == 5)

# Now evaluate each option: which MUST be true?
# For "must be true", we add the NEGATION of the option and check if UNSAT.
# If NOT(option) is UNSAT, then the option must hold in all valid models.

found_options = []
for letter, constr in [
    ("A", O == 2),
    ("B", P == 7),
    ("C", Or(R1 == 4, R2 == 4)),
    ("D", S == 6),
    ("E", T == 3)
]:
    solver.push()
    # Add NOT(option) — if this makes problem unsat, option must be true
    solver.add(Not(constr))
    if solver.check() == unsat:
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