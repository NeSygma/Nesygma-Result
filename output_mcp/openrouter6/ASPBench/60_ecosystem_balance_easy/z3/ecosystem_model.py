from z3 import *

# Create solver
solver = Solver()

# Define species with carrying capacities
CAPACITIES = {
    'grass': 100,
    'rabbits': 30,
    'foxes': 10,
    'hawks': 5
}

# Declare population variables (Real for ecological modeling)
grass_pop = Real('grass_pop')
rabbit_pop = Real('rabbit_pop')
fox_pop = Real('fox_pop')
hawk_pop = Real('hawk_pop')

# Declare consumption rates for each predator-prey relationship
# Rates must be between 0.1 and 0.5
cr_grass_rabbit = Real('cr_grass_rabbit')  # rabbits eating grass
cr_rabbit_fox = Real('cr_rabbit_fox')      # foxes eating rabbits
cr_rabbit_hawk = Real('cr_rabbit_hawk')    # hawks eating rabbits
cr_fox_hawk = Real('cr_fox_hawk')          # hawks eating foxes

# Constraint 1: All species must have non-negative populations
solver.add(grass_pop >= 0)
solver.add(rabbit_pop >= 0)
solver.add(fox_pop >= 0)
solver.add(hawk_pop >= 0)

# Constraint 2: Populations cannot exceed carrying capacity
solver.add(grass_pop <= CAPACITIES['grass'])
solver.add(rabbit_pop <= CAPACITIES['rabbits'])
solver.add(fox_pop <= CAPACITIES['foxes'])
solver.add(hawk_pop <= CAPACITIES['hawks'])

# Constraint 3: Herbivore populations must be sustainable relative to primary producers
# Rabbits ≤ 0.5 × Grass
solver.add(rabbit_pop <= 0.5 * grass_pop)

# Constraint 4: Predator populations must be sustainable relative to prey
# Foxes ≤ 0.3 × Rabbits
solver.add(fox_pop <= 0.3 * rabbit_pop)

# Constraint 5: No species can go extinct (all populations > 0)
solver.add(grass_pop > 0)
solver.add(rabbit_pop > 0)
solver.add(fox_pop > 0)
solver.add(hawk_pop > 0)

# Constraint 6: Food web relationships must be maintained with consumption rates between 0.1 and 0.5
solver.add(cr_grass_rabbit >= 0.1)
solver.add(cr_grass_rabbit <= 0.5)
solver.add(cr_rabbit_fox >= 0.1)
solver.add(cr_rabbit_fox <= 0.5)
solver.add(cr_rabbit_hawk >= 0.1)
solver.add(cr_rabbit_hawk <= 0.5)
solver.add(cr_fox_hawk >= 0.1)
solver.add(cr_fox_hawk <= 0.5)

# Consumption constraints: predator consumption cannot exceed prey availability
# Rabbits consume grass
solver.add(rabbit_pop * cr_grass_rabbit <= grass_pop)

# Foxes consume rabbits
solver.add(fox_pop * cr_rabbit_fox <= rabbit_pop)

# Hawks consume rabbits and foxes
solver.add(hawk_pop * cr_rabbit_hawk <= rabbit_pop)
solver.add(hawk_pop * cr_fox_hawk <= fox_pop)

# Additional constraint: Total rabbit consumption (by foxes and hawks) cannot exceed rabbit population
# This ensures multiple predators don't overconsume the same prey
solver.add(fox_pop * cr_rabbit_fox + hawk_pop * cr_rabbit_hawk <= rabbit_pop)

