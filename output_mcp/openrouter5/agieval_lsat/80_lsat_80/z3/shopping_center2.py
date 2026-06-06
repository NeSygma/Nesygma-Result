from z3 import *

solver = Solver()

# 7 spaces, numbered 1 to 7
O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
businesses = [O, P, R1, R2, S, T, V]

# Each business gets a distinct space from 1 to 7
solver.add(Distinct(businesses))
for b in businesses:
    solver.add(b >= 1, b <= 7)

# Constraint 1: Pharmacy at one end, one restaurant at the other end
solver.add(Or(P == 1, P == 7))
solver.add(Or(And(P == 1, Or(R1 == 7, R2 == 7)),
              And(P == 7, Or(R1 == 1, R2 == 1))))

# Constraint 2: Two restaurants separated by at least two other businesses
# |R1 - R2| >= 3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian
solver.add(Or(Or(P - O == 1, O - P == 1),
              Or(P - V == 1, V - P == 1)))

# Constraint 4: Toy store not next to veterinarian
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Given: Shoe store in space 4
solver.add(S == 4)

# Let's first enumerate all valid models to see what must be true
# We'll check each option more carefully

# Option A: The optometrist is next to a restaurant.
opt_a_constr = Or(Or(O - R1 == 1, R1 - O == 1),
                  Or(O - R2 == 1, R2 - O == 1))

# Option B: The pharmacy is next to the veterinarian.
opt_b_constr = Or(P - V == 1, V - P == 1)

# Option C: A restaurant is next to the toy store.
opt_c_constr = Or(Or(R1 - T == 1, T - R1 == 1),
                  Or(R2 - T == 1, T - R2 == 1))

# Option D: The shoe store is next to the toy store.
opt_d_constr = Or(S - T == 1, T - S == 1)

# Option E: The shoe store is next to the veterinarian.
opt_e_constr = Or(S - V == 1, V - S == 1)

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("Base model found:")
    for b in businesses:
        print(f"  {b} = {m[b]}")
else:
    print("Base constraints unsat!")
    exit()

# Now let's check each option more carefully.
# The question asks "which one of the following MUST be true?"
# So we need to check if an option is true in ALL valid models.
# If we add the NEGATION of an option and it's unsat, then the option MUST be true.

print("\nChecking which options MUST be true (negation test):")
must_be_true = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))  # If negating the option makes it unsat, the option must be true
    res = solver.check()
    print(f"  Option {letter} negation check: {res}")
    if res == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"\nOptions that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")