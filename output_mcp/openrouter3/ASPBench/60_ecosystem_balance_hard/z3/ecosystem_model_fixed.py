from z3 import *

# Define species, zones, seasons
species = ['Grass', 'Rabbits', 'Foxes', 'Hawks']
zones = ['Forest', 'Meadow']
seasons = ['Summer', 'Winter']

# Create symbolic variables for population levels
# Format: pop[species][zone][season]
pop = {}
for s in species:
    pop[s] = {}
    for z in zones:
        pop[s][z] = {}
        for sea in seasons:
            pop[s][z][sea] = Int(f'pop_{s}_{z}_{sea}')

solver = Solver()

# Add domain constraints: population levels must be 0, 1, or 2
for s in species:
    for z in zones:
        for sea in seasons:
            solver.add(Or(pop[s][z][sea] == 0,
                         pop[s][z][sea] == 1,
                         pop[s][z][sea] == 2))

# 1. Carrying Capacity Constraints
# Grass has a max level of 1 in the Forest
solver.add(pop['Grass']['Forest']['Summer'] <= 1)
solver.add(pop['Grass']['Forest']['Winter'] <= 1)

# Foxes have a level of 0 in the Meadow
solver.add(pop['Foxes']['Meadow']['Summer'] == 0)
solver.add(pop['Foxes']['Meadow']['Winter'] == 0)

# Hawks have a max level of 1 everywhere
for z in zones:
    for sea in seasons:
        solver.add(pop['Hawks'][z][sea] <= 1)

# 2. Winter Scarcity Constraints
# Grass has a max level of 1 in Winter
for z in zones:
    solver.add(pop['Grass'][z]['Winter'] <= 1)

# Rabbits cannot have a high (2) level in Winter
for z in zones:
    solver.add(pop['Rabbits'][z]['Winter'] <= 1)

# 3. Predator-Prey Balance Constraints
# In any given location (zone, season), predator level ≤ prey level
for z in zones:
    for sea in seasons:
        # Rabbits ≤ Grass
        solver.add(pop['Rabbits'][z][sea] <= pop['Grass'][z][sea])
        # Foxes ≤ Rabbits
        solver.add(pop['Foxes'][z][sea] <= pop['Rabbits'][z][sea])
        # Hawks ≤ Foxes
        solver.add(pop['Hawks'][z][sea] <= pop['Foxes'][z][sea])

# 4. Biodiversity: Each species total population ≥ 1
for s in species:
    total = Sum([pop[s][z][sea] for z in zones for sea in seasons])
    solver.add(total >= 1)

# 5. Hawk Population: Total must be exactly 2
hawk_total = Sum([pop['Hawks'][z][sea] for z in zones for sea in seasons])
solver.add(hawk_total == 2)

# Check for solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Ecosystem solution found!")
    print("\nPopulation levels by species, zone, and season:")
    
    # Print all population levels
    for s in species:
        print(f"\n{s}:")
        for z in zones:
            for sea in seasons:
                level = m.eval(pop[s][z][sea])
                print(f"  {z} ({sea}): {level}")
    
    # Calculate totals for verification
    print("\nVerification:")
    for s in species:
        total = sum([int(m.eval(pop[s][z][sea])) for z in zones for sea in seasons])
        print(f"  {s} total: {total}")
    
    hawk_total_val = sum([int(m.eval(pop['Hawks'][z][sea])) for z in zones for sea in seasons])
    print(f"  Hawks total: {hawk_total_val} (should be 2)")
    
    # Check predator-prey balance
    print("\nPredator-prey balance check:")
    balance_achieved = True
    for z in zones:
        for sea in seasons:
            grass = int(m.eval(pop['Grass'][z][sea]))
            rabbits = int(m.eval(pop['Rabbits'][z][sea]))
            foxes = int(m.eval(pop['Foxes'][z][sea]))
            hawks = int(m.eval(pop['Hawks'][z][sea]))
            print(f"  {z} ({sea}): Grass={grass}, Rabbits={rabbits}, Foxes={foxes}, Hawks={hawks}")
            if rabbits <= grass and foxes <= rabbits and hawks <= foxes:
                print(f"    ✓ Balance maintained")
            else:
                print(f"    ✗ Balance violated")
                balance_achieved = False
    
    print(f"\nbalance_achieved: {balance_achieved}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")