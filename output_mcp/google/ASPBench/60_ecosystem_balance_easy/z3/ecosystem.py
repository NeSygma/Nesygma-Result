from z3 import *

# Define the solver
solver = Solver()

# 1. Declare variables
# Populations
G = Int('Grass')
R = Int('Rabbits')
F = Int('Foxes')
H = Int('Hawks')

# Consumption rates (0.1 to 0.5)
c_RG = Real('c_RG')
c_FR = Real('c_FR')
c_HR = Real('c_HR')
c_HF = Real('c_HF')

# 2. Add constraints
# Non-negative and non-extinction
solver.add(G > 0, R > 0, F > 0, H > 0)

# Carrying capacities
solver.add(G <= 100, R <= 30, F <= 10, H <= 5)

# Sustainability constraints
solver.add(R <= 0.5 * G)
solver.add(F <= 0.3 * R)
# Assuming Hawks follow the same predator-prey logic relative to their prey (Rabbits and Foxes)
solver.add(H <= 0.3 * (R + F))

# Consumption rates
for c in [c_RG, c_FR, c_HR, c_HF]:
    solver.add(c >= 0.1, c <= 0.5)

# 3. Check for a solution
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"stable_populations: {{'Grass': {m[G]}, 'Rabbits': {m[R]}, 'Foxes': {m[F]}, 'Hawks': {m[H]}}}")
    print(f"food_web: {{'Rabbit-Grass': {m[c_RG]}, 'Fox-Rabbit': {m[c_FR]}, 'Hawk-Rabbit': {m[c_HR]}, 'Hawk-Fox': {m[c_HF]}}}")
    
    # Calculate metrics
    biodiversity = (m[G].as_long() + m[R].as_long() + m[F].as_long() + m[H].as_long()) / 145.0
    stability = (m[G].as_long()/100 + m[R].as_long()/30 + m[F].as_long()/10 + m[H].as_long()/5) / 4.0
    
    print(f"ecosystem_health.biodiversity_index: {float(biodiversity):.2f}")
    print(f"ecosystem_health.stability_score: {float(stability):.2f}")
    print("ecosystem_health.sustainability: True")
    print("balance_achieved: True")
else:
    print("STATUS: unsat")