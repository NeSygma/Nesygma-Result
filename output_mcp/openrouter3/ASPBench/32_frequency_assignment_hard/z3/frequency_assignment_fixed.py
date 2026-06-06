from z3 import *

# Problem data
transmitters = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10"]

# Frequency data: (frequency, band, cost)
frequencies = [
    (101, "low", 10), (102, "low", 12), (103, "low", 15),
    (201, "mid", 20), (202, "mid", 22), (203, "mid", 25), (204, "mid", 28),
    (301, "high", 40), (302, "high", 45)
]

# Band restrictions per transmitter
band_restrictions = {
    "t1": ["low"], "t2": ["low"],
    "t3": ["mid"], "t4": ["mid"], "t5": ["mid"],
    "t6": ["high"],
    "t7": ["low", "mid"], "t8": ["low", "mid"],
    "t9": ["mid", "high"], "t10": ["mid", "high"]
}

# Interference pairs
interference_pairs = [
    ("t1", "t2"), ("t1", "t7"), ("t2", "t8"), ("t3", "t4"), ("t3", "t9"),
    ("t4", "t5"), ("t4", "t7"), ("t5", "t8"), ("t5", "t10"), ("t6", "t9"), ("t6", "t10")
]

# Create optimization solver
opt = Optimize()

# Create variables for each transmitter's frequency assignment
# We'll use integer variables representing the frequency index (0-8)
freq_vars = {}
for t in transmitters:
    freq_vars[t] = Int(f"freq_{t}")

# Map frequency indices to actual frequency values and bands
freq_to_value = {}
freq_to_band = {}
freq_to_cost = {}
for idx, (freq_val, band, cost) in enumerate(frequencies):
    freq_to_value[idx] = freq_val
    freq_to_band[idx] = band
    freq_to_cost[idx] = cost

# Constraint 1: Each transmitter gets a valid frequency index (0-8)
for t in transmitters:
    opt.add(freq_vars[t] >= 0)
    opt.add(freq_vars[t] <= 8)

# Constraint 2: Band restrictions
for t in transmitters:
    allowed_bands = band_restrictions[t]
    # freq_vars[t] must be in the set of indices corresponding to allowed bands
    allowed_indices = [idx for idx in range(9) if freq_to_band[idx] in allowed_bands]
    opt.add(Or([freq_vars[t] == idx for idx in allowed_indices]))

# Constraint 3: Interference constraints
for (t1, t2) in interference_pairs:
    f1 = freq_vars[t1]
    f2 = freq_vars[t2]
    
    # For each possible pair of frequency indices, check if they violate constraints
    for idx1 in range(9):
        for idx2 in range(9):
            band1 = freq_to_band[idx1]
            band2 = freq_to_band[idx2]
            freq_val1 = freq_to_value[idx1]
            freq_val2 = freq_to_value[idx2]
            
            if band1 == band2:
                # Same band: frequencies must differ by more than 1
                constraint = Implies(
                    And(f1 == idx1, f2 == idx2),
                    abs(freq_val1 - freq_val2) > 1
                )
                opt.add(constraint)
            else:
                # Different bands: frequency numbers must differ
                constraint = Implies(
                    And(f1 == idx1, f2 == idx2),
                    freq_val1 != freq_val2
                )
                opt.add(constraint)

# Objective: Minimize total cost
# We need to create a cost variable that depends on the frequency assignment
# Use If expressions to select the cost based on the frequency index
total_cost = Sum([
    If(freq_vars[t] == 0, frequencies[0][2],
    If(freq_vars[t] == 1, frequencies[1][2],
    If(freq_vars[t] == 2, frequencies[2][2],
    If(freq_vars[t] == 3, frequencies[3][2],
    If(freq_vars[t] == 4, frequencies[4][2],
    If(freq_vars[t] == 5, frequencies[5][2],
    If(freq_vars[t] == 6, frequencies[6][2],
    If(freq_vars[t] == 7, frequencies[7][2],
    frequencies[8][2])))))))) for t in transmitters
])
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Assignments:")
    total_cost_value = 0
    for t in transmitters:
        freq_idx = model[freq_vars[t]].as_long()
        freq_val = frequencies[freq_idx][0]
        cost = frequencies[freq_idx][2]
        total_cost_value += cost
        print(f"  {t}: frequency {freq_val} (cost {cost})")
    print(f"Total cost: {total_cost_value}")
    print(f"Expected minimum cost: 200")
    if total_cost_value == 200:
        print("SUCCESS: Found optimal solution with cost 200")
    else:
        print(f"Note: Found solution with cost {total_cost_value}, expected 200")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")