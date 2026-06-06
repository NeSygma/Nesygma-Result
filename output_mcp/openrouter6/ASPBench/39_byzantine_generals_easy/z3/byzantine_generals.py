from z3 import *

# Problem parameters
num_generals = 4
honest_indices = [0, 1, 2]  # G1, G2, G3 are honest
traitor_index = 3  # G4 is traitor
initial_proposals = [1, 1, 0, 1]  # G1:1, G2:1, G3:0, G4:1

# Decision variable: consensus value (0 or 1)
consensus = Int('consensus')
solver = Solver()

# Constraint: consensus must be 0 or 1
solver.add(Or(consensus == 0, consensus == 1))

# Extract honest proposals
honest_proposals = [initial_proposals[i] for i in honest_indices]

# Constraint 1: Validity - if all honest have same initial value, consensus must equal that value
all_same = And([honest_proposals[i] == honest_proposals[0] for i in range(len(honest_proposals))])
if all_same:
    solver.add(Implies(all_same, consensus == honest_proposals[0]))

# Constraint 2: Majority rule among honest generals
count1 = Sum([If(honest_proposals[i] == 1, 1, 0) for i in range(len(honest_proposals))])
count0 = Sum([If(honest_proposals[i] == 0, 1, 0) for i in range(len(honest_proposals))])

# Majority conditions
majority_1 = count1 > count0
majority_0 = count0 > count1
tie = count1 == count0

# Apply majority rule and tie-breaking
solver.add(Implies(majority_1, consensus == 1))
solver.add(Implies(majority_0, consensus == 0))
solver.add(Implies(tie, consensus == 0))  # Tie-breaking: default to 0

# Constraint 3: Agreement - all honest must decide same value (already encoded by single consensus variable)

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    consensus_value = model[consensus]
    print("STATUS: sat")
    print(f"consensus = {consensus_value}")
    print(f"honest_generals = G1, G2, G3")
    print(f"traitor = G4")
    print(f"Initial proposals: G1=1, G2=1, G3=0, G4=1")
    print(f"Majority among honest: 2 votes for 1, 1 vote for 0")
    print(f"Consensus value: {consensus_value}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")