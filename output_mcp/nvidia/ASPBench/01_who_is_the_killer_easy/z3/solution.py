from z3 import *

# Hate matrix
hate = [[Bool(f'hate_{i}_{j}') for j in range(3)] for i in range(3)]

# Wealth
wealth = [Int(f'wealth_{i}') for i in range(3)]

solver = Solver()

# Constraint 4: Agatha hates everybody except the butler (i.e., only Charles)
# She hates Charles (2), does not hate herself (0) or Butler (1)
solver.add(hate[0][2])          # Agatha hates Charles
solver.add(Not(hate[0][0]))     # does not hate herself
solver.add(Not(hate[0][1]))     # does not hate Butler

# Constraint 5: Butler hates everyone not richer than Aunt Agatha
for i in range(3):
    solver.add(Implies(wealth[i] <= wealth[0], hate[1][i]))

# Constraint 6: Butler hates everyone whom Agatha hates
for j in range(3):
    solver.add(Implies(hate[0][j], hate[1][j]))

# Constraint 3: Charles hates no one that Agatha hates
for j in range(3):
    solver.add(Implies(hate[0][j], Not(hate[2][j])))

# Constraint 7: No one hates everyone
for i in range(3):
    solver.add(Or(*[Not(hate[i][j]) for j in range(3)]))

# Define killer variables
killer = [Bool(f'killer_{i}') for i in range(3)]

# Exactly one killer
for i in range(3):
    for j in range(i+1, 3):
        solver.add(Not(And(killer[i], killer[j])))
solver.add(Or(killer[0], killer[1], killer[2]))

# If someone is the killer, they must hate the victim (Agatha) and be no richer than the victim
for i in range(3):
    solver.add(Implies(killer[i], hate[i][0]))
    solver.add(Implies(killer[i], wealth[i] <= wealth[0]))

# Give concrete wealth values to guide the model
solver.add(wealth[0] == 0)  # Agatha
solver.add(wealth[1] == 1)  # Butler
solver.add(wealth[2] == 0)  # Charles

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Find the killer index
    for i in range(3):
        if m[killer[i]]:
            killer_idx = i
            break
    names = ["Agatha", "Butler", "Charles"]
    print(f"killer_name = {names[killer_idx]}")
else:
    print("STATUS: unsat")