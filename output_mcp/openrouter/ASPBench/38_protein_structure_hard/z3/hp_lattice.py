from z3 import *

# Protein sequence length
n = 10
seq = "HPHPHHPHPH"
# Identify hydrophobic positions (0-indexed)
h_positions = [i for i, c in enumerate(seq) if c == 'H']

# Variables for coordinates
xs = [Int(f'x_{i}') for i in range(n)]
ys = [Int(f'y_{i}') for i in range(n)]

opt = Optimize()

# Bounds to keep search finite (max Manhattan distance from start <= n)
BOUND = n
for i in range(n):
    opt.add(xs[i] >= -BOUND, xs[i] <= BOUND)
    opt.add(ys[i] >= -BOUND, ys[i] <= BOUND)

# Self-avoiding: all positions distinct
for i in range(n):
    for j in range(i+1, n):
        opt.add(Or(xs[i] != xs[j], ys[i] != ys[j]))

# Connectivity: consecutive residues adjacent (Manhattan distance = 1)
for i in range(n-1):
    opt.add(Abs(xs[i] - xs[i+1]) + Abs(ys[i] - ys[i+1]) == 1)

# Energy: -1 for each non-sequential H-H adjacent pair
energy_terms = []
for i in range(n):
    for j in range(i+2, n):  # |i-j| > 1 ensures non-sequential
        if seq[i] == 'H' and seq[j] == 'H':
            adj = (Abs(xs[i] - xs[j]) + Abs(ys[i] - ys[j]) == 1)
            # If adjacent, contributes -1
            energy_terms.append(If(adj, -1, 0))

energy = Sum(energy_terms) if energy_terms else IntVal(0)
opt.minimize(energy)

result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    # Compute energy value from model (should match minimized)
    ev = m.eval(energy, model_completion=True)
    print("energy =", ev)
    for i in range(n):
        print(f"residue_{i+1} ({seq[i]}): ({m[xs[i]]}, {m[ys[i]]})")
else:
    print("STATUS: unsat")