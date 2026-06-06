from z3 import *

# Transmitters
transmitters = ['A', 'B', 'C', 'D', 'E', 'F']

# Available frequencies
freq_range = [1, 2, 3, 4, 5]

# Interference edges (undirected)
interference_pairs = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('B', 'E'),
    ('C', 'D'), ('C', 'F'),
    ('D', 'E'),
    ('E', 'F')
]

# Decision variables: frequency assigned to each transmitter
freq = {t: Int(f'freq_{t}') for t in transmitters}

# Boolean variables: whether each frequency is used
used = {f: Bool(f'used_{f}') for f in freq_range}

opt = Optimize()

# Constraint 1: Each transmitter assigned exactly one frequency from 1-5
for t in transmitters:
    opt.add(Or([freq[t] == f for f in freq_range]))

# Constraint 2 & 3: Interfering transmitters cannot use same or adjacent frequencies
for (t1, t2) in interference_pairs:
    opt.add(Abs(freq[t1] - freq[t2]) >= 2)

# Link used[] to freq[]: frequency f is used iff some transmitter is assigned f
for f in freq_range:
    opt.add(used[f] == Or([freq[t] == f for t in transmitters]))

# Objective: minimize total number of distinct frequencies used
total_used = Sum([If(used[f], 1, 0) for f in freq_range])
opt.minimize(total_used)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print("Optimal solution found:")
    assignments = []
    for t in transmitters:
        f_val = m.evaluate(freq[t], model_completion=True)
        assignments.append((t, int(str(f_val))))
        print(f"  {t} -> frequency {f_val}")
    
    # Count distinct frequencies used
    used_freqs = sorted(set(f for _, f in assignments))
    print(f"\nfrequencies_used = {len(used_freqs)}")
    print(f"Frequencies used: {used_freqs}")
    
    # Verify constraints
    print("\nVerification:")
    for (t1, t2) in interference_pairs:
        f1 = int(str(m.evaluate(freq[t1])))
        f2 = int(str(m.evaluate(freq[t2])))
        diff = abs(f1 - f2)
        status = "OK" if diff >= 2 else "VIOLATION"
        print(f"  {t1}({f1}) vs {t2}({f2}): diff={diff} [{status}]")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")