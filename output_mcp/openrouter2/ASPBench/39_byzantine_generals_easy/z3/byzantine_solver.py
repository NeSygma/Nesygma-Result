from z3 import *

solver = Solver()
# Declare variables for initial proposals
G1 = Int('G1')
G2 = Int('G2')
G3 = Int('G3')
G4 = Int('G4')

# Initial proposals
solver.add(G1 == 1)
solver.add(G2 == 1)
solver.add(G3 == 0)
solver.add(G4 == 1)

# Consensus variable (0 or 1)
consensus = Int('consensus')
solver.add(consensus >= 0, consensus <= 1)

# Majority rule among honest generals (G1, G2, G3)
sumHonest = G1 + G2 + G3
solver.add(consensus == If(sumHonest > 1, 1, 0))

# Validity: if all honest have same initial value, consensus must be that value
solver.add(Implies(And(G1 == G2, G2 == G3), consensus == G1))

# Agreement: all honest generals decide the same value (implicitly satisfied by consensus)

# Check solver
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("consensus =", m[consensus])
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")