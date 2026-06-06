from z3 import *

# BENCHMARK_MODE: ON (model-finding with minimization)
BENCHMARK_MODE = True

# 1. Declare symbolic variables
# Transmitters: A, B, C, D, E, F
transmitters = ['A', 'B', 'C', 'D', 'E', 'F']
freq_range = range(1, 6)  # Available frequencies: 1, 2, 3, 4, 5

# Assignments: one Int per transmitter
assign = {t: Int(f'assign_{t}') for t in transmitters}

# Objective: minimize the number of distinct frequencies used
# We will use an optimization approach to minimize the count of distinct frequencies

# 2. Interference graph constraints
# A interferes with B, C
# B interferes with A, D, E
# C interferes with A, D, F
# D interferes with B, C, E
# E interferes with B, D, F
# F interferes with C, E

interference = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D', 'F'],
    'D': ['B', 'C', 'E'],
    'E': ['B', 'D', 'F'],
    'F': ['C', 'E']
}

# 3. Add constraints
solver = Optimize()

# Each transmitter must be assigned exactly one frequency from 1 to 5
for t in transmitters:
    solver.add(And(assign[t] >= 1, assign[t] <= 5))

# Transmitters that interfere cannot use the same frequency
for t in transmitters:
    for neighbor in interference[t]:
        solver.add(assign[t] != assign[neighbor])

# Transmitters that interfere cannot use adjacent frequencies (differing by 1)
for t in transmitters:
    for neighbor in interference[t]:
        solver.add(Not(Or(
            assign[t] == assign[neighbor] + 1,
            assign[t] == assign[neighbor] - 1
        )))

# 4. Objective: minimize the number of distinct frequencies used
# We introduce a Boolean variable for each frequency and transmitter indicating if the frequency is used
freq_used = [Bool(f'freq_{f}_used') for f in freq_range]

# For each frequency, it is used if at least one transmitter is assigned to it
for f in freq_range:
    solver.add(Or([assign[t] == f for t in transmitters]) == freq_used[f-1])

# Minimize the sum of frequencies used
solver.minimize(Sum([If(freq_used[f-1], 1, 0) for f in freq_range]))

# 5. Check and print a clear result
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract assignments
    assignments = [(t, model[assign[t]]) for t in transmitters]
    for t, f in assignments:
        print(f"assignments: transmitter={t}, frequency={f}")
    # Extract number of distinct frequencies used
    frequencies_used = sum(1 for f in freq_range if model[freq_used[f-1]])
    print(f"frequencies_used: {frequencies_used}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")