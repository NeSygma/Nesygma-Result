from z3 import *

def count_solutions(extra_constraint=None):
    """Count solutions with base constraints + optional extra constraint."""
    solver = Solver()
    
    opt = Int('opt')
    pharm = Int('pharm')
    rest1 = Int('rest1')
    rest2 = Int('rest2')
    shoe = Int('shoe')
    toy = Int('toy')
    vet = Int('vet')
    
    businesses = [opt, pharm, rest1, rest2, shoe, toy, vet]
    
    for b in businesses:
        solver.add(b >= 1, b <= 7)
    solver.add(Distinct(businesses))
    
    # Constraint 1: Pharmacy at one end, one restaurant at the other
    solver.add(Or(pharm == 1, pharm == 7))
    solver.add(Or(
        And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
        And(pharm == 7, Or(rest1 == 1, rest2 == 1))
    ))
    
    # Constraint 3: Pharmacy next to either optometrist or veterinarian
    solver.add(Or(
        Or(pharm - opt == 1, opt - pharm == 1),
        Or(pharm - vet == 1, vet - pharm == 1)
    ))
    
    # Constraint 4: Toy store cannot be next to veterinarian
    solver.add(Not(Or(toy - vet == 1, vet - toy == 1)))
    
    if extra_constraint is not None:
        solver.add(extra_constraint)
    
    count = 0
    while solver.check() == sat:
        m = solver.model()
        count += 1
        # Block this solution
        solver.add(Or([b != m[b] for b in businesses]))
    
    return count

# Original constraint: two restaurants separated by at least 2 other businesses
# |rest1 - rest2| >= 3
rest1, rest2 = Ints('rest1 rest2')
original_constr = Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3)

# Option A: A restaurant must be in either space 3, space 4, or space 5.
opt_a_constr = Or(
    Or(rest1 == 3, rest1 == 4, rest1 == 5),
    Or(rest2 == 3, rest2 == 4, rest2 == 5)
)

# Option B: A restaurant must be next to either the optometrist or the veterinarian.
opt = Int('opt')
vet = Int('vet')
opt_b_constr = And(
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
toy = Int('toy')
lo = If(rest1 < rest2, rest1, rest2)
hi = If(rest1 < rest2, rest2, rest1)
opt_c_constr = Or(
    And(toy > lo, toy < hi),
    And(vet > lo, vet < hi)
)

# Option D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
pharm = Int('pharm')
dist1 = If(pharm > rest1, pharm - rest1, rest1 - pharm)
dist2 = If(pharm > rest2, pharm - rest2, rest2 - pharm)
nearest_dist = If(dist1 < dist2, dist1, dist2)
opt_d_constr = (nearest_dist <= 3)

# Option E: The optometrist cannot be next to the shoe store.
shoe = Int('shoe')
opt_e_constr = Not(Or(opt - shoe == 1, shoe - opt == 1))

print("Counting solutions with original constraint...")
orig_count = count_solutions(original_constr)
print(f"Original: {orig_count}")

options = {
    "A": opt_a_constr,
    "B": opt_b_constr,
    "C": opt_c_constr,
    "D": opt_d_constr,
    "E": opt_e_constr
}

for letter, constr in options.items():
    c = count_solutions(constr)
    print(f"Option {letter}: {c}")
    if c == orig_count:
        print(f"  ** MATCH! **")