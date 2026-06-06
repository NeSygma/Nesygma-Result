from z3 import *

# Declare Bool variables for genes
g1, g2, g3, g4, g5 = Bools('g1 g2 g3 g4 g5')

solver = Solver()
# Constraints: each gene is Bool already
# Regulatory rules
solver.add(g1 == Not(g2))
solver.add(g2 == Not(g1))
solver.add(g3 == And(g4, g5))
solver.add(g4 == True)
solver.add(g5 == True)

# Enumerate all steady states (models)
steady_states = []
while solver.check() == sat:
    m = solver.model()
    # Extract values as 0/1
    state = {
        'g1': 1 if is_true(m[g1]) else 0,
        'g2': 1 if is_true(m[g2]) else 0,
        'g3': 1 if is_true(m[g3]) else 0,
        'g4': 1 if is_true(m[g4]) else 0,
        'g5': 1 if is_true(m[g5]) else 0,
    }
    steady_states.append(state)
    # Block this solution
    solver.add(Or(g1 != m[g1], g2 != m[g2], g3 != m[g3], g4 != m[g4], g5 != m[g5]))

print("STATUS: sat")
for s in steady_states:
    print("steady_state:", s)