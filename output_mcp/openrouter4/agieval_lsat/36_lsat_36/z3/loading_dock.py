from z3 import *

solver = Solver()

# Each cargo type is assigned a bay number from 1 to 6
fuel, grain, livestock, machinery, produce, textiles = Ints('fuel grain livestock machinery produce textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Domain: each cargo is in a bay 1-6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# Each bay holds a different cargo
solver.add(Distinct(cargos))

# Constraint 1: grain > livestock
solver.add(grain > livestock)

# Constraint 2: livestock > textiles
solver.add(livestock > textiles)

# Constraint 3: produce > fuel
solver.add(produce > fuel)

# Constraint 4: textiles is next to produce (|textiles - produce| == 1)
solver.add(Or(textiles + 1 == produce, produce + 1 == textiles))

# Given: bay 4 is holding produce
solver.add(produce == 4)

# Now let's enumerate all solutions to see which bays have fixed cargo types
solutions = []
decision_vars = cargos

while solver.check() == sat:
    m = solver.model()
    sol = {v: m.eval(v, model_completion=True) for v in decision_vars}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}:")
    for v in decision_vars:
        print(f"  {v}: {sol[v]}")
    # Show what's in each bay
    bay_to_cargo = {}
    for v in decision_vars:
        bay = int(str(sol[v]))
        bay_to_cargo[bay] = str(v)
    for bay in range(1, 7):
        print(f"  Bay {bay}: {bay_to_cargo.get(bay, '?')}")
    print()

# Now determine for each bay how many different cargo types appear across all solutions
if solutions:
    # For each bay, check what cargo types appear there across all solutions
    bay_assignments = {bay: set() for bay in range(1, 7)}
    for sol in solutions:
        for v in decision_vars:
            bay = int(str(sol[v]))
            bay_assignments[bay].add(str(v))
    
    print("Bay assignments across all solutions:")
    fixed_count = 0
    for bay in range(1, 7):
        types = bay_assignments[bay]
        if len(types) == 1:
            fixed_count += 1
            print(f"  Bay {bay}: FIXED -> {list(types)[0]}")
        else:
            print(f"  Bay {bay}: Multiple possibilities: {types}")
    
    print(f"\nNumber of bays with completely determined cargo: {fixed_count}")
    
    # Now check each answer choice
    # (A) two -> fixed_count == 2
    # (B) three -> fixed_count == 3
    # (C) four -> fixed_count == 4
    # (D) five -> fixed_count == 5
    # (E) six -> fixed_count == 6
    
    found_options = []
    
    # Option A: exactly two bays are determined
    opt_a = (fixed_count == 2)
    # Option B: exactly three bays are determined
    opt_b = (fixed_count == 3)
    # Option C: exactly four bays are determined
    opt_c = (fixed_count == 4)
    # Option D: exactly five bays are determined
    opt_d = (fixed_count == 5)
    # Option E: exactly six bays are determined
    opt_e = (fixed_count == 6)
    
    # We need to use the skeleton pattern
    # But here fixed_count is already a concrete integer, so we can just compare directly
    for letter, val in [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
        if fixed_count == val:
            found_options.append(letter)
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")