from z3 import *

# Transmitters
transmitters = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10']

# Frequencies with bands and costs
freqs = {
    101: {'band': 'low', 'cost': 10},
    102: {'band': 'low', 'cost': 12},
    103: {'band': 'low', 'cost': 15},
    201: {'band': 'mid', 'cost': 20},
    202: {'band': 'mid', 'cost': 22},
    203: {'band': 'mid', 'cost': 25},
    204: {'band': 'mid', 'cost': 28},
    301: {'band': 'high', 'cost': 40},
    302: {'band': 'high', 'cost': 45},
}

freq_list = sorted(freqs.keys())

# Band restrictions: allowed bands per transmitter
allowed_bands = {
    't1': ['low'],
    't2': ['low'],
    't3': ['mid'],
    't4': ['mid'],
    't5': ['mid'],
    't6': ['high'],
    't7': ['low', 'mid'],
    't8': ['low', 'mid'],
    't9': ['mid', 'high'],
    't10': ['mid', 'high'],
}

# Interference pairs
interference_pairs = [
    ('t1', 't2'), ('t1', 't7'), ('t2', 't8'),
    ('t3', 't4'), ('t3', 't9'), ('t4', 't5'),
    ('t4', 't7'), ('t5', 't8'), ('t5', 't10'),
    ('t6', 't9'), ('t6', 't10'),
]

# Create Z3 solver with optimization
opt = Optimize()

# Decision variables: frequency assigned to each transmitter
assign = {t: Int(f'assign_{t}') for t in transmitters}

# Constraint 1: Band restrictions - each transmitter must get a frequency from allowed bands
for t in transmitters:
    allowed_freqs = [f for f in freq_list if freqs[f]['band'] in allowed_bands[t]]
    opt.add(Or([assign[t] == f for f in allowed_freqs]))

# Constraint 2 & 3: Interference constraints
for (t1, t2) in interference_pairs:
    f1 = assign[t1]
    f2 = assign[t2]
    
    # Get band of each frequency using symbolic constraints
    # We need to express: if same band, diff > 1; if different bands, freq numbers must differ
    
    # For same-band interference: if both in same band, |f1 - f2| > 1
    # For cross-band interference: if different bands, the frequency numbers must differ
    
    # We'll use the structure of frequencies:
    # Low: 101-103, Mid: 201-204, High: 301-302
    # Band can be determined by: low if 100-199, mid if 200-299, high if 300-399
    
    # Same band condition
    same_band = Or(
        And(f1 >= 100, f1 < 200, f2 >= 100, f2 < 200),  # both low
        And(f1 >= 200, f1 < 300, f2 >= 200, f2 < 300),  # both mid
        And(f1 >= 300, f1 < 400, f2 >= 300, f2 < 400),  # both high
    )
    
    # Different band condition
    diff_band = Not(same_band)
    
    # Same band constraint: frequencies must differ by more than 1
    opt.add(Implies(same_band, Or(f1 - f2 > 1, f2 - f1 > 1)))
    
    # Cross-band constraint: frequency numbers must differ
    # (e.g., can't have 101 and 201 if they interfere, even though different bands)
    opt.add(Implies(diff_band, f1 != f2))

# Objective: minimize total cost
cost_expr = Sum([If(assign[t] == f, freqs[f]['cost'], 0) 
                 for t in transmitters 
                 for f in freq_list])
opt.minimize(cost_expr)

# Check and print results
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    total_cost = 0
    assignments = []
    for t in transmitters:
        f = model[assign[t]].as_long()
        cost = freqs[f]['cost']
        total_cost += cost
        assignments.append((t, f, cost))
        print(f"  {t} -> frequency {f} (band: {freqs[f]['band']}, cost: {cost})")
    
    print(f"\nTotal cost: {total_cost}")
    print(f"Expected minimum cost: 200")
    
    # Verify interference constraints
    print("\nInterference verification:")
    all_ok = True
    for (t1, t2) in interference_pairs:
        f1 = model[assign[t1]].as_long()
        f2 = model[assign[t2]].as_long()
        band1 = freqs[f1]['band']
        band2 = freqs[f2]['band']
        
        if band1 == band2:
            if abs(f1 - f2) <= 1:
                print(f"  VIOLATION: {t1}({f1}) and {t2}({f2}) same band, diff <= 1")
                all_ok = False
            else:
                print(f"  OK: {t1}({f1}) and {t2}({f2}) same band, diff = {abs(f1-f2)} > 1")
        else:
            if f1 == f2:
                print(f"  VIOLATION: {t1}({f1}) and {t2}({f2}) different bands, same freq number")
                all_ok = False
            else:
                print(f"  OK: {t1}({f1}) and {t2}({f2}) different bands, different freq numbers")
    
    if all_ok:
        print("\nAll interference constraints satisfied!")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid assignment exists.")
else:
    print("STATUS: unknown")
    print("Solver returned unknown.")