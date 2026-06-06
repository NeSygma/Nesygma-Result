from z3 import *

solver = Solver()

# Initial proposals (0/1 values)
g1 = Int('g1')
g2 = Int('g2')
g3 = Int('g3')
g4 = Int('g4')
solver.add(g1 == 1)
solver.add(g2 == 1)
solver.add(g3 == 0)
solver.add(g4 == 1)

# Consensus variable (0 or 1)
consensus = Int('consensus')
solver.add(consensus >= 0, consensus <= 1)

# Majority rule: if at least 2 out of 3 honest generals propose 1,
# then consensus must be 1, otherwise 0
sum_honest = g1 + g2 + g3
solver.add(If(sum_honest >= 2, consensus == 1, consensus == 0))

# Validity: if all honest generals have the same initial value,
# then consensus must equal that value
all_equal = And(g1 == g2, g2 == g3)
solver.add(Implies(all_equal, consensus == g1))

# Check satisfiability
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