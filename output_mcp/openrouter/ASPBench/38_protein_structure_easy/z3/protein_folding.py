from z3 import *

# Sequence data
seq = "HPPHPPHH"
N = len(seq)
# Indices of hydrophobic residues
H_indices = [i for i, c in enumerate(seq) if c == 'H']

# Declare coordinate variables
xs = [Int(f'x_{i}') for i in range(N)]
ys = [Int(f'y_{i}') for i in range(N)]

opt = Optimize()

# 1. Distinct positions (self-avoiding)
for i in range(N):
    for j in range(i+1, N):
        opt.add(Or(xs[i] != xs[j], ys[i] != ys[j]))

# 2. Consecutive adjacency (Manhattan distance = 1)
for i in range(N-1):
    opt.add(Abs(xs[i] - xs[i+1]) + Abs(ys[i] - ys[i+1]) == 1)

# 3. Define contact count for H-H non-consecutive neighbors
contact_terms = []
for idx_i in range(len(H_indices)):
    i = H_indices[idx_i]
    for idx_j in range(idx_i+1, len(H_indices)):
        j = H_indices[idx_j]
        # skip sequential neighbors
        if abs(i - j) == 1:
            continue
        # Manhattan distance == 1
        manhattan = Abs(xs[i] - xs[j]) + Abs(ys[i] - ys[j])
        contact = If(manhattan == 1, 1, 0)
        contact_terms.append(contact)

total_contacts = Sum(contact_terms)
# Maximize contacts (i.e., minimize energy = -contacts)
opt.maximize(total_contacts)

# Run optimizer
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract coordinates
    coords = [(m.eval(xs[i]).as_long(), m.eval(ys[i]).as_long()) for i in range(N)]
    # Compute contacts count concretely
    contacts = 0
    for idx_i in range(len(H_indices)):
        i = H_indices[idx_i]
        for idx_j in range(idx_i+1, len(H_indices)):
            j = H_indices[idx_j]
            if abs(i - j) == 1:
                continue
            xi, yi = coords[i]
            xj, yj = coords[j]
            if abs(xi - xj) + abs(yi - yj) == 1:
                contacts += 1
    energy = -contacts
    print("STATUS: sat")
    print("energy =", energy)
    print("coordinates =", coords)
else:
    print("STATUS: unsat")