from z3 import *

solver = Solver()

# 7 spaces, numbered 1 to 7
# We'll assign each business a space number (1-7)
# Businesses: optometrist (O), pharmacy (P), restaurant1 (R1), restaurant2 (R2),
#             shoe store (S), toy store (T), veterinarian (V)

O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')

# All distinct and in range 1..7
businesses = [O, P, R1, R2, S, T, V]
solver.add(Distinct(businesses))
for b in businesses:
    solver.add(b >= 1, b <= 7)

# Constraint 1: Pharmacy at one end, one of the restaurants at the other.
solver.add(Or(P == 1, P == 7))
solver.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
# The pharmacy and the restaurant at the ends must be opposite ends.
# If P==1 then one restaurant is at 7; if P==7 then one restaurant is at 1.
solver.add(Implies(P == 1, Or(R1 == 7, R2 == 7)))
solver.add(Implies(P == 7, Or(R1 == 1, R2 == 1)))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# |R1 - R2| >= 3 (since at least 2 businesses between them means distance >= 3)
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian.
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Constraint 4: Toy store cannot be next to veterinarian.
solver.add(Not(Abs(T - V) == 1))

# Additional constraint from the question: Veterinarian is in space 5.
solver.add(V == 5)

# Now evaluate each option
# Option A: The optometrist is in space 2.
opt_a = (O == 2)

# Option B: The pharmacy is in space 7.
opt_b = (P == 7)

# Option C: A restaurant is in space 4.
opt_c = Or(R1 == 4, R2 == 4)

# Option D: The shoe store is in space 6.
opt_d = (S == 6)

# Option E: The toy store is in space 3.
opt_e = (T == 3)

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