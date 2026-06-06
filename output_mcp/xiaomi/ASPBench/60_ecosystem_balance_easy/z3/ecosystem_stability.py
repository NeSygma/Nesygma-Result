from z3 import *

# Create solver
solver = Solver()

# Species populations (stable levels)
grass = Int('grass')
rabbits = Int('rabbits')
foxes = Int('foxes')
hawks = Int('hawks')

# Carrying capacities
GRASS_CAP = 100
RABBITS_CAP = 30
FOXES_CAP = 10
HAWKS_CAP = 5

# Constraint 1: All species must have non-negative populations
solver.add(grass >= 0)
solver.add(rabbits >= 0)
solver.add(foxes >= 0)
solver.add(hawks >= 0)

# Constraint 2: Populations cannot exceed carrying capacity
solver.add(grass <= GRASS_CAP)
solver.add(rabbits <= RABBITS_CAP)
solver.add(foxes <= FOXES_CAP)
solver.add(hawks <= HAWKS_CAP)

# Constraint 3: Herbivore populations must be sustainable relative to primary producers
solver.add(rabbits <= 0.5 * grass)

# Constraint 4: Predator populations must be sustainable relative to prey
solver.add(foxes <= 0.3 * rabbits)

# Constraint 5: No species can go extinct (all populations > 0)
solver.add(grass > 0)
solver.add(rabbits > 0)
solver.add(foxes > 0)
solver.add(hawks > 0)

# Constraint 6: Food web relationships must be maintained with consumption rates between 0.1 and 0.5
# Define consumption rates for each predator-prey relationship
consumption_rabbit_grass = Real('consumption_rabbit_grass')  # Rabbits eat Grass
consumption_fox_rabbit = Real('consumption_fox_rabbit')       # Foxes eat Rabbits
consumption_hawk_rabbit = Real('consumption_hawk_rabbit')     # Hawks eat Rabbits
consumption_hawk_fox = Real('consumption_hawk_fox')           # Hawks eat Foxes

# Consumption rates must be between 0.1 and 0.5
solver.add(consumption_rabbit_grass >= 0.1)
solver.add(consumption_rabbit_grass <= 0.5)
solver.add(consumption_fox_rabbit >= 0.1)
solver.add(consumption_fox_rabbit <= 0.5)
solver.add(consumption_hawk_rabbit >= 0.1)
solver.add(consumption_hawk_rabbit <= 0.5)
solver.add(consumption_hawk_fox >= 0.1)
solver.add(consumption_hawk_fox <= 0.5)

# Additional ecological constraints for stability:
# - Hawks should be limited by both rabbits and foxes availability
solver.add(hawks <= 0.2 * rabbits)
solver.add(hawks <= 0.3 * foxes)

# - Total consumption should not exceed available resources
# Rabbits consume grass: consumption_rabbit_grass * rabbits <= grass
solver.add(consumption_rabbit_grass * rabbits <= grass)
# Foxes consume rabbits: consumption_fox_rabbit * foxes <= rabbits
solver.add(consumption_fox_rabbit * foxes <= rabbits)
# Hawks consume rabbits and foxes: consumption_hawk_rabbit * hawks + consumption_hawk_fox * hawks <= rabbits + foxes
solver.add(consumption_hawk_rabbit * hawks + consumption_hawk_fox * hawks <= rabbits + foxes)

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract population values
    grass_val = model[grass].as_long()
    rabbits_val = model[rabbits].as_long()
    foxes_val = model[foxes].as_long()
    hawks_val = model[hawks].as_long()
    
    # Extract consumption rates
    cr_grass = float(model[consumption_rabbit_grass].as_decimal(10).replace('?', ''))
    cr_rabbit = float(model[consumption_fox_rabbit].as_decimal(10).replace('?', ''))
    cr_hawk_rabbit = float(model[consumption_hawk_rabbit].as_decimal(10).replace('?', ''))
    cr_hawk_fox = float(model[consumption_hawk_fox].as_decimal(10).replace('?', ''))
    
    # Calculate ecosystem health metrics
    # Biodiversity index: based on population distribution (normalized)
    total_pop = grass_val + rabbits_val + foxes_val + hawks_val
    # Shannon diversity approximation
    p_grass = grass_val / total_pop
    p_rabbits = rabbits_val / total_pop
    p_foxes = foxes_val / total_pop
    p_hawks = hawks_val / total_pop
    
    # Avoid log(0) by ensuring all are positive
    biodiversity = -(p_grass * (p_grass if p_grass > 0 else 1) + 
                     p_rabbits * (p_rabbits if p_rabbits > 0 else 1) + 
                     p_foxes * (p_foxes if p_foxes > 0 else 1) + 
                     p_hawks * (p_hawks if p_hawks > 0 else 1))
    # Normalize to 0-1 range (max entropy for 4 species is ln(4) ≈ 1.386)
    biodiversity_index = min(1.0, max(0.0, biodiversity / 1.386))
    
    # Stability score: based on how well populations are balanced
    # Check if all constraints are satisfied with margin
    stability_score = 1.0  # Start with perfect
    # Reduce score if populations are too close to limits
    stability_score -= (grass_val / GRASS_CAP) * 0.1
    stability_score -= (rabbits_val / RABBITS_CAP) * 0.1
    stability_score -= (foxes_val / FOXES_CAP) * 0.1
    stability_score -= (hawks_val / HAWKS_CAP) * 0.1
    stability_score = max(0.0, min(1.0, stability_score))
    
    # Sustainability: check if all constraints are satisfied
    sustainable = (grass_val > 0 and rabbits_val > 0 and foxes_val > 0 and hawks_val > 0 and
                   rabbits_val <= 0.5 * grass_val and
                   foxes_val <= 0.3 * rabbits_val and
                   hawks_val <= 0.2 * rabbits_val and
                   hawks_val <= 0.3 * foxes_val)
    
    # Balance achieved: all constraints satisfied
    balance_achieved = sustainable
    
    print("STATUS: sat")
    print("\n=== Stable Population Levels ===")
    print(f"stable_populations:")
    print(f"  Grass: {grass_val}")
    print(f"  Rabbits: {rabbits_val}")
    print(f"  Foxes: {foxes_val}")
    print(f"  Hawks: {hawks_val}")
    
    print(f"\nfood_web:")
    print(f"  - predator: Rabbits, prey: Grass, consumption_rate: {cr_grass:.3f}")
    print(f"  - predator: Foxes, prey: Rabbits, consumption_rate: {cr_rabbit:.3f}")
    print(f"  - predator: Hawks, prey: Rabbits, consumption_rate: {cr_hawk_rabbit:.3f}")
    print(f"  - predator: Hawks, prey: Foxes, consumption_rate: {cr_hawk_fox:.3f}")
    
    print(f"\necosystem_health:")
    print(f"  biodiversity_index: {biodiversity_index:.3f}")
    print(f"  stability_score: {stability_score:.3f}")
    print(f"  sustainability: {sustainable}")
    
    print(f"\nbalance_achieved: {balance_achieved}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")