from z3 import *

# Define entities
species = ['Grass', 'Rabbits', 'Foxes', 'Hawks']
zones = ['Forest', 'Meadow']
seasons = ['Summer', 'Winter']

# Create variables
pop = {}
for s in species:
    for z in zones:
        for se in seasons:
            var_name = f"{s}_{z}_{se}"
            pop[(s,z,se)] = Int(var_name)
            # Domain 0-2
            solver = Solver()
            solver.add(pop[(s,z,se)] >= 0, pop[(s,z,se)] <= 2)

# Now create a new solver and add all constraints
solver = Solver()
# Domain constraints
for var in pop.values():
    solver.add(var >= 0, var <= 2)

# Carrying capacity constraints
# Grass max 1 in Forest
for se in seasons:
    solver.add(pop[('Grass','Forest',se)] <= 1)
# Foxes level 0 in Meadow
for se in seasons:
    solver.add(pop[('Foxes','Meadow',se)] == 0)
# Hawks max 1 everywhere
for s in species:
    if s == 'Hawks':
        for z in zones:
            for se in seasons:
                solver.add(pop[(s,z,se)] <= 1)

# Winter scarcity
# Grass max 1 in Winter
for z in zones:
    solver.add(pop[('Grass',z,'Winter')] <= 1)
# Rabbits cannot have high (2) in Winter
for z in zones:
    solver.add(pop[('Rabbits',z,'Winter')] <= 1)

# Predator-prey balance per location
for z in zones:
    for se in seasons:
        # Rabbits <= Grass
        solver.add(pop[('Rabbits',z,se)] <= pop[('Grass',z,se)])
        # Foxes <= Rabbits
        solver.add(pop[('Foxes',z,se)] <= pop[('Rabbits',z,se)])
        # Hawks <= Foxes
        solver.add(pop[('Hawks',z,se)] <= pop[('Foxes',z,se)])

# Biodiversity: each species total >= 1
for s in species:
    total = Sum([pop[(s,z,se)] for z in zones for se in seasons])
    solver.add(total >= 1)

# Hawk total exactly 2
hawk_total = Sum([pop[('Hawks',z,se)] for z in zones for se in seasons])
solver.add(hawk_total == 2)

# Check
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print each variable
    for s in species:
        for z in zones:
            for se in seasons:
                var = pop[(s,z,se)]
                val = m[var]
                print(f"{s}_{z}_{se} = {val}")
    # Balance achieved is true if all constraints satisfied
    print("balance_achieved: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")