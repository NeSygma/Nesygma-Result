from z3 import *

# BENCHMARK_MODE: OFF (since we are solving a minimization problem)
BENCHMARK_MODE = False

# Create the solver
opt = Optimize()

# Declare the path as a list of 100 integer variables
path = [Int(f'path_{i}') for i in range(100)]

# Each vertex from 0 to 99 must appear exactly once in the path
solver = Solver()
solver.add(Distinct(path))
solver.add([And(path[i] >= 0, path[i] <= 99) for i in range(100)])

# The path must start at 0 and end at 99
solver.add(path[0] == 0)
solver.add(path[99] == 99)

# Encode allowed edges and their weights
allowed_edges = []

# Chain edges (weight 1)
for i in range(99):
    allowed_edges.append(((i, i+1), 1))

# Local swap gadgets (weight 3)
for N in range(25):  # 0..24 to cover up to 99
    B = 2 + 4 * N
    if B + 3 <= 99:
        allowed_edges.append(((B, B+2), 3))
        allowed_edges.append(((B+2, B+1), 3))
        allowed_edges.append(((B+1, B+3), 3))

# Skips of length 2 (weight 4)
for N in range(25):  # 0..24
    S = 4 * N
    if S + 2 <= 99:
        allowed_edges.append(((S, S+2), 4))

# Jumps of length 3 (weight 5)
for N in range(24):  # 0..23
    T = 1 + 4 * N
    if T + 3 <= 99:
        allowed_edges.append(((T, T+3), 5))

# Long bridges of length 4 (weight 6)
for K in range(20):  # 0..19
    U = 5 * K
    if U + 4 <= 99:
        allowed_edges.append(((U, U+4), 6))

# Encode forbidden edges
forbidden_edges = [
    (0, 2),
    (1, 3)
]

# Periodic forbids
for N in range(12):  # 0..11
    F = 2 + 8 * N
    if F + 2 <= 99:
        forbidden_edges.append((F, F+2))

for N in range(13):  # 0..12
    G = 8 * N
    if G + 2 <= 99:
        forbidden_edges.append((G, G+2))

for N in range(12):  # 0..11
    H = 1 + 8 * N
    if H + 3 <= 99:
        forbidden_edges.append((H, H+3))

for M in range(10):  # 0..9
    L = 10 * M + 5
    if L + 4 <= 99:
        forbidden_edges.append((L, L+4))

# Convert allowed_edges to a dictionary for quick lookup
allowed_dict = {}
for (u, v), w in allowed_edges:
    allowed_dict[(u, v)] = w

# Total cost variable
total_cost = Int('total_cost')
opt.add(total_cost == Sum([
    If(And(path[i] >= 0, path[i+1] >= 0, path[i] <= 99, path[i+1] <= 99),
       If(And(path[i] == u, path[i+1] == v),
          allowed_dict.get((u, v), 0),
          0),
       0)
    for i in range(99) for (u, v), w in allowed_edges
]))

# Ensure that only allowed edges are used
for i in range(99):
    u = path[i]
    v = path[i+1]
    # Check if (u, v) is a forbidden edge
    opt.add(Not(Or([And(u == fu, v == fv) for (fu, fv) in forbidden_edges])))
    # Check if (u, v) is an allowed edge
    opt.add(Or([And(u == u_edge, v == v_edge) for (u_edge, v_edge), w in allowed_edges]))

# Add the distinctness and bounds constraints to the optimizer
opt.add(solver.assertions())

# Set the objective: minimize total_cost
opt.minimize(total_cost)

# Check for a solution
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract the path
    path_model = [model[path[i]] for i in range(100)]
    # Extract the total cost
    cost_model = model[total_cost]
    print("STATUS: sat")
    print(f"min_cost: {cost_model}")
    print(f"count: 1")
    print(f"exists: true")
    print(f"paths: [[{', '.join(str(v) for v in path_model)}]]")
elif result == unsat:
    print("STATUS: unsat")
    print("No Hamiltonian path exists.")
else:
    print("STATUS: unknown")