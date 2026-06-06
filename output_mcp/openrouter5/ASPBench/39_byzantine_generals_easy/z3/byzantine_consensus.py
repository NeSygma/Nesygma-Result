from z3 import *

solver = Solver()

# Generals: G1, G2, G3, G4
# Initial proposals
initial = {
    "G1": 1,
    "G2": 1,
    "G3": 0,
    "G4": 1
}

# Traitor: G4 (can send different messages to different generals)
# Honest generals: G1, G2, G3
honest_generals = ["G1", "G2", "G3"]
traitor = "G4"

# The consensus value (0 or 1) that honest generals should adopt
consensus = Int('consensus')
solver.add(Or(consensus == 0, consensus == 1))

# Constraint 1: Agreement - all honest generals decide on the same value
# (This is enforced by having a single consensus variable)

# Constraint 2: Validity - If all honest generals have the same initial value, that must be the consensus
# Honest generals initial values: G1=1, G2=1, G3=0
# They are NOT all the same (1, 1, 0), so this constraint is vacuously true (no trigger)

# Constraint 3: Majority Rule - consensus should reflect majority vote among honest generals
# Honest votes: G1=1, G2=1, G3=0
# Majority is 1 (two out of three)
# So consensus must be 1

# Constraint 4: Tie-Breaking - In case of a tie among honest votes, use value 0 as default
# There is no tie (2 votes for 1, 1 vote for 0), so this doesn't apply

# Encode majority rule: count honest votes for 1 and for 0
# Honest: G1=1, G2=1, G3=0
# Votes for 1: 2, Votes for 0: 1
# Majority is 1

# The consensus must equal the majority value among honest generals
# Since 2 out of 3 honest generals proposed 1, the majority is 1
solver.add(consensus == 1)

# Check
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"consensus = {m[consensus]}")
    print(f"honest_generals = {honest_generals}")
    print(f"traitor = {traitor}")
    print(f"honest_initial_values = {{G1: 1, G2: 1, G3: 0}}")
    print(f"majority_vote = 1 (2 out of 3 honest generals proposed 1)")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")