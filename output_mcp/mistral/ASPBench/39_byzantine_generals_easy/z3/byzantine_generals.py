from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Declare consensus variable (0 or 1)
consensus = Int('consensus')
solver.add(Or(consensus == 0, consensus == 1))

# Define generals and their initial proposals
# G1: 1, G2: 1, G3: 0, G4: 1 (traitor)
proposals = {
    'G1': 1,
    'G2': 1,
    'G3': 0,
    'G4': 1  # traitor, but we ignore its proposal for honest consensus
}

# Honest generals (non-traitors)
honest_generals = ['G1', 'G2', 'G3']

# Constraint 1: Agreement - All honest generals must agree on the consensus
# Since we are modeling the consensus directly, this is implicitly satisfied by the consensus variable.
# No additional constraints needed here.

# Constraint 2: Validity - If all honest generals have the same initial value, consensus must equal that value
# Check if all honest generals have the same proposal
all_same = True
first_val = proposals[honest_generals[0]]
for g in honest_generals[1:]:
    if proposals[g] != first_val:
        all_same = False
        break

if all_same:
    solver.add(consensus == first_val)

# Constraint 3: Majority Rule - Consensus should reflect the majority vote among honest generals
# Count the number of 1s and 0s among honest generals
count_1 = Sum([If(proposals[g] == 1, 1, 0) for g in honest_generals])
count_0 = Sum([If(proposals[g] == 0, 1, 0) for g in honest_generals])

# Majority: if count_1 > count_0, consensus should be 1; if count_0 > count_1, consensus should be 0
solver.add(Implies(count_1 > count_0, consensus == 1))
solver.add(Implies(count_0 > count_1, consensus == 0))

# Constraint 4: Tie-Breaking - In case of a tie, use 0 as the default
solver.add(Implies(count_1 == count_0, consensus == 0))

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"consensus = {model[consensus]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")