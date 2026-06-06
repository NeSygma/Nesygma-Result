from z3 import *

# Declare variables
grass = Int('grass')
rabbits = Int('rabbits')
foxes = Int('foxes')
hawks = Int('hawks')

# Consumption rates (Real)
c_rg = Real('c_rg')  # rabbits eat grass
c_fr = Real('c_fr')  # foxes eat rabbits
c_hr = Real('c_hr')  # hawks eat rabbits
c_hf = Real('c_hf')  # hawks eat foxes

solver = Solver()

# Constraints
# Non-negative and >0 (no extinction)
solver.add(grass >= 1)
solver.add(rabbits >= 1)
solver.add(foxes >= 1)
solver.add(hawks >= 1)

# Carrying capacities
solver.add(grass <= 100)
solver.add(rabbits <= 30)
solver.add(foxes <= 10)
solver.add(hawks <= 5)

# Sustainability constraints
# Rabbits <= 0.5 * Grass -> 2*rabbits <= grass
solver.add(2 * rabbits <= grass)
# Foxes <= 0.3 * Rabbits -> 10*foxes <= 3*rabbits
solver.add(10 * foxes <= 3 * rabbits)

# Consumption rates between 0.1 and 0.5
solver.add(c_rg >= 0.1, c_rg <= 0.5)
solver.add(c_fr >= 0.1, c_fr <= 0.5)
solver.add(c_hr >= 0.1, c_hr <= 0.5)
solver.add(c_hf >= 0.1, c_hf <= 0.5)

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("grass =", m[grass])
    print("rabbits =", m[rabbits])
    print("foxes =", m[foxes])
    print("hawks =", m[hawks])
    print("c_rg =", m[c_rg])
    print("c_fr =", m[c_fr])
    print("c_hr =", m[c_hr])
    print("c_hf =", m[c_hf])
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")