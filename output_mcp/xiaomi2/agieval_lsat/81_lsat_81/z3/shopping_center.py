from z3 import *

# Variables: each business assigned to a space 1-7
O = Int('O')   # Optometrist
P = Int('P')   # Pharmacy
R1 = Int('R1') # Restaurant 1
R2 = Int('R2') # Restaurant 2
S = Int('S')   # Shoe Store
T = Int('T')   # Toy Store
V = Int('V')   # Veterinarian

businesses = [O, P, R1, R2, S, T, V]

def add_base(solver):
    for b in businesses:
        solver.add(b >= 1, b <= 7)
    solver.add(Distinct(businesses))

# Constraint 1: Pharmacy at one end, one restaurant at the other
c1 = Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
)

# Constraint 2: Two restaurants separated by at least two other businesses
# |R1 - R2| >= 3
c2 = Or(R1 - R2 >= 3, R2 - R1 >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
c3 = Or(
    Or(P - O == 1, O - P == 1),
    Or(P - V == 1, V - P == 1)
)

# Constraint 4: Toy store not next to veterinarian
c4 = And(T - V != 1, V - T != 1)

# Answer choice constraints
# (A) A restaurant must be in either space 3, space 4, or space 5.
opt_a = Or(R1 == 3, R1 == 4, R1 == 5, R2 == 3, R2 == 4, R2 == 5)

# (B) A restaurant must be next to either the optometrist or the veterinarian.
opt_b = Or(
    Or(R1 - O == 1, O - R1 == 1, R1 - V == 1, V - R1 == 1),
    Or(R2 - O == 1, O - R2 == 1, R2 - V == 1, V - R2 == 1)
)

# (C) Either the toy store or the veterinarian must be somewhere between the two restaurants.
min_r = If(R1 < R2, R1, R2)
max_r = If(R1 < R2, R2, R1)
opt_c = Or(
    And(T > min_r, T < max_r),
    And(V > min_r, V < max_r)
)

# (D) No more than two businesses can separate the pharmacy and the restaurant nearest it.
# "No more than two businesses between" means distance <= 3
dist1 = If(P >= R1, P - R1, R1 - P)
dist2 = If(P >= R2, P - R2, R2 - P)
min_dist = If(dist1 <= dist2, dist1, dist2)
opt_d = min_dist <= 3

# (E) The optometrist cannot be next to the shoe store.
opt_e = And(O - S != 1, S - O != 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []

for letter, opt_constr in options:
    # Direction 1: {c1, c2, c3, c4} implies opt_constr?
    s1 = Solver()
    add_base(s1)
    s1.add(c1, c2, c3, c4, Not(opt_constr))
    dir1 = s1.check()

    # Direction 2: {c1, c3, c4, opt_constr} implies c2?
    s2 = Solver()
    add_base(s2)
    s2.add(c1, c3, c4, opt_constr, Not(c2))
    dir2 = s2.check()

    print(f"Option {letter}: dir1(implies option)={dir1}, dir2(implies c2)={dir2}")

    if dir1 == unsat and dir2 == unsat:
        found_options.append(letter)

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")