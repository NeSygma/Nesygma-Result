from z3 import *

solver = Solver()

# 7 spaces, numbered 1 to 7
# We'll assign each business to a space number.
# Businesses: optometrist (O), pharmacy (P), restaurant1 (R1), restaurant2 (R2),
# shoe store (S), toy store (T), veterinarian (V)

# Use integer variables for each business's space
O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')

# Domain: each business in 1..7
businesses = [O, P, R1, R2, S, T, V]
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All different spaces
solver.add(Distinct(businesses))

# Constraint 1: Pharmacy at one end, one of the restaurants at the other.
solver.add(Or(P == 1, P == 7))
solver.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
# The pharmacy and the restaurant at the ends must be opposite ends.
# If P==1 then one restaurant is 7; if P==7 then one restaurant is 1.
solver.add(Or(And(P == 1, Or(R1 == 7, R2 == 7)),
              And(P == 7, Or(R1 == 1, R2 == 1))))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# That means |R1 - R2| >= 3 (since at least 2 businesses between them)
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian.
solver.add(Or(Or(P - O == 1, O - P == 1),
              Or(P - V == 1, V - P == 1)))

# Constraint 4: Toy store cannot be next to veterinarian.
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Given: Shoe store is in space 2.
solver.add(S == 2)

# Now evaluate each option
found_options = []

# Option A: Optometrist is in space 5
opt_a = (O == 5)

# Option B: Pharmacy is in space 1
opt_b = (P == 1)

# Option C: A restaurant is in space 3
opt_c = Or(R1 == 3, R2 == 3)

# Option D: Toy store is in space 6
opt_d = (T == 6)

# Option E: Veterinarian is in space 4
opt_e = (V == 4)

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