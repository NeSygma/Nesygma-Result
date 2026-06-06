from z3 import *

solver = Solver()

# Bays 1..6
# We'll assign each cargo type to a bay number (1-6)
fuel, grain, livestock, machinery, produce, textiles = Ints('fuel grain livestock machinery produce textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Each cargo is assigned to a distinct bay 1..6
for c in cargos:
    solver.add(c >= 1, c <= 6)
solver.add(Distinct(cargos))

# Constraints:
# 1. grain > livestock
solver.add(grain > livestock)

# 2. livestock > textiles
solver.add(livestock > textiles)

# 3. produce > fuel
solver.add(produce > fuel)

# 4. textiles is next to produce (|textiles - produce| == 1)
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Additional condition: exactly one bay between machinery and grain
# |machinery - grain| == 2
solver.add(Or(machinery == grain + 2, machinery == grain - 2))

# Now we need to determine: for exactly how many of the six bays is the type of cargo completely determined?
# We'll enumerate all solutions and see which positions are fixed.

# First, let's find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {c: m.eval(c).as_long() for c in cargos}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([c != m.eval(c).as_long() for c in cargos]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: fuel={sol[fuel]}, grain={sol[grain]}, livestock={sol[livestock]}, machinery={sol[machinery]}, produce={sol[produce]}, textiles={sol[textiles]}")

# Now determine which bay positions have fixed cargo types across all solutions
if len(solutions) > 0:
    fixed_count = 0
    for bay in range(1, 7):
        cargo_types_at_bay = set()
        for sol in solutions:
            for cargo_name, cargo_val in sol.items():
                if cargo_val == bay:
                    cargo_types_at_bay.add(cargo_name)
        if len(cargo_types_at_bay) == 1:
            fixed_count += 1
            print(f"Bay {bay} is fixed: {list(cargo_types_at_bay)[0]}")
        else:
            print(f"Bay {bay} is NOT fixed: {cargo_types_at_bay}")
    
    print(f"Number of fixed bays: {fixed_count}")
    
    # Now evaluate the answer choices
    # A: two, B: three, C: four, D: five, E: six
    opt_a = (fixed_count == 2)
    opt_b = (fixed_count == 3)
    opt_c = (fixed_count == 4)
    opt_d = (fixed_count == 5)
    opt_e = (fixed_count == 6)
    
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
else:
    print("STATUS: unsat")
    print("Refine: No solutions found")