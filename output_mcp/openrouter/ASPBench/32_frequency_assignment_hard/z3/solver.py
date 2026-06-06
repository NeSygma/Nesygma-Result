from z3 import *

# Transmitters
transmitters = ['t1','t2','t3','t4','t5','t6','t7','t8','t9','t10']

# Frequencies, bands, costs
low_freqs = [101,102,103]
mid_freqs = [201,202,203,204]
high_freqs = [301,302]
all_freqs = low_freqs + mid_freqs + high_freqs

cost_map = {101:10, 102:12, 103:15,
            201:20, 202:22, 203:25, 204:28,
            301:40, 302:45}

# Band mapping function (0=low,1=mid,2=high)
def band_expr(f):
    return If(Or([f == v for v in low_freqs]), 0,
              If(Or([f == v for v in mid_freqs]), 1, 2))

# Allowed frequencies per transmitter
allowed = {
    't1': low_freqs,
    't2': low_freqs,
    't3': mid_freqs,
    't4': mid_freqs,
    't5': mid_freqs,
    't6': high_freqs,
    't7': low_freqs + mid_freqs,
    't8': low_freqs + mid_freqs,
    't9': mid_freqs + high_freqs,
    't10': mid_freqs + high_freqs,
}

# Create variables
freq = {t: Int(f'freq_{t}') for t in transmitters}

opt = Optimize()

# Domain constraints per transmitter
for t in transmitters:
    allowed_vals = allowed[t]
    opt.add(Or([freq[t] == v for v in allowed_vals]))

# Interference pairs
pairs = [('t1','t2'),('t1','t7'),('t2','t8'),('t3','t4'),('t3','t9'),('t4','t5'),('t4','t7'),('t5','t8'),('t5','t10'),('t6','t9'),('t6','t10')]

for a,b in pairs:
    fa = freq[a]
    fb = freq[b]
    ba = band_expr(fa)
    bb = band_expr(fb)
    same_band = ba == bb
    # Same-band interference: difference > 1
    opt.add(Implies(same_band, Abs(fa - fb) > 1))
    # Cross-band interference: cannot be same frequency number
    opt.add(Implies(Not(same_band), fa != fb))

# Cost expression
cost_expr = Sum([If(freq[t] == v, cost_map[v], 0) for t in transmitters for v in all_freqs])
opt.minimize(cost_expr)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    total_cost = m.eval(cost_expr).as_long()
    print("STATUS: sat")
    print("total_cost =", total_cost)
    for t in transmitters:
        print(f"{t} =", m[freq[t]])
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")