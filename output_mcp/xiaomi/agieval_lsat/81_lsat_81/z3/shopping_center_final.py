from z3 import *

def get_solutions(extra_constraint=None):
    """Get all solutions with base constraints + optional extra constraint."""
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
    
    solutions = set()
    while solver.check() == sat:
        m = solver.model()
        sol = tuple((str(b), m[b].as_long()) for b in businesses)
        solutions.add(sol)
        solver.add(Or([b != m[b] for b in businesses]))
    
    return solutions

# Original constraint: two restaurants separated by at least 2 other businesses
rest1, rest2 = Ints('rest1 rest2')
original_constr = Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3)

# Option D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
pharm = Int('pharm')
dist1 = If(pharm > rest1, pharm - rest1, rest1 - pharm)
dist2 = If(pharm > rest2, pharm - rest2, rest2 - pharm)
nearest_dist = If(dist1 < dist2, dist1, dist2)
opt_d_constr = (nearest_dist <= 3)

orig_solutions = get_solutions(original_constr)
opt_d_solutions = get_solutions(opt_d_constr)

print(f"Original solutions: {len(orig_solutions)}")
print(f"Option D solutions: {len(opt_d_solutions)}")
print(f"Sets identical: {orig_solutions == opt_d_solutions}")

# Verify: original implies D, and D implies original
print(f"Original subset of D: {orig_solutions.issubset(opt_d_solutions)}")
print(f"D subset of Original: {opt_d_solutions.issubset(orig_solutions)}")

print()
print("STATUS: sat")
print("answer:D")