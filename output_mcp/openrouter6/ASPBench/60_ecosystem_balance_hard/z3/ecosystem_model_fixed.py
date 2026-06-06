from z3 import *

# Define species, zones, seasons indices
species_names = ["Grass", "Rabbits", "Foxes", "Hawks"]
zone_names = ["Forest", "Meadow"]
season_names = ["Summer", "Winter"]

# Create population variables: pop[species][zone][season]
# Each variable is an integer 0, 1, or 2
pop = {}
for s_idx, s_name in enumerate(species_names):
    for z_idx, z_name in enumerate(zone_names):
        for se_idx, se_name in enumerate(season_names):
            var_name = f"pop_{s_name}_{z_name}_{se_name}"
            pop[(s_idx, z_idx, se_idx)] = Int(var_name)

solver = Solver()

# Add domain constraints: 0 <= level <= 2
for var in pop.values():
    solver.add(var >= 0)
    solver.add(var <= 2)

# 1. Carrying Capacity constraints
# Grass has max level 1 in Forest
solver.add(pop[(0, 0, 0)] <= 1)  # Grass, Forest, Summer
solver.add(pop[(0, 0, 1)] <= 1)  # Grass, Forest, Winter

# Foxes have level 0 in Meadow
solver.add(pop[(2, 1, 0)] == 0)  # Foxes, Meadow, Summer
solver.add(pop[(2, 1, 1)] == 0)  # Foxes, Meadow, Winter

# Hawks have max level 1 everywhere
for z in range(2):
    for se in range(2):
        solver.add(pop[(3, z, se)] <= 1)  # Hawks

# 2. Winter Scarcity
# Grass max level 1 in Winter (already covered above, but explicit)
solver.add(pop[(0, 0, 1)] <= 1)  # Grass, Forest, Winter
solver.add(pop[(0, 1, 1)] <= 1)  # Grass, Meadow, Winter

# Rabbits cannot have level 2 in Winter
solver.add(pop[(1, 0, 1)] <= 1)  # Rabbits, Forest, Winter
solver.add(pop[(1, 1, 1)] <= 1)  # Rabbits, Meadow, Winter

# 3. Predator-Prey Balance for each location (zone, season)
for z in range(2):
    for se in range(2):
        # Rabbits <= Grass
        solver.add(pop[(1, z, se)] <= pop[(0, z, se)])
        # Foxes <= Rabbits
        solver.add(pop[(2, z, se)] <= pop[(1, z, se)])
        # Hawks <= Foxes
        solver.add(pop[(3, z, se)] <= pop[(2, z, se)])

# 4. Biodiversity: Total population for each species >= 1
for s in range(4):
    total = Sum([pop[(s, z, se)] for z in range(2) for se in range(2)])
    solver.add(total >= 1)

# 5. Hawk Population: Total exactly 2
hawk_total = Sum([pop[(3, z, se)] for z in range(2) for se in range(2)])
solver.add(hawk_total == 2)

# Check for solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nValid ecosystem solution found:")
    print("=" * 50)
    
    # Print population levels in a readable format
    for s_idx, s_name in enumerate(species_names):
        print(f"\n{s_name}:")
        for z_idx, z_name in enumerate(zone_names):
            for se_idx, se_name in enumerate(season_names):
                level = model[pop[(s_idx, z_idx, se_idx)]]
                print(f"  {z_name}, {se_name}: {level}")
    
    # Verify constraints
    print("\n" + "=" * 50)
    print("Constraint Verification:")
    
    # Check carrying capacity
    print("1. Carrying Capacity:")
    print(f"   Grass max 1 in Forest: {model[pop[(0, 0, 0)]]} <= 1, {model[pop[(0, 0, 1)]]} <= 1")
    print(f"   Foxes 0 in Meadow: {model[pop[(2, 1, 0)]]} == 0, {model[pop[(2, 1, 1)]]} == 0")
    print(f"   Hawks max 1 everywhere: all <= 1")
    
    # Check winter scarcity
    print("2. Winter Scarcity:")
    print(f"   Grass max 1 in Winter: {model[pop[(0, 0, 1)]]} <= 1, {model[pop[(0, 1, 1)]]} <= 1")
    print(f"   Rabbits no high in Winter: {model[pop[(1, 0, 1)]]} <= 1, {model[pop[(1, 1, 1)]]} <= 1")
    
    # Check predator-prey balance
    print("3. Predator-Prey Balance (all locations):")
    for z in range(2):
        for se in range(2):
            r = model[pop[(1, z, se)]]
            g = model[pop[(0, z, se)]]
            f = model[pop[(2, z, se)]]
            h = model[pop[(3, z, se)]]
            print(f"   {zone_names[z]}, {season_names[se]}: Rabbits({r}) <= Grass({g}), Foxes({f}) <= Rabbits({r}), Hawks({h}) <= Foxes({f})")
    
    # Check biodiversity
    print("4. Biodiversity (total per species >= 1):")
    for s_idx, s_name in enumerate(species_names):
        total = sum(model[pop[(s_idx, z, se)]] for z in range(2) for se in range(2))
        print(f"   {s_name}: {total} >= 1")
    
    # Check hawk total
    hawk_total_val = sum(model[pop[(3, z, se)]] for z in range(2) for se in range(2))
    print(f"5. Hawk total: {hawk_total_val} == 2")
    
    print("\n" + "=" * 50)
    print("balance_achieved: True")
    
    # Output in required format for field descriptions
    print("\n" + "=" * 50)
    print("Field Descriptions Output:")
    print("population_levels: [")
    for s_idx, s_name in enumerate(species_names):
        for z_idx, z_name in enumerate(zone_names):
            for se_idx, se_name in enumerate(season_names):
                level = model[pop[(s_idx, z_idx, se_idx)]]
                print(f'  {{"species": "{s_name}", "zone": "{z_name}", "season": "{se_name}", "level": {level}}},')
    print("]")
    
    print("\npredator_prey_relationships: [")
    print('  {"predator": "Rabbits", "prey": "Grass"},')
    print('  {"predator": "Foxes", "prey": "Rabbits"},')
    print('  {"predator": "Hawks", "prey": "Foxes"}')
    print("]")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid ecosystem solution exists with given constraints")
else:
    print("STATUS: unknown")
    print("Solver could not determine satisfiability")