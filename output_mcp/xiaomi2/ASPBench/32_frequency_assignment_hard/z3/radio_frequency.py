from z3 import *

# Transmitters
transmitters = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10']

# Frequencies with costs
freq_costs = {101: 10, 102: 12, 103: 15, 201: 20, 202: 22, 203: 25, 204: 28, 301: 40, 302: 45}

# All frequencies
all_freqs = sorted(freq_costs.keys())

# Band restrictions: Low={101,102,103}, Mid={201,202,203,204}, High={301,302}
allowed = {
    't1': [101, 102, 103],
    't2': [101, 102, 103],
    't3': [201, 202, 203, 204],
    't4': [201, 202, 203, 204],
    't5': [201, 202, 203, 204],
    't6': [301, 302],
    't7': [101, 102, 103, 201, 202, 203, 204],
    't8': [101, 102, 103, 201, 202, 203, 204],
    't9': [201, 202, 203, 204, 301, 302],
    't10': [201, 202, 203, 204, 301, 302],
}

# Interference pairs
interference = [
    ('t1', 't2'), ('t1', 't7'), ('t2', 't8'),
    ('t3', 't4'), ('t3', 't9'), ('t4', 't5'),
    ('t4', 't7'), ('t5', 't8'), ('t5', 't10'),
    ('t6', 't9'), ('t6', 't10')
]

# Create optimizer
opt = Optimize()

# Decision variables: frequency assigned to each transmitter
freq = {t: Int(f'freq_{t}') for t in transmitters}

# Constraint 1: Band restriction - each transmitter gets a frequency from allowed bands
for t in transmitters:
    opt.add(Or([freq[t] == f for f in allowed[t]]))

# Constraints 2 & 3: Interference constraints
for (ta, tb) in interference:
    fa, fb = freq[ta], freq[tb]
    
    # Determine if same band: band = freq // 100 (1=Low, 2=Mid, 3=High)
    same_band = (fa / 100 == fb / 100)
    
    # Same-band interference: frequencies must differ by more than 1
    same_band_ok = Or(fa - fb > 1, fb - fa > 1)
    
    # Cross-band interference: cannot use the same frequency value
    # (201 and 301 are different values, so they don't conflict)
    cross_band_ok = (fa != fb)
    
    opt.add(If(same_band, same_band_ok, cross_band_ok))

# Objective: minimize total licensing cost
total_cost = Sum([If(freq[t] == f, freq_costs[f], 0) 
                  for t in transmitters for f in all_freqs])
opt.minimize(total_cost)

# Solve
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    total = 0
    assignments = []
    for t in transmitters:
        f = m.evaluate(freq[t]).as_long()
        c = freq_costs[f]
        total += c
        assignments.append((t, f, c))
        print(f"  {t} -> frequency {f} (cost {c})")
    print(f"\nTotal cost: {total}")
    
    # Output in expected format
    print("\n--- Structured Output ---")
    print("assignments:")
    for t, f, c in assignments:
        print(f'  {{"transmitter": "{t}", "frequency": {f}}}')
    print(f"total_cost: {total}")
    
    # Verify constraints
    print("\n--- Verification ---")
    for (ta, tb) in interference:
        fa = m.evaluate(freq[ta]).as_long()
        fb = m.evaluate(freq[tb]).as_long()
        band_a = fa // 100
        band_b = fb // 100
        if band_a == band_b:
            diff = abs(fa - fb)
            status = "OK" if diff > 1 else "VIOLATION"
            print(f"  ({ta},{tb}): same band, |{fa}-{fb}|={diff} -> {status}")
        else:
            status = "OK" if fa != fb else "VIOLATION"
            print(f"  ({ta},{tb}): cross band, {fa}!={fb} -> {status}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")