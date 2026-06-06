from z3 import *

# Define indices
species = ['Grass', 'Rabbits', 'Foxes', 'Hawks']
zones = ['Forest', 'Meadow']
seasons = ['Summer', 'Winter']

# Create 3D list of Int variables
pop = [[[Int(f"pop_{sp}_{zn}_{sn}") for sn in range(2)] for zn in range(2)] for sp in range(4)]

solver = Solver()

# Domain constraints 0..2
for sp in range(4):
    for zn in range(2):
        for sn in range(2):
            solver.add(pop[sp][zn][sn] >= 0, pop[sp][zn][sn] <= 2)

# 1. Carrying Capacity
# Grass max 1 in Forest (zone 0) any season
for sn in range(2):
    solver.add(pop[0][0][sn] <= 1)
# Foxes level 0 in Meadow (zone 1) any season
for sn in range(2):
    solver.add(pop[2][1][sn] == 0)
# Hawks max 1 everywhere
for sp in [3]:
    for zn in range(2):
        for sn in range(2):
            solver.add(pop[sp][zn][sn] <= 1)

# 2. Winter Scarcity
# Grass max 1 in Winter (season 1) any zone
for zn in range(2):
    solver.add(pop[0][zn][1] <= 1)
# Rabbits cannot be high (2) in Winter
for zn in range(2):
    solver.add(pop[1][zn][1] != 2)

# 3. Predator-Prey Balance for each zone, season
for zn in range(2):
    for sn in range(2):
        # Rabbits <= Grass
        solver.add(pop[1][zn][sn] <= pop[0][zn][sn])
        # Foxes <= Rabbits
        solver.add(pop[2][zn][sn] <= pop[1][zn][sn])
        # Hawks <= Foxes
        solver.add(pop[3][zn][sn] <= pop[2][zn][sn])

# 4. Biodiversity: each species total >=1
for sp in range(4):
    total = Sum([pop[sp][zn][sn] for zn in range(2) for sn in range(2)])
    solver.add(total >= 1)

# 5. Hawk total exactly 2
hawk_total = Sum([pop[3][zn][sn] for zn in range(2) for sn in range(2)])
solver.add(hawk_total == 2)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for sp_idx, sp_name in enumerate(species):
        for zn_idx, zn_name in enumerate(zones):
            for sn_idx, sn_name in enumerate(seasons):
                val = m.eval(pop[sp_idx][zn_idx][sn_idx], model_completion=True)
                print(f"{sp_name}_{zn_name}_{sn_name} = {val}")
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")