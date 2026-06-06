from z3 import *

# People indices
AGATHA = 0
BUTLER = 1
CHARLES = 2

# Create solver
solver = Solver()

# Variables
killer = Int('killer')
hate = [[Bool(f'hate_{i}_{j}') for j in range(3)] for i in range(3)]
richer = [[Bool(f'richer_{i}_{j}') for j in range(3)] for i in range(3)]

# Domain constraints
solver.add(killer >= 0, killer <= 2)

# Constraint 1: Killer hates victim (Agatha)
solver.add(Or([And(killer == i, hate[i][AGATHA]) for i in range(3)]))

# Constraint 2: Killer is not richer than victim
solver.add(Or([And(killer == i, Not(richer[i][AGATHA])) for i in range(3)]))

# Constraint 3: Charles hates no one that Agatha hates
for j in range(3):
    solver.add(Implies(hate[AGATHA][j], Not(hate[CHARLES][j])))

# Constraint 4: Agatha hates everybody except the butler
for j in range(3):
    if j == BUTLER:
        solver.add(Not(hate[AGATHA][j]))
    else:
        solver.add(hate[AGATHA][j])

# Constraint 5: Butler hates everyone not richer than Agatha
for j in range(3):
    solver.add(Implies(Not(richer[j][AGATHA]), hate[BUTLER][j]))

# Constraint 6: Butler hates everyone whom Agatha hates
for j in range(3):
    solver.add(Implies(hate[AGATHA][j], hate[BUTLER][j]))

# Constraint 7: No one hates everyone
for i in range(3):
    solver.add(Or([Not(hate[i][j]) for j in range(3)]))

# Check for solutions
result = solver.check()

if result == sat:
    model = solver.model()
    killer_val = model[killer].as_long()
    killer_names = ["Agatha", "Butler", "Charles"]
    
    print("STATUS: sat")
    print(f"killer: {killer_val}")
    print(f"killer_name: {killer_names[killer_val]}")
    
    # Print hate matrix for verification
    print("\nHate matrix:")
    for i in range(3):
        for j in range(3):
            val = model[hate[i][j]]
            print(f"  {killer_names[i]} hates {killer_names[j]}: {val}")
    
    # Print richer matrix for verification
    print("\nRicher matrix:")
    for i in range(3):
        for j in range(3):
            val = model[richer[i][j]]
            print(f"  {killer_names[i]} richer than {killer_names[j]}: {val}")
            
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - constraints are contradictory")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")