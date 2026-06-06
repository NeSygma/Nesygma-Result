from z3 import *

# Problem parameters
N = 4  # Total generals
H = 3  # Honest generals (G1, G2, G3)
T = 1  # Traitor (G4)

# Initial proposals (for honest generals)
initial_proposals = [1, 1, 0]  # G1, G2, G3

# Create solver
solver = Solver()

# Decision variables for honest generals (what they decide)
# Each honest general decides 0 or 1
honest_decisions = [Bool(f"honest_{i}") for i in range(H)]

# Traitor's behavior: can send different messages to different generals
# We model this by allowing the traitor to influence the decisions
# For simplicity, we'll consider the traitor can cause any honest general to flip their decision

# Constraint 1: Agreement - all honest generals must decide the same value
# Convert Bool to Int (0/1) for comparison
honest_ints = [If(honest_decisions[i], 1, 0) for i in range(H)]
for i in range(H-1):
    solver.add(honest_ints[i] == honest_ints[i+1])

# Constraint 2: Validity - if all honest have same initial value, that must be consensus
# Check if all initial proposals are the same
all_same_initial = all(p == initial_proposals[0] for p in initial_proposals)
if all_same_initial:
    # If all honest start with same value, consensus must be that value
    consensus_value = initial_proposals[0]
    solver.add(honest_ints[0] == consensus_value)

# Constraint 3: Majority rule - consensus should reflect majority among honest
# Count how many honest start with 1 vs 0
count_ones = sum(initial_proposals)
count_zeros = H - count_ones

# Majority value among honest
if count_ones > count_zeros:
    majority_value = 1
elif count_zeros > count_ones:
    majority_value = 0
else:
    # Tie case - handled by tie-breaking constraint
    majority_value = None

if majority_value is not None:
    # Consensus should be majority value
    solver.add(honest_ints[0] == majority_value)

# Constraint 4: Tie-breaking - if tie among honest, use 0
if count_ones == count_zeros:
    solver.add(honest_ints[0] == 0)

# Additional constraint: Traitor can influence but system handles 1 traitor
# For this problem, we assume the protocol ensures honest agree despite traitor
# We don't need to explicitly model traitor's messages since we're finding consensus

# Check for solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract consensus value
    consensus_val = model.eval(honest_ints[0], model_completion=True)
    print(f"consensus = {consensus_val}")
    
    # Show honest generals' decisions
    print("honest_generals_decisions:")
    for i in range(H):
        val = model.eval(honest_ints[i], model_completion=True)
        print(f"  G{i+1} = {val}")
    
    # Determine honest generals list
    honest_generals = ["G1", "G2", "G3"]
    print(f"honest_generals = {honest_generals}")
    print(f"traitor = G4")
    
    # Print answer in required format
    print(f"answer:{consensus_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")