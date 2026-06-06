from z3 import *

# Declare integer variables for each cargo
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

# Domain constraints: 1..6
solver = Solver()
solver.add(And(fuel >= 1, fuel <= 6))
solver.add(And(grain >= 1, grain <= 6))
solver.add(And(livestock >= 1, livestock <= 6))
solver.add(And(machinery >= 1, machinery <= 6))
solver.add(And(produce >= 1, produce <= 6))
solver.add(And(textiles >= 1, textiles <= 6))

# AllDifferent
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Base constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(textiles == produce + 1, textiles + 1 == produce))

# Function to check adjacency
def adjacent(x, y):
    return Or(x == y + 1, x + 1 == y)

# Options as Z3 expressions
opt_a = adjacent(fuel, machinery)
opt_b = adjacent(grain, machinery)
opt_c = adjacent(livestock, fuel)
opt_d = adjacent(produce, livestock)
opt_e = adjacent(textiles, fuel)

# Enumerate all models
solutions = []
while solver.check() == sat:
    m = solver.model()
    # Extract values
    sol = {var: m[var].as_long() for var in [fuel, grain, livestock, machinery, produce, textiles]}
    solutions.append(sol)
    # Block this exact model
    solver.add(Or([var != m[var] for var in [fuel, grain, livestock, machinery, produce, textiles]]))

print(f"Found {len(solutions)} solutions.")
# Analyze which options appear in any solution
option_possible = {letter: False for letter in ['A','B','C','D','E']}
for sol in solutions:
    # Check each option
    if adjacent(sol[fuel], sol[machinery]):
        option_possible['A'] = True
    if adjacent(sol[grain], sol[machinery]):
        option_possible['B'] = True
    if adjacent(sol[livestock], sol[sol['fuel']] if 'fuel' in sol else None):
        pass