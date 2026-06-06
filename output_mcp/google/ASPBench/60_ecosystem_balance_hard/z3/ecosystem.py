from z3 import *

# Species: 0: Grass, 1: Rabbits, 2: Foxes, 3: Hawks
# Zones: 0: Forest, 1: Meadow
# Seasons: 0: Summer, 1: Winter

species = ['Grass', 'Rabbits', 'Foxes', 'Hawks']
zones = ['Forest', 'Meadow']
seasons = ['Summer', 'Winter']

# Create variables for each state
# pop[s][z][se]
pop = {}
for s in range(4):
    for z in range(2):
        for se in range(2):
            pop[(s, z, se)] = Int(f'pop_{species[s]}_{zones[z]}_{seasons[se]}')

solver = Solver()

# Domain constraints
for s in range(4):
    for z in range(2):
        for se in range(2):
            solver.add(pop[(s, z, se)] >= 0, pop[(s, z, se)] <= 2)

# C1: Carrying Capacity
# Grass has a max level of 1 in the Forest
for se in range(2):
    solver.add(pop[(0, 0, se)] <= 1)

# Foxes have a level of 0 in the Meadow
for se in range(2):
    solver.add(pop[(2, 1, se)] == 0)

# Hawks have a max level of 1 everywhere
for z in range(2):
    for se in range(2):
        solver.add(pop[(3, z, se)] <= 1)

# C2: Winter Scarcity
# Grass has a max level of 1 in Winter
for z in range(2):
    solver.add(pop[(0, z, 1)] <= 1)

# Rabbits cannot have a high (2) level in Winter
for z in range(2):
    solver.add(pop[(1, z, 1)] <= 1)

# C3: Predator-Prey Balance
for z in range(2):
    for se in range(2):
        solver.add(pop[(1, z, se)] <= pop[(0, z, se)]) # Rabbits <= Grass
        solver.add(pop[(2, z, se)] <= pop[(1, z, se)]) # Foxes <= Rabbits
        solver.add(pop[(3, z, se)] <= pop[(2, z, se)]) # Hawks <= Foxes

# C4: Biodiversity (Total population >= 1 for each species)
for s in range(4):
    total_s = Sum([pop[(s, z, se)] for z in range(2) for se in range(2)])
    solver.add(total_s >= 1)

# C5: Hawk Population (Total population level for Hawks must be exactly 2)
total_hawks = Sum([pop[(3, z, se)] for z in range(2) for se in range(2)])
solver.add(total_hawks == 2)

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for s in range(4):
        for z in range(2):
            for se in range(2):
                print(f"{species[s]} in {zones[z]} ({seasons[se]}): {m[pop[(s, z, se)]]}")
else:
    print("STATUS: unsat")