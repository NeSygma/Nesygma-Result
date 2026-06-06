from z3 import *

# Species: Grass=0, Rabbits=1, Foxes=2, Hawks=3
# Zones: Forest=0, Meadow=1
# Seasons: Summer=0, Winter=1

species_names = ["Grass", "Rabbits", "Foxes", "Hawks"]
zone_names = ["Forest", "Meadow"]
season_names = ["Summer", "Winter"]

# Create 16 variables: pop[species][zone][season] each in {0,1,2}
pop = [[[Int(f"pop_{s}_{z}_{se}") for se in range(2)] for z in range(2)] for s in range(4)]

solver = Solver()

# Domain: each population level is 0, 1, or 2
for s in range(4):
    for z in range(2):
        for se in range(2):
            solver.add(pop[s][z][se] >= 0)
            solver.add(pop[s][z][se] <= 2)

# Constraint 1: Carrying Capacity
# Grass (s=0) has max level 1 in Forest (z=0)
for se in range(2):
    solver.add(pop[0][0][se] <= 1)

# Foxes (s=2) have level 0 in Meadow (z=1)
for se in range(2):
    solver.add(pop[2][1][se] == 0)

# Hawks (s=3) have max level 1 everywhere
for z in range(2):
    for se in range(2):
        solver.add(pop[3][z][se] <= 1)

# Constraint 2: Winter Scarcity
# Grass has max level 1 in Winter (se=1)
for z in range(2):
    solver.add(pop[0][z][1] <= 1)

# Rabbits (s=1) cannot have high (2) level in Winter
for z in range(2):
    solver.add(pop[1][z][1] <= 1)

# Constraint 3: Predator-Prey Balance
# In any given location (zone, season):
# level(Rabbits) <= level(Grass)
# level(Foxes) <= level(Rabbits)
# level(Hawks) <= level(Foxes)
for z in range(2):
    for se in range(2):
        solver.add(pop[1][z][se] <= pop[0][z][se])  # Rabbits <= Grass
        solver.add(pop[2][z][se] <= pop[1][z][se])  # Foxes <= Rabbits
        solver.add(pop[3][z][se] <= pop[2][z][se])  # Hawks <= Foxes

# Constraint 4: Biodiversity - total population for each species >= 1
for s in range(4):
    total_species = Sum([pop[s][z][se] for z in range(2) for se in range(2)])
    solver.add(total_species >= 1)

# Constraint 5: Hawk total population exactly 2
total_hawks = Sum([pop[3][z][se] for z in range(2) for se in range(2)])
solver.add(total_hawks == 2)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for s in range(4):
        for z in range(2):
            for se in range(2):
                val = m.eval(pop[s][z][se]).as_long()
                print(f"{species_names[s]}_{zone_names[z]}_{season_names[se]} = {val}")
    # Verify constraints
    print("\n--- Verification ---")
    for s in range(4):
        total = sum(m.eval(pop[s][z][se]).as_long() for z in range(2) for se in range(2))
        print(f"Total {species_names[s]}: {total}")
    print("balance_achieved: true")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")