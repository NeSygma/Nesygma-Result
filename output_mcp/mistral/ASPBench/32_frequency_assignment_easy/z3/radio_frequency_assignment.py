from z3 import *

# Problem: Assign frequencies to transmitters minimizing interference and total frequencies used
# Transmitters: A, B, C, D, E, F
# Frequencies: 1, 2, 3, 4, 5
# Interference graph:
# A interferes with: B, C
# B interferes with: A, D, E
# C interferes with: A, D, F
# D interferes with: B, C, E
# E interferes with: B, D, F
# F interferes with: C, E

# Constraints:
# 1. Each transmitter gets exactly one frequency from 1-5
# 2. Interfering transmitters cannot use the same frequency
# 3. Interfering transmitters cannot use adjacent frequencies (difference of 1)
# Objective: Minimize the total number of distinct frequencies used

# BENCHMARK_MODE: ON (problem is solvable)
BENCHMARK_MODE = True

# Create solver for optimization
opt = Optimize()

# Declare transmitters and their frequency assignments
transmitters = ['A', 'B', 'C', 'D', 'E', 'F']
freq_assign = {t: Int(f"freq_{t}") for t in transmitters}

# Declare boolean variables for which frequencies are used
freq_used = [Bool(f"used_{f}") for f in range(1, 6)]

# Each transmitter must be assigned a frequency between 1 and 5
for t in transmitters:
    opt.add(freq_assign[t] >= 1, freq_assign[t] <= 5)

# If a transmitter is assigned frequency f, then freq_used[f-1] must be True
for t in transmitters:
    for f in range(1, 6):
        opt.add(Implies(freq_assign[t] == f, freq_used[f-1]))

# Interference constraints:
# A interferes with B, C
opt.add(freq_assign['A'] != freq_assign['B'])
opt.add(Not(Or(freq_assign['A'] == freq_assign['B'] - 1, freq_assign['A'] == freq_assign['B'] + 1)))
opt.add(freq_assign['A'] != freq_assign['C'])
opt.add(Not(Or(freq_assign['A'] == freq_assign['C'] - 1, freq_assign['A'] == freq_assign['C'] + 1)))

# B interferes with A, D, E
opt.add(freq_assign['B'] != freq_assign['A'])
opt.add(Not(Or(freq_assign['B'] == freq_assign['A'] - 1, freq_assign['B'] == freq_assign['A'] + 1)))
opt.add(freq_assign['B'] != freq_assign['D'])
opt.add(Not(Or(freq_assign['B'] == freq_assign['D'] - 1, freq_assign['B'] == freq_assign['D'] + 1)))
opt.add(freq_assign['B'] != freq_assign['E'])
opt.add(Not(Or(freq_assign['B'] == freq_assign['E'] - 1, freq_assign['B'] == freq_assign['E'] + 1)))

# C interferes with A, D, F
opt.add(freq_assign['C'] != freq_assign['A'])
opt.add(Not(Or(freq_assign['C'] == freq_assign['A'] - 1, freq_assign['C'] == freq_assign['A'] + 1)))
opt.add(freq_assign['C'] != freq_assign['D'])
opt.add(Not(Or(freq_assign['C'] == freq_assign['D'] - 1, freq_assign['C'] == freq_assign['D'] + 1)))
opt.add(freq_assign['C'] != freq_assign['F'])
opt.add(Not(Or(freq_assign['C'] == freq_assign['F'] - 1, freq_assign['C'] == freq_assign['F'] + 1)))

# D interferes with B, C, E
opt.add(freq_assign['D'] != freq_assign['B'])
opt.add(Not(Or(freq_assign['D'] == freq_assign['B'] - 1, freq_assign['D'] == freq_assign['B'] + 1)))
opt.add(freq_assign['D'] != freq_assign['C'])
opt.add(Not(Or(freq_assign['D'] == freq_assign['C'] - 1, freq_assign['D'] == freq_assign['C'] + 1)))
opt.add(freq_assign['D'] != freq_assign['E'])
opt.add(Not(Or(freq_assign['D'] == freq_assign['E'] - 1, freq_assign['D'] == freq_assign['E'] + 1)))

# E interferes with B, D, F
opt.add(freq_assign['E'] != freq_assign['B'])
opt.add(Not(Or(freq_assign['E'] == freq_assign['B'] - 1, freq_assign['E'] == freq_assign['B'] + 1)))
opt.add(freq_assign['E'] != freq_assign['D'])
opt.add(Not(Or(freq_assign['E'] == freq_assign['D'] - 1, freq_assign['E'] == freq_assign['D'] + 1)))
opt.add(freq_assign['E'] != freq_assign['F'])
opt.add(Not(Or(freq_assign['E'] == freq_assign['F'] - 1, freq_assign['E'] == freq_assign['F'] + 1)))

# F interferes with C, E
opt.add(freq_assign['F'] != freq_assign['C'])
opt.add(Not(Or(freq_assign['F'] == freq_assign['C'] - 1, freq_assign['F'] == freq_assign['C'] + 1)))
opt.add(freq_assign['F'] != freq_assign['E'])
opt.add(Not(Or(freq_assign['F'] == freq_assign['E'] - 1, freq_assign['F'] == freq_assign['E'] + 1)))

# Objective: Minimize the number of distinct frequencies used
opt.minimize(Sum(freq_used))

# Check for a solution
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal solution found!")
    print("\nFrequency assignments:")
    for t in transmitters:
        print(f"{t} = {model[freq_assign[t]]}")
    
    # Count distinct frequencies used
    used_freqs = set()
    for f in range(1, 6):
        if model.eval(freq_used[f-1], model_completion=True):
            used_freqs.add(f)
    
    print(f"\nTotal distinct frequencies used: {len(used_freqs)}")
    print(f"Frequencies used: {sorted(used_freqs)}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")