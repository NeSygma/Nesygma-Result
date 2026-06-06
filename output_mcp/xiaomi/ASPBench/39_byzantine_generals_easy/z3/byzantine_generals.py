from z3 import *

solver = Solver()

# Generals: G1=0, G2=1, G3=2, G4=3
num_generals = 4
general_names = ["G1", "G2", "G3", "G4"]

# Initial proposals
proposals = [1, 1, 0, 1]  # G1=1, G2=1, G3=0, G4=1

# Traitor is G4 (index 3)
traitor_idx = 3

# Honest generals: G1, G2, G3 (indices 0, 1, 2)
honest_indices = [0, 1, 2]

# Consensus value (0 or 1)
consensus = Int('consensus')
solver.add(Or(consensus == 0, consensus == 1))

# Count honest votes for 0 and 1
honest_votes_for_1 = Sum([If(proposals[i] == 1, 1, 0) for i in honest_indices])
honest_votes_for_0 = Sum([If(proposals[i] == 0, 1, 0) for i in honest_indices])

# Constraint: Agreement - all honest generals decide the same value
# (consensus represents what all honest generals agree on)

# Constraint: Validity - if all honest generals have the same initial value, that must be consensus
# All honest have value 1: G1=1, G2=1, G3=0 -> not all same, so validity doesn't force anything
# All honest have value 0: not the case either
# Since honest proposals are [1, 1, 0], they don't all agree, so validity is vacuously satisfied

# Constraint: Majority Rule - consensus reflects majority vote among honest generals
# Honest votes: G1=1, G2=1, G3=0 -> 2 votes for 1, 1 vote for 0
# Majority is 1

# Constraint: Tie-breaking - if tie, use 0 as default
# No tie here (2 vs 1), so tie-breaking doesn't apply

# Model the decision logic:
# If votes_for_1 > votes_for_0, consensus = 1
# If votes_for_0 > votes_for_1, consensus = 0
# If tie, consensus = 0

solver.add(Implies(honest_votes_for_1 > honest_votes_for_0, consensus == 1))
solver.add(Implies(honest_votes_for_0 > honest_votes_for_1, consensus == 0))
solver.add(Implies(honest_votes_for_1 == honest_votes_for_0, consensus == 0))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"consensus = {m[consensus]}")
    print(f"honest_generals = {[general_names[i] for i in honest_indices]}")
    print(f"traitor = {general_names[traitor_idx]}")
    print(f"honest_votes_for_1 = {m.eval(honest_votes_for_1)}")
    print(f"honest_votes_for_0 = {m.eval(honest_votes_for_0)}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")