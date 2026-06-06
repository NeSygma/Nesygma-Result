from z3 import *

# 7 spaces (1-7), 7 businesses
# Businesses: optometrist(0), pharmacy(1), restaurant1(2), restaurant2(3), shoe_store(4), toy_store(5), veterinarian(6)
# We'll assign each business to a space

solver = Solver()

# Variables: space assignment for each business (1-7)
opt = Int('opt')
pharm = Int('pharm')
rest1 = Int('rest1')
rest2 = Int('rest2')
shoe = Int('shoe')
toy = Int('toy')
vet = Int('vet')

businesses = [opt, pharm, rest1, rest2, shoe, toy, vet]

# All in spaces 1-7
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All different
solver.add(Distinct(businesses))

# Constraint 1: Pharmacy at one end, one restaurant at the other
# Ends are space 1 and space 7
solver.add(Or(pharm == 1, pharm == 7))
solver.add(Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
))

# Constraint 2: Two restaurants separated by at least two other businesses
# |rest1 - rest2| >= 3
solver.add(Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3))

# Constraint 3: Pharmacy next to either optometrist or veterinarian
solver.add(Or(
    Or(pharm - opt == 1, opt - pharm == 1),
    Or(pharm - vet == 1, vet - pharm == 1)
))

# Constraint 4: Toy store cannot be next to veterinarian
solver.add(Not(Or(toy - vet == 1, vet - toy == 1)))

# Find all valid arrangements under original constraints
original_solutions = []
decision_vars = businesses

while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(v).as_long() for v in decision_vars)
    original_solutions.append(sol)
    solver.add(Or([v != m.eval(v) for v in decision_vars]))

print(f"Original solutions count: {len(original_solutions)}")

# Now test each answer choice
# For each option, we replace constraint 2 with the new constraint
# and check if the set of solutions matches

def get_solutions_for_constraint(new_constraint):
    s = Solver()
    # Same variables
    opt2 = Int('opt2')
    pharm2 = Int('pharm2')
    rest1_2 = Int('rest1_2')
    rest2_2 = Int('rest2_2')
    shoe2 = Int('shoe2')
    toy2 = Int('toy2')
    vet2 = Int('vet2')
    biz2 = [opt2, pharm2, rest1_2, rest2_2, shoe2, toy2, vet2]
    
    for b in biz2:
        s.add(b >= 1, b <= 7)
    s.add(Distinct(biz2))
    
    # Constraint 1
    s.add(Or(pharm2 == 1, pharm2 == 7))
    s.add(Or(
        And(pharm2 == 1, Or(rest1_2 == 7, rest2_2 == 7)),
        And(pharm2 == 7, Or(rest1_2 == 1, rest2_2 == 1))
    ))
    
    # NEW constraint replaces constraint 2
    s.add(new_constraint(opt2, pharm2, rest1_2, rest2_2, shoe2, toy2, vet2))
    
    # Constraint 3
    s.add(Or(
        Or(pharm2 - opt2 == 1, opt2 - pharm2 == 1),
        Or(pharm2 - vet2 == 1, vet2 - pharm2 == 1)
    ))
    
    # Constraint 4
    s.add(Not(Or(toy2 - vet2 == 1, vet2 - toy2 == 1)))
    
    sols = []
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(v).as_long() for v in biz2)
        sols.append(sol)
        s.add(Or([v != m.eval(v) for v in biz2]))
    return sols

# Option A: A restaurant must be in either space 3, space 4, or space 5.
def opt_a(opt, pharm, rest1, rest2, shoe, toy, vet):
    return Or(
        Or(rest1 == 3, rest1 == 4, rest1 == 5),
        Or(rest2 == 3, rest2 == 4, rest2 == 5)
    )

# Option B: A restaurant must be next to either the optometrist or the veterinarian.
def opt_b(opt, pharm, rest1, rest2, shoe, toy, vet):
    return And(
        Or(
            Or(rest1 - opt == 1, opt - rest1 == 1),
            Or(rest1 - vet == 1, vet - rest1 == 1)
        ),
        Or(
            Or(rest2 - opt == 1, opt - rest2 == 1),
            Or(rest2 - vet == 1, vet - rest2 == 1)
        )
    )

# Option C: Either the toy store or the veterinarian must be somewhere between the two restaurants.
def opt_c(opt, pharm, rest1, rest2, shoe, toy, vet):
    # Between means: min(rest1,rest2) < x < max(rest1,rest2)
    lo = If(rest1 < rest2, rest1, rest2)
    hi = If(rest1 < rest2, rest2, rest1)
    return Or(
        And(toy > lo, toy < hi),
        And(vet > lo, vet < hi)
    )

# Option D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
def opt_d(opt, pharm, rest1, rest2, shoe, toy, vet):
    # |pharm - nearest_restaurant| <= 3 (at most 2 businesses between = distance <= 3)
    dist1 = If(pharm > rest1, pharm - rest1, rest1 - pharm)
    dist2 = If(pharm > rest2, pharm - rest2, rest2 - pharm)
    nearest_dist = If(dist1 < dist2, dist1, dist2)
    return nearest_dist <= 3

# Option E: The optometrist cannot be next to the shoe store.
def opt_e(opt, pharm, rest1, rest2, shoe, toy, vet):
    return Not(Or(opt - shoe == 1, shoe - opt == 1))

options = {
    "A": opt_a,
    "B": opt_b,
    "C": opt_c,
    "D": opt_d,
    "E": opt_e,
}

original_set = set(original_solutions)

for letter, constr_fn in options.items():
    sols = get_solutions_for_constraint(constr_fn)
    sol_set = set(sols)
    match = sol_set == original_set
    print(f"Option {letter}: {len(sols)} solutions, matches original: {match}")
    if not match:
        only_in_orig = original_set - sol_set
        only_in_new = sol_set - original_set
        print(f"  Only in original: {len(only_in_orig)}, Only in new: {len(only_in_new)}")