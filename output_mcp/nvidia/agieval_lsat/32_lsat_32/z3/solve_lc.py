from z3 import *

# Declare integer variables for each cargo type
grain = Int('grain')
livestock = Int('livestock')
textiles = Int('textiles')
produce = Int('produce')
fuel = Int('fuel')
machinery = Int('machinery')

solver = Solver()

# Domain constraints 1..6
for var in [grain, livestock, textiles, produce, fuel, machinery]:
    solver.add(var >= 1, var <= 6)

# AllDifferent
solver.add(Distinct([grain, livestock, textiles, produce, fuel, machinery]))

# Order constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)

# Textiles adjacent to produce
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Exactly one bay between machinery and grain => distance 2
solver.add(Or(machinery == grain + 2, machinery == grain - 2))

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    # Build mapping cargo -> bay number
    sol_map = {
        'grain': m[grain].as_long(),
        'livestock': m[livestock].as_long(),
        'textiles': m[textiles].as_long(),
        'produce': m[produce].as_long(),
        'fuel': m[fuel].as_long(),
        'machinery': m[machinery].as_long()
    }
    solutions.append(sol_map)
    # Block this solution
    block = Or([var != m[var] for var in [grain, livestock, textiles, produce, fuel, machinery]])
    solver.add(block)

len(solutions)