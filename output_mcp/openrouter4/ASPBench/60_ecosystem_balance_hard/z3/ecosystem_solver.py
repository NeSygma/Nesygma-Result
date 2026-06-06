from z3 import *

# Define domains
species = ["Grass", "Rabbits", "Foxes", "Hawks"]
zones = ["Forest", "Meadow"]
seasons = ["Summer", "Winter"]

# Map to indices
species_idx = {s: i for i, s in enumerate(species)}
zones_idx = {z: i for i, z in enumerate(zones)}
seasons_idx = {sz: i for i, sz in enumerate(seasons)}

# Create solver
solver = Solver()

# Decision variables: P[species_idx][zone_idx][season_idx] ∈ {0, 1, 2}
P = [[[Int(f"P_{s}_{z}_{sz}") for sz in range(len(seasons))] for z in range(len(zones))] for s in range(len(species))]

# Domain constraints: each level is 0, 1, or 2
for s in range(len(species)):
    for z in range(len(zones)):
        for sz in range(len(seasons)):
            solver.add(And(P[s][z][sz] >= 0, P[s][z][sz] <= 2))

# --- Constraint 1: Carrying Capacity ---

# Grass max level 1 in Forest (both seasons)
g_idx = species_idx["Grass"]
f_idx = zones_idx["Forest"]
for sz in range(len(seasons)):
    solver.add(P[g_idx][f_idx][sz] <= 1)

# Foxes level 0 in Meadow (both seasons)
fx_idx = species_idx["Foxes"]
m_idx = zones_idx["Meadow"]
for sz in range(len(seasons)):
    solver.add(P[fx_idx][m_idx][sz] == 0)

# Hawks max level 1 everywhere
h_idx = species_idx["Hawks"]
for z in range(len(zones)):
    for sz in range(len(seasons)):
        solver.add(P[h_idx][z][sz] <= 1)

# --- Constraint 2: Winter Scarcity ---

w_idx = seasons_idx["Winter"]

# Grass max level 1 in Winter (both zones)
for z in range(len(zones)):
    solver.add(P[g_idx][z][w_idx] <= 1)

# Rabbits cannot have high (2) in Winter
r_idx = species_idx["Rabbits"]
for z in range(len(zones)):
    solver.add(P[r_idx][z][w_idx] <= 1)

# --- Constraint 3: Predator-Prey Balance ---
# In any given location (zone, season):
# level(Rabbits) <= level(Grass)
# level(Foxes) <= level(Rabbits)
# level(Hawks) <= level(Foxes)

for z in range(len(zones)):
    for sz in range(len(seasons)):
        solver.add(P[r_idx][z][sz] <= P[g_idx][z][sz])   # Rabbits <= Grass
        solver.add(P[fx_idx][z][sz] <= P[r_idx][z][sz])  # Foxes <= Rabbits
        solver.add(P[h_idx][z][sz] <= P[fx_idx][z][sz])  # Hawks <= Foxes

# --- Constraint 4: Biodiversity ---
# Total population for each species >= 1
for s in range(len(species)):
    total_s = Sum([P[s][z][sz] for z in range(len(zones)) for sz in range(len(seasons))])
    solver.add(total_s >= 1)

# --- Constraint 5: Hawk Population total == 2 ---
total_hawks = Sum([P[h_idx][z][sz] for z in range(len(zones)) for sz in range(len(seasons))])
solver.add(total_hawks == 2)

# --- Solve ---
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Valid ecosystem configuration found:")
    print()
    print("population_levels = [")
    for s in range(len(species)):
        for z in range(len(zones)):
            for sz in range(len(seasons)):
                val = model.eval(P[s][z][sz]).as_long()
                print(f"  {{ species: {species[s]}, zone: {zones[z]}, season: {seasons[sz]}, level: {val} }},")
    print("]")
    print()
    # Verify constraints
    print("--- Verification ---")
    # Check predator-prey chain
    for z in range(len(zones)):
        for sz in range(len(seasons)):
            gv = model.eval(P[g_idx][z][sz]).as_long()
            rv = model.eval(P[r_idx][z][sz]).as_long()
            fxv = model.eval(P[fx_idx][z][sz]).as_long()
            hv = model.eval(P[h_idx][z][sz]).as_long()
            print(f"  {zones[z]}/{seasons[sz]}: G={gv}, R={rv}, Fx={fxv}, H={hv}  ", end="")
            ok = (rv <= gv) and (fxv <= rv) and (hv <= fxv)
            print("OK" if ok else "FAIL")
    
    # Check totals
    for s in range(len(species)):
        total = sum(model.eval(P[s][z][sz]).as_long() for z in range(len(zones)) for sz in range(len(seasons)))
        print(f"  Total {species[s]}: {total} {'OK' if total >= 1 else 'FAIL'}")
    total_h = sum(model.eval(P[h_idx][z][sz]).as_long() for z in range(len(zones)) for sz in range(len(seasons)))
    print(f"  Total Hawks: {total_h} {'OK' if total_h == 2 else 'FAIL'}")
    print("balance_achieved: true")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")