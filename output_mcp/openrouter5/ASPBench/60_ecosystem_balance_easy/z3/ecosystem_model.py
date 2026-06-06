from z3 import *

solver = Solver()

# Species populations (non-negative integers)
Grass = Int('Grass')
Rabbits = Int('Rabbits')
Foxes = Int('Foxes')
Hawks = Int('Hawks')

# Carrying capacities
Grass_max = 100
Rabbits_max = 30
Foxes_max = 10
Hawks_max = 5

# Constraint 1: Non-negative populations
solver.add(Grass >= 0)
solver.add(Rabbits >= 0)
solver.add(Foxes >= 0)
solver.add(Hawks >= 0)

# Constraint 2: Populations cannot exceed carrying capacity
solver.add(Grass <= Grass_max)
solver.add(Rabbits <= Rabbits_max)
solver.add(Foxes <= Foxes_max)
solver.add(Hawks <= Hawks_max)

# Constraint 3: Herbivore sustainability (Rabbits ≤ 0.5 × Grass)
# Using integer arithmetic: 2 * Rabbits <= Grass
solver.add(2 * Rabbits <= Grass)

# Constraint 4: Predator sustainability
# Foxes ≤ 0.3 × Rabbits => 10 * Foxes <= 3 * Rabbits
solver.add(10 * Foxes <= 3 * Rabbits)
# Hawks eat Rabbits and Foxes. We need a combined prey constraint.
# Hawks eat both Rabbits and Foxes. Let's model a combined constraint.
# A reasonable approach: Hawks <= 0.2 * (Rabbits + Foxes) or similar.
# Since Hawks eat both, we can say Hawks <= 0.2 * (Rabbits + Foxes)
# => 5 * Hawks <= Rabbits + Foxes
solver.add(5 * Hawks <= Rabbits + Foxes)

# Constraint 5: No species can go extinct (all populations > 0)
solver.add(Grass > 0)
solver.add(Rabbits > 0)
solver.add(Foxes > 0)
solver.add(Hawks > 0)

# Constraint 6: Food web relationships with consumption rates between 0.1 and 0.5
# Rabbits eat Grass: consumption rate = Rabbits / Grass should be between 0.1 and 0.5
# 0.1 <= Rabbits/Grass <= 0.5
# => Grass <= 10 * Rabbits and 2 * Rabbits <= Grass (already have 2*Rabbits <= Grass)
solver.add(Grass <= 10 * Rabbits)

# Foxes eat Rabbits: 0.1 <= Foxes/Rabbits <= 0.5
# => 10 * Foxes >= Rabbits and 2 * Foxes <= Rabbits
solver.add(10 * Foxes >= Rabbits)
solver.add(2 * Foxes <= Rabbits)

# Hawks eat Rabbits and Foxes: consumption rates between 0.1 and 0.5
# For Hawks eating Rabbits: 0.1 <= Hawks/Rabbits <= 0.5
# => 10 * Hawks >= Rabbits and 2 * Hawks <= Rabbits
# But Hawks also eat Foxes, so let's use a combined prey base.
# Let's say Hawks consume from the combined pool of Rabbits+Foxes
# 0.1 <= Hawks / (Rabbits + Foxes) <= 0.5
# => 10 * Hawks >= Rabbits + Foxes and 2 * Hawks <= Rabbits + Foxes
solver.add(10 * Hawks >= Rabbits + Foxes)
solver.add(2 * Hawks <= Rabbits + Foxes)

# Also need to ensure the food web relationships exist (predator eats prey)
# This is already encoded in the consumption rate constraints above.

# Let's also add a biodiversity index constraint (implicitly through having all species > 0)
# and stability score.

# Compute biodiversity_index = (number of species present) / 4 = 1.0 (all present)
# Compute stability_score based on how balanced the populations are.
# We'll just check satisfiability and report the model.

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Stable Populations:")
    print(f"  Grass = {m[Grass]}")
    print(f"  Rabbits = {m[Rabbits]}")
    print(f"  Foxes = {m[Foxes]}")
    print(f"  Hawks = {m[Hawks]}")
    
    # Compute derived values
    g = m[Grass].as_long()
    r = m[Rabbits].as_long()
    f = m[Foxes].as_long()
    h = m[Hawks].as_long()
    
    print()
    print("Food Web (consumption rates):")
    print(f"  Rabbits eat Grass: {r}/{g} = {r/g:.3f} (target: 0.1-0.5)")
    print(f"  Foxes eat Rabbits: {f}/{r} = {f/r:.3f} (target: 0.1-0.5)")
    print(f"  Hawks eat Rabbits+Foxes: {h}/{(r+f)} = {h/(r+f):.3f} (target: 0.1-0.5)")
    
    print()
    print("Ecosystem Health:")
    bio_index = 1.0  # all 4 species present
    # stability: closer to balanced = higher score
    # Simple heuristic: average of how close each consumption rate is to 0.3 (midpoint)
    cr1 = r / g
    cr2 = f / r
    cr3 = h / (r + f)
    # stability = 1 - avg deviation from ideal 0.3, scaled to 0-1
    avg_dev = (abs(cr1 - 0.3) + abs(cr2 - 0.3) + abs(cr3 - 0.3)) / 3
    stability = max(0, 1 - avg_dev / 0.4)  # normalize
    print(f"  biodiversity_index = {bio_index:.2f}")
    print(f"  stability_score = {stability:.3f}")
    print(f"  sustainability = True")
    print(f"  balance_achieved = True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")