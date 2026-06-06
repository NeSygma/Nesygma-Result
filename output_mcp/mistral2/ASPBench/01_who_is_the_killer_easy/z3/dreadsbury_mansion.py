from z3 import *

# Declare the solver
solver = Solver()

# People: 0 = Agatha, 1 = Butler, 2 = Charles
# Variables
killer = Int('killer')

# Hates matrix: hates[i][j] = True if person i hates person j
hates = [[Bool(f'hates_{i}_{j}') for j in range(3)] for i in range(3)]

# Richer matrix: richer[i][j] = True if person i is richer than person j
richer = [[Bool(f'richer_{i}_{j}') for j in range(3)] for i in range(3)]

# Constraint 1: Killer always hates their victim (Agatha is victim, index 0)
solver.add(Implies(killer == 0, hates[0][0]))
solver.add(Implies(killer == 1, hates[1][0]))
solver.add(Implies(killer == 2, hates[2][0]))

# Constraint 2: Killer is no richer than their victim (Agatha is victim, index 0)
solver.add(Implies(killer == 0, Not(richer[0][0])))
solver.add(Implies(killer == 1, Not(richer[1][0])))
solver.add(Implies(killer == 2, Not(richer[2][0])))

# Constraint 3: Charles hates no one that Agatha hates
# Agatha hates: everyone except the butler (index 1)
# So, for all j, if hates[0][j] is True, then hates[2][j] is False
for j in range(3):
    solver.add(Implies(hates[0][j], Not(hates[2][j])))

# Constraint 4: Agatha hates everybody except the butler
# Agatha does not hate herself (index 0)
solver.add(Not(hates[0][0]))
# Agatha does not hate the butler (index 1)
solver.add(Not(hates[0][1]))
# Agatha hates Charles (index 2)
solver.add(hates[0][2])

# Constraint 5: Butler hates everyone not richer than Aunt Agatha
# For all j, if Not(richer[1][0]), then hates[1][j] == True
for j in range(3):
    solver.add(Implies(Not(richer[1][0]), hates[1][j]))

# Constraint 6: Butler hates everyone whom Agatha hates
# For all j, if hates[0][j] is True, then hates[1][j] is True
for j in range(3):
    solver.add(Implies(hates[0][j], hates[1][j]))

# Constraint 7: No one hates everyone
# For all i, there exists at least one j such that hates[i][j] == False
for i in range(3):
    solver.add(Or(Not(hates[i][0]), Not(hates[i][1]), Not(hates[i][2])))

# Additional constraints to ensure uniqueness of the killer
# Killer must be one of 0, 1, or 2
solver.add(Or(killer == 0, killer == 1, killer == 2))

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    killer_val = model[killer]
    killer_name = None
    if killer_val == 0:
        killer_name = "Agatha"
    elif killer_val == 1:
        killer_name = "Butler"
    elif killer_val == 2:
        killer_name = "Charles"
    
    print("STATUS: sat")
    print(f"killer: {killer_val}")
    print(f"killer_name: {killer_name}")
    
    # Print hates matrix for verification
    print("\nHates matrix:")
    for i in range(3):
        for j in range(3):
            print(f"hates[{i}][{j}] = {model[hates[i][j]]}")
    
    # Print richer matrix for verification
    print("\nRicher matrix:")
    for i in range(3):
        for j in range(3):
            print(f"richer[{i}][{j}] = {model[richer[i][j]]}")
            
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")