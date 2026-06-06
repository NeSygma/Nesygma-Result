from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables
# Consensus value (0 or 1)
consensus = Int('consensus')

# Honesty of generals (True = honest, False = traitor)
honest = {
    'G1': Bool('honest_G1'),
    'G2': Bool('honest_G2'),
    'G3': Bool('honest_G3'),
    'G4': Bool('honest_G4'),
}

# Initial proposals (only honest generals' proposals matter)
proposals = {
    'G1': Int('proposal_G1'),
    'G2': Int('proposal_G2'),
    'G3': Int('proposal_G3'),
    'G4': Int('proposal_G4'),
}

# Initialize proposals based on the problem statement
solver = Solver()
solver.add(proposals['G1'] == 1)
solver.add(proposals['G2'] == 1)
solver.add(proposals['G3'] == 0)
solver.add(proposals['G4'] == 1)

# Traitor is G4
solver.add(honest['G4'] == False)

# Honest generals are G1, G2, G3
solver.add(honest['G1'] == True)
solver.add(honest['G2'] == True)
solver.add(honest['G3'] == True)

# Agreement: All honest generals must decide on the same value
# This is enforced by the consensus value being the same for all honest generals

# Validity: If all honest generals have the same initial value, that must be the consensus
# Check if all honest generals have the same proposal
all_honest_same = And(
    proposals['G1'] == proposals['G2'],
    proposals['G2'] == proposals['G3']
)

# If all honest generals have the same proposal, consensus must equal that value
solver.add(Implies(all_honest_same, consensus == proposals['G1']))

# Majority Rule: The consensus should reflect the majority vote among honest generals
# Count the number of honest generals voting for 0 and 1
count_0 = Sum([If(And(honest[g], proposals[g] == 0), 1, 0) for g in ['G1', 'G2', 'G3']])
count_1 = Sum([If(And(honest[g], proposals[g] == 1), 1, 0) for g in ['G1', 'G2', 'G3']])

# Majority rule: consensus should be 1 if more honest generals vote for 1, else 0
solver.add(Implies(count_1 > count_0, consensus == 1))
solver.add(Implies(count_0 > count_1, consensus == 0))

# Tie-Breaking: In case of a tie, use 0 as the default
solver.add(Implies(count_0 == count_1, consensus == 0))

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"consensus = {model[consensus]}")
    print(f"honest_G1 = {model[honest['G1']]}")
    print(f"honest_G2 = {model[honest['G2']]}")
    print(f"honest_G3 = {model[honest['G3']]}")
    print(f"honest_G4 = {model[honest['G4']]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")