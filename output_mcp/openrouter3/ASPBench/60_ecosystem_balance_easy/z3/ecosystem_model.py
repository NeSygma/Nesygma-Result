from z3 import *

# Initialize solver
solver = Solver()

# Define population variables for each species
grass_pop = Int('grass_pop')
rabbit_pop = Int('rabbit_pop')
fox_pop = Int('fox_pop')
hawk_pop = Int('hawk_pop')

# Carrying capacities
CAP_GRASS = 100
CAP_RABBITS = 30
CAP_FOXES = 10
CAP_HAWKS = 5

# Constraint 1 & 5: All species must have non-negative populations and no extinction
solver.add(grass_pop > 0)
solver.add(rabbit_pop > 0)
solver.add(fox_pop > 0)
solver.add(hawk_pop > 0)

# Constraint 2: Populations cannot exceed carrying capacity
solver.add(grass_pop <= CAP_GRASS)
solver.add(rabbit_pop <= CAP_RABBITS)
solver.add(fox_pop <= CAP_FOXES)
solver.add(hawk_pop <= CAP_HAWKS)

# Constraint 3: Herbivore populations must be sustainable relative to primary producers
# Rabbits ≤ 0.5 × Grass
solver.add(rabbit_pop <= grass_pop * 0.5)

# Constraint 4: Predator populations must be sustainable relative to prey
# Foxes ≤ 0.3 × Rabbits
solver.add(fox_pop <= rabbit_pop * 0.3)

# Constraint 6: Food web relationships with consumption rates between 0.1 and 0.5
# Define consumption rate variables for each feeding relationship
# Relationships: Rabbits eat Grass, Foxes eat Rabbits, Hawks eat Rabbits and Foxes
rabbit_grass_rate = Real('rabbit_grass_rate')
fox_rabbit_rate = Real('fox_rabbit_rate')
hawk_rabbit_rate = Real('hawk_rabbit_rate')
hawk_fox_rate = Real('hawk_fox_rate')

# Consumption rates must be between 0.1 and 0.5
solver.add(rabbit_grass_rate >= 0.1, rabbit_grass_rate <= 0.5)
solver.add(fox_rabbit_rate >= 0.1, fox_rabbit_rate <= 0.5)
solver.add(hawk_rabbit_rate >= 0.1, hawk_rabbit_rate <= 0.5)
solver.add(hawk_fox_rate >= 0.1, hawk_fox_rate <= 0.5)

# Additional ecological balance constraints:
# The total consumption should not exceed available prey
# Rabbits consume grass: rabbit_pop * rabbit_grass_rate <= grass_pop
solver.add(rabbit_pop * rabbit_grass_rate <= grass_pop)

# Foxes consume rabbits: fox_pop * fox_rabbit_rate <= rabbit_pop
solver.add(fox_pop * fox_rabbit_rate <= rabbit_pop)

# Hawks consume rabbits and foxes: hawk_pop * (hawk_rabbit_rate + hawk_fox_rate) <= rabbit_pop + fox_pop
solver.add(hawk_pop * (hawk_rabbit_rate + hawk_fox_rate) <= rabbit_pop + fox_pop)

# Check for solutions
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nStable Population Levels:")
    print(f"Grass: {model[grass_pop]}")
    print(f"Rabbits: {model[rabbit_pop]}")
    print(f"Foxes: {model[fox_pop]}")
    print(f"Hawks: {model[hawk_pop]}")
    
    print("\nConsumption Rates:")
    print(f"Rabbit-Grass rate: {model[rabbit_grass_rate]}")
    print(f"Fox-Rabbit rate: {model[fox_rabbit_rate]}")
    print(f"Hawk-Rabbit rate: {model[hawk_rabbit_rate]}")
    print(f"Hawk-Fox rate: {model[hawk_fox_rate]}")
    
    # Calculate ecosystem health metrics
    grass_val = int(str(model[grass_pop]))
    rabbit_val = int(str(model[rabbit_pop]))
    fox_val = int(str(model[fox_pop]))
    hawk_val = int(str(model[hawk_pop]))
    
    # Biodiversity index: proportion of species at carrying capacity
    total_capacity = CAP_GRASS + CAP_RABBITS + CAP_FOXES + CAP_HAWKS
    total_pop = grass_val + rabbit_val + fox_val + hawk_val
    biodiversity_index = total_pop / total_capacity if total_capacity > 0 else 0
    
    # Stability score: inverse of variance from ideal ratios
    # Ideal ratios: Rabbits/Grass = 0.5, Foxes/Rabbits = 0.3
    rabbit_grass_ratio = rabbit_val / grass_val if grass_val > 0 else 0
    fox_rabbit_ratio = fox_val / rabbit_val if rabbit_val > 0 else 0
    
    # Calculate deviation from ideal ratios
    rabbit_deviation = abs(rabbit_grass_ratio - 0.5)
    fox_deviation = abs(fox_rabbit_ratio - 0.3)
    stability_score = 1.0 - (rabbit_deviation + fox_deviation) / 2
    
    # Sustainability: all constraints satisfied (already checked)
    sustainability = True
    
    # Balance achieved: all populations positive and within constraints
    balance_achieved = True
    
    print(f"\nEcosystem Health Metrics:")
    print(f"Biodiversity Index: {biodiversity_index:.3f}")
    print(f"Stability Score: {stability_score:.3f}")
    print(f"Sustainability: {sustainability}")
    print(f"Balance Achieved: {balance_achieved}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")