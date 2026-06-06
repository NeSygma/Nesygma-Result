from z3 import *

# Create Boolean variables for each gene's state
g1, g2, g3, g4, g5 = Bools('g1 g2 g3 g4 g5')

# Create a solver
solver = Solver()

# Regulatory Rules:
# g1 is active IF AND ONLY IF g2 is not active
solver.add(g1 == Not(g2))

# g2 is active IF AND ONLY IF g1 is not active
solver.add(g2 == Not(g1))

# g3 is active IF AND ONLY IF (g4 is active AND g5 is active)
solver.add(g3 == And(g4, g5))

# g4 is active ALWAYS (constitutive expression)
solver.add(g4 == True)

# g5 is active ALWAYS (constitutive expression)
solver.add(g5 == True)

# Find all steady states (all solutions)
decision_vars = [g1, g2, g3, g4, g5]
solutions = []

while solver.check() == sat:
    m = solver.model()
    # Extract the solution
    sol = {
        'g1': 1 if is_true(m.eval(g1)) else 0,
        'g2': 1 if is_true(m.eval(g2)) else 0,
        'g3': 1 if is_true(m.eval(g3)) else 0,
        'g4': 1 if is_true(m.eval(g4)) else 0,
        'g5': 1 if is_true(m.eval(g5)) else 0
    }
    solutions.append(sol)
    
    # Block this solution to find others
    solver.add(Or([v != m.eval(v) for v in decision_vars]))

print("STATUS: sat")
print(f"Total steady states found: {len(solutions)}")
print("steady_states = [")
for sol in solutions:
    print(f"  {sol},")
print("]")