# Additional constraint: Hawk sustainability (since not explicitly specified)
# Hawks should not overconsume their prey: hawk_pop ≤ 0.2 × (rabbit_pop + fox_pop)
solver.add(hawk_pop <= 0.2 * (rabbit_pop + fox_pop))

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract population values
    grass_val = float(model[grass_pop].as_decimal(6).rstrip('?'))
    rabbit_val = float(model[rabbit_pop].as_decimal(6).rstrip('?'))
    fox_val = float(model[fox_pop].as_decimal(6).rstrip('?'))
    hawk_val = float(model[hawk_pop].as_decimal(6).rstrip('?'))
    
    # Extract consumption rates
    cr_grass_rabbit_val = float(model[cr_grass_rabbit].as_decimal(6).rstrip('?'))
    cr_rabbit_fox_val = float(model[cr_rabbit_fox].as_decimal(6).rstrip('?'))
    cr_rabbit_hawk_val = float(model[cr_rabbit_hawk].as_decimal(6).rstrip('?'))
    cr_fox_hawk_val = float(model[cr_fox_hawk].as_decimal(6).rstrip('?'))
    
    # Compute ecosystem health metrics
    # Biodiversity index: all 4 species have positive populations
    biodiversity_index = 1.0
    
    # Stability score: minimum of (population/capacity) across all species
    ratios = [
        grass_val / CAPACITIES['grass'],
        rabbit_val / CAPACITIES['rabbits'],
        fox_val / CAPACITIES['foxes'],
        hawk_val / CAPACITIES['hawks']
    ]
    stability_score = min(ratios)
    
    # Sustainability and balance achieved: all constraints satisfied
    sustainability = True
    balance_achieved = True
    
    print("STATUS: sat")
    print("\n=== STABLE POPULATIONS ===")
    print(f"Grass: {grass_val:.2f} (capacity: {CAPACITIES['grass']})")
    print(f"Rabbits: {rabbit_val:.2f} (capacity: {CAPACITIES['rabbits']})")
    print(f"Foxes: {fox_val:.2f} (capacity: {CAPACITIES['foxes']})")
    print(f"Hawks: {hawk_val:.2f} (capacity: {CAPACITIES['hawks']})")
    
    print("\n=== FOOD WEB CONSUMPTION RATES ===")
    print(f"Rabbits eating grass: {cr_grass_rabbit_val:.3f}")
    print(f"Foxes eating rabbits: {cr_rabbit_fox_val:.3f}")
    print(f"Hawks eating rabbits: {cr_rabbit_hawk_val:.3f}")
    print(f"Hawks eating foxes: {cr_fox_hawk_val:.3f}")
    
    print("\n=== ECOSYSTEM HEALTH ===")
    print(f"Biodiversity Index: {biodiversity_index:.3f}")
    print(f"Stability Score: {stability_score:.3f}")
    print(f"Sustainability: {sustainability}")
    print(f"Balance Achieved: {balance_achieved}")
    
    # Verify constraints
    print("\n=== CONSTRAINT VERIFICATION ===")
    print(f"Rabbits ≤ 0.5 × Grass: {rabbit_val:.2f} ≤ {0.5 * grass_val:.2f} ✓" if rabbit_val <= 0.5 * grass_val else f"Rabbits ≤ 0.5 × Grass: {rabbit_val:.2f} ≤ {0.5 * grass_val:.2f} ✗")
    print(f"Foxes ≤ 0.3 × Rabbits: {fox_val:.2f} ≤ {0.3 * rabbit_val:.2f} ✓" if fox_val <= 0.3 * rabbit_val else f"Foxes ≤ 0.3 × Rabbits: {fox_val:.2f} ≤ {0.3 * rabbit_val:.2f} ✗")
    print(f"Hawks ≤ 0.2 × (Rabbits + Foxes): {hawk_val:.2f} ≤ {0.2 * (rabbit_val + fox_val):.2f} ✓" if hawk_val <= 0.2 * (rabbit_val + fox_val) else f"Hawks ≤ 0.2 × (Rabbits + Foxes): {hawk_val:.2f} ≤ {0.2 * (rabbit_val + fox_val):.2f} ✗")
    
    # Consumption verification
    rabbit_grass_consumption = rabbit_val * cr_grass_rabbit_val
    fox_rabbit_consumption = fox_val * cr_rabbit_fox_val
    hawk_rabbit_consumption = hawk_val * cr_rabbit_hawk_val
    hawk_fox_consumption = hawk_val * cr_fox_hawk_val
    
    print(f"\nRabbits consume grass: {rabbit_grass_consumption:.2f} ≤ {grass_val:.2f} ✓" if rabbit_grass_consumption <= grass_val else f"Rabbits consume grass: {rabbit_grass_consumption:.2f} ≤ {grass_val:.2f} ✗")
    print(f"Total rabbit consumption: {fox_rabbit_consumption + hawk_rabbit_consumption:.2f} ≤ {rabbit_val:.2f} ✓" if fox_rabbit_consumption + hawk_rabbit_consumption <= rabbit_val else f"Total rabbit consumption: {fox_rabbit_consumption + hawk_rabbit_consumption:.2f} ≤ {rabbit_val:.2f} ✗")
    print(f"Hawks consume foxes: {hawk_fox_consumption:.2f} ≤ {fox_val:.2f} ✓" if hawk_fox_consumption <= fox_val else f"Hawks consume foxes: {hawk_fox_consumption:.2f} ≤ {fox_val:.2f} ✗")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No stable population levels satisfy all ecological constraints.")
    print("This suggests the constraints are too restrictive or contradictory.")
else:
    print("STATUS: unknown")
    print("Solver could not determine satisfiability.")