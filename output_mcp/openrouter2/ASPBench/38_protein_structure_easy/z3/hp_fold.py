from z3 import *

# Problem parameters
seq = "HPPHPPHH"
N = len(seq)
# Indices of hydrophobic residues
h_indices = [i for i, r in enumerate(seq) if r == 'H']

# Solver
opt = Optimize()

# Coordinate variables
x = [Int(f'x_{i}') for i in range(N)]
 y = [Int(f'y_{i}') for i in range(N)]

# Bounds for coordinates (small lattice)
for i in range(N):
    opt.add(x[i] >= -7, x[i] <= 7)
    opt.add(y[i] >= -7, y[i] <= 7)

# Self-avoiding walk: all coordinates unique
for i in range(N):
    for j in range(i+1, N):
        opt.add(Or(x[i] != x[j], y[i] != y[j]))

# Consecutive residues adjacent (Manhattan distance 1)
for i in range(N-1):
    opt.add(Or(
        And(x[i] == x[i+1], y[i] == y[i+1] + 1),
        And(x[i] == x[i+1], y[i] == y[i+1] - 1),
        And(x[i] == x[i+1] + 1, y[i] == y[i+1]),
        And(x[i] == x[i+1] - 1, y[i] == y[i+1])
    ))

# Contact variables for H-H pairs that are non-sequential neighbors
contact_vars = {}
for idx, i in enumerate(h_indices):
    for j in h_indices[idx+1:]:
        # adjacency condition
        adj = Or(
            And(x[i] == x[j], y[i] == y[j] + 1),
            And(x[i] == x[j], y[i] == y[j] - 1),
            And(x[i] == x[j] + 1, y[i] == y[j]),
            And(x[i] == x[j] - 1, y[i] == y[j])
        )
        # non-sequential: j-i > 1
        non_seq = j - i > 1
        c = Bool(f'c_{i}_{j}')
        opt.add(c == And(adj, non_seq))
        contact_vars[(i,j)] = c

# Sum of contacts
sum_contacts = Sum([If(c, 1, 0) for c in contact_vars.values()])
# Objective: maximize contacts (equivalently minimize energy)
opt.maximize(sum_contacts)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract coordinates
    coords = [(m[x[i]].as_long(), m[y[i]].as_long()) for i in range(N)]
    # Compute number of contacts
    num_contacts = sum(1 for c in contact_vars.values() if is_true(m[c]))
    energy = -num_contacts
    print("STATUS: sat")
    print("sequence:", seq)
    print("coordinates:", coords)
    print("energy:", energy)
else:
    print("STATUS: unsat")
    if result == unknown:
        print("STATUS: unknown")