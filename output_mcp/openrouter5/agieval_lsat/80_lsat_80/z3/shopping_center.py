from z3 import *

solver = Solver()

# 7 spaces, numbered 1 to 7
# We'll assign each business a space number (1-7)
# Businesses: optometrist (O), pharmacy (P), restaurant1 (R1), restaurant2 (R2),
# shoe store (S), toy store (T), veterinarian (V)

O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
businesses = [O, P, R1, R2, S, T, V]

# Each business gets a distinct space from 1 to 7
solver.add(Distinct(businesses))
for b in businesses:
    solver.add(b >= 1, b <= 7)

# Constraint 1: Pharmacy must be at one end (space 1 or 7) and one of the restaurants at the other.
solver.add(Or(P == 1, P == 7))
# One of the restaurants is at the opposite end
solver.add(Or(And(P == 1, Or(R1 == 7, R2 == 7)),
              And(P == 7, Or(R1 == 1, R2 == 1))))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# That means |R1 - R2| >= 3 (since at least 2 businesses between them means distance >= 3)
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: The pharmacy must be next to either the optometrist or the veterinarian.
# Next to means |P - O| == 1 or |P - V| == 1
solver.add(Or(Or(P - O == 1, O - P == 1),
              Or(P - V == 1, V - P == 1)))

# Constraint 4: The toy store cannot be next to the veterinarian.
# |T - V| != 1
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Additional condition: The shoe store is in space 4
solver.add(S == 4)

# Now evaluate each option
# Option A: The optometrist is next to a restaurant.
# i.e., |O - R1| == 1 or |O - R2| == 1
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