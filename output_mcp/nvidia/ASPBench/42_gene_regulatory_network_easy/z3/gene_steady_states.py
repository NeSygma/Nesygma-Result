from z3 import *

# Declare Boolean variables for the five genes
g1 = Bool('g1')
g2 = Bool('g2')
g3 = Bool('g3')
g4 = Bool('g4')
g5 = Bool('g5')

solver = Solver()

# Encode the steady‑state constraints
# g1 <=> not g2
solver.add(g1 == Not(g2))
# g2 <=> not g1
solver.add(g2 == Not(g1))
# g3 <=> (g4 and g5)
solver.add(g3 == And(g4, g5))
# g4 is always active
solver.add(g4 == True)
# g5 is always active
solver.add(g5 == True)

# Enumerate all models (steady states)
while solver.check() == sat:
    m = solver.model()
    # Print the status line required by the pipeline
    print("STATUS: sat")
    # Convert the model to a dictionary with 0/1 values
    sol = {
        'g1': 1 if m[g1] else 0,
        'g2': 1 if m[g2] else 0,
        'g3': 1 if m[g3] else 0,
        'g4': 1 if m[g4] else 0,
        'g5': 1 if m[g5] else 0,
    }
    # Print the dictionary representing one steady state
    print(sol)
    # Block the current solution to find the next one
    solver.add(Or([g1 != m[g1], g2 != m[g2], g3 != m[g3], g4 != m[g4], g5 != m[g5]]))