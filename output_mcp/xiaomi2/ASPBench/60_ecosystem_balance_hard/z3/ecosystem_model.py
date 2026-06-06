from z3 import *

solver = Solver()

# Define entities
species = ['Grass', 'Rabbits', 'Foxes', 'Hawks']
zones = ['Forest', 'Meadow']
seasons = ['Summer', 'Winter']

# Create population level variables: pop[species][zone][season]
pop = {}
for s in species:
    for z in zones:
        for se in seasons:
            pop[(s, z, se)] = Int(f'pop_{s}_{z}_{se}')

# Domain constraints: each level is 0, 1, or 2
for key in pop:
    solver.add(pop[key] >= 0, pop[key] <= 2)

# Constraint 1: Carrying Capacity
for z in zones:
    for se in seasons:
        # Grass max level 1 in Forest
        solver.add(pop[('Grass', 'Forest', se)] <= 1)
        # Foxes level 0 in Meadow
        solver.add(pop[('Foxes', 'Meadow', se)] == 0)
        # Hawks max level 1 everywhere
        solver.add(pop[('Hawks', z, se)] <= 1)

# Constraint 2: Winter Scarcity
for z in zones:
    # Grass max level 1 in Winter
    solver.add(pop[('Grass', z, 'Winter')] <= 1)
    # Rabbits cannot have level 2 in Winter
    solver.add(pop[('Rabbits', z, 'Winter')] <= 1)

# Constraint 3: Predator-Prey Balance
# In any given (zone, season):
#   level(Rabbits) <= level(Grass)
#   level(Foxes) <= level(Rabbits)
#   level(Hawks) <= level(Foxes)
for z in zones:
    for se in seasons:
        solver.add(pop[('Rabbits', z, se)] <= pop[('Grass', z, se)])
        solver.add(pop[('Foxes', z, se)] <= pop[('Rabbits', z, se)])
        solver.add(pop[('Hawks', z, se)] <= pop[('Foxes', z, se)])

# Constraint 4: Biodiversity - total population for each species >= 1
for s in species:
    total = Sum([pop[(s, z, se)] for z in zones for se in seasons])
    solver.add(total >= 1)

# Constraint 5: Hawk total population exactly 2
hawk_total = Sum([pop[('Hawks', z, se)] for z in zones for se in seasons])
solver.add(hawk_total == 2)

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("balance_achieved: True")
    print()
    print("population_levels:")
    for s in species:
        for z in zones:
            for se in seasons:
                val = m.evaluate(pop[(s, z, se)], model_completion=True)
                print(f"  species={s}, zone={z}, season={se}, level={val}")
    print()
    print("predator_prey_relationships:")
    print("  Rabbits -> Grass (Rabbits eat Grass)")
    print("  Foxes -> Rabbits (Foxes eat Rabbits)")
    print("  Hawks -> Foxes (Hawks eat Foxes)")
    print()
    # Print summary totals
    print("Species totals:")
    for s in species:
        total = sum(int(str(m.evaluate(pop[(s, z, se)], model_completion=True))) for z in zones for se in seasons)
        print(f"  {s}: {total}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")