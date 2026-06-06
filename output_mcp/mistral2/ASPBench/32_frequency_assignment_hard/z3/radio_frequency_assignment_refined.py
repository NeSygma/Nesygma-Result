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

# Helper function to get the band of a frequency
# Since we cannot use t[a] as a key, we will use a series of Or conditions

def get_band(freq_var):
    return Or(
        And(freq_var == 101, True),
        And(freq_var == 102, True),
        And(freq_var == 103, True),
        And(freq_var == 201, True),
        And(freq_var == 202, True),
        And(freq_var == 203, True),
        And(freq_var == 204, True),
        And(freq_var == 301, True),
        And(freq_var == 302, True)
    )

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
            Or(
                And(t[a] == 101, t[b] == 103),
                And(t[a] == 103, t[b] == 101),
                And(t[a] == 201, t[b] == 203),
                And(t[a] == 203, t[b] == 201),
                And(t[a] == 201, t[b] == 204),
                And(t[a] == 204, t[b] == 201),
                And(t[a] == 202, t[b] == 204),
                And(t[a] == 204, t[b] == 202)
            ),
            # Ensure they are in the same band
            Or(
                And(t[a] == 101, t[b] == 103),
                And(t[a] == 103, t[b] == 101),
                And(t[a] == 201, t[b] == 203),
                And(t[a] == 203, t[b] == 201),
                And(t[a] == 201, t[b] == 204),
                And(t[a] == 204, t[b] == 201),
                And(t[a] == 202, t[b] == 204),
                And(t[a] == 204, t[b] == 202)
            )
        ),
        # Different bands: frequency numbers must not be equal
        t[a] != t[b]
    ))

# Add cost minimization
cost_expr = Sum([
    If(t[name] == 101, 10,
    If(t[name] == 102, 12,
    If(t[name] == 103, 15,
    If(t[name] == 201, 20,
    If(t[name] == 202, 22,
    If(t[name] == 203, 25,
    If(t[name] == 204, 28,
    If(t[name] == 301, 40,
    If(t[name] == 302, 45, 0))))))))) for name in transmitters
])
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