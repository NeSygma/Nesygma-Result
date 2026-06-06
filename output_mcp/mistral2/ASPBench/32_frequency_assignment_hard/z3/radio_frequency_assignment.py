from z3 import *

# Initialize the optimizer
opt = Optimize()

# Transmitter variables
transmitters = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10']
t = {name: Int(name) for name in transmitters}

# Frequency options and their costs
frequencies = {
    101: 10,
    102: 12,
    103: 15,
    201: 20,
    202: 22,
    203: 25,
    204: 28,
    301: 40,
    302: 45
}

# Band restrictions
low_only = ['t1', 't2']
mid_only = ['t3', 't4', 't5']
high_only = ['t6']
low_or_mid = ['t7', 't8']
mid_or_high = ['t9', 't10']

# Interference pairs
interference_pairs = [
    ('t1', 't2'),
    ('t1', 't7'),
    ('t2', 't8'),
    ('t3', 't4'),
    ('t3', 't9'),
    ('t4', 't5'),
    ('t4', 't7'),
    ('t5', 't8'),
    ('t5', 't10'),
    ('t6', 't9'),
    ('t6', 't10')
]

# Band mapping for frequencies
band_of_freq = {
    101: 'low',
    102: 'low',
    103: 'low',
    201: 'mid',
    202: 'mid',
    203: 'mid',
    204: 'mid',
    301: 'high',
    302: 'high'
}

# Add band restriction constraints
for name in low_only:
    opt.add(Or(t[name] == 101, t[name] == 102, t[name] == 103))
for name in mid_only:
    opt.add(Or(t[name] == 201, t[name] == 202, t[name] == 203, t[name] == 204))
for name in high_only:
    opt.add(Or(t[name] == 301, t[name] == 302))
for name in low_or_mid:
    opt.add(Or(t[name] == 101, t[name] == 102, t[name] == 103,
               t[name] == 201, t[name] == 202, t[name] == 203, t[name] == 204))
for name in mid_or_high:
    opt.add(Or(t[name] == 201, t[name] == 202, t[name] == 203, t[name] == 204,
               t[name] == 301, t[name] == 302))

# Add interference constraints
for (a, b) in interference_pairs:
    # Same-band interference: frequencies must differ by more than 1
    # Cross-band interference: frequency numbers must not be equal
    opt.add(Or(
        # Same band: frequencies differ by more than 1
        And(
            band_of_freq[t[a]] == band_of_freq[t[b]],
            Or(
                t[a] - t[b] > 1,
                t[b] - t[a] > 1
            )
        ),
        # Different bands: frequency numbers must not be equal
        And(
            band_of_freq[t[a]] != band_of_freq[t[b]],
            t[a] != t[b]
        )
    ))

# Add cost minimization
cost_expr = Sum([frequencies[model.eval(t[name], model_completion=True)] for name in transmitters])
opt.minimize(cost_expr)

# Check for a solution
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    total_cost = 0
    assignments = []
    for name in transmitters:
        freq = model[t[name]]
        cost = frequencies[freq.as_long()]
        total_cost += cost
        assignments.append((name, freq, cost))
    print("STATUS: sat")
    print("Total cost:", total_cost)
    for name, freq, cost in assignments:
        print(f"{name} -> {freq} (cost: {cost})")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")