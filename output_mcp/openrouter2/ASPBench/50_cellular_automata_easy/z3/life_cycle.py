from z3 import *

# Parameters
N = 5
T = 10  # maximum time steps

# Create solver
solver = Optimize()

# State variables: state[t][i][j]
state = [[[Int(f's_{t}_{i}_{j}') for j in range(N)] for i in range(N)] for t in range(T+1)]

# Helper to get neighbor indices
neighbors = {}
for i in range(N):
    for j in range(N):
        neigh = []
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di==0 and dj==0:
                    continue
                ni, nj = i+di, j+dj
                if 0 <= ni < N and 0 <= nj < N:
                    neigh.append((ni,nj))
        neighbors[(i,j)] = neigh

# Initial configuration
init_grid = [
    [0,1,0,1,0],
    [1,0,1,0,1],
    [0,1,0,1,0],
    [1,0,1,0,1],
    [0,1,0,1,0]
]
for i in range(N):
    for j in range(N):
        solver.add(state[0][i][j] == init_grid[i][j])

# Evolution rules
for t in range(T):
    for i in range(N):
        for j in range(N):
            # Count neighbors
            neigh_sum = Sum([If(state[t][ni][nj] == 1, 1, 0) for (ni,nj) in neighbors[(i,j)]])
            cell = state[t][i][j]
            # Next state
            next_cell = If(And(cell == 1, Or(neigh_sum == 2, neigh_sum == 3)), 1,
                           If(And(cell == 0, neigh_sum == 3), 1, 0))
            solver.add(state[t+1][i][j] == next_cell)

# Cycle detection variables
# t1: first occurrence of a state that repeats later
# t2: later occurrence of the same state
# 0 <= t1 < t2 <= T

# Define Int variables
T1 = Int('t1')
T2 = Int('t2')
solver.add(T1 >= 0, T1 <= T)
solver.add(T2 > T1, T2 <= T)

# No repetition before t1
for i in range(T+1):
    for j in range(i+1, T1):  # j < t1
        # For all pairs i<j< t1, ensure states differ
        # We need to add constraint that there exists a cell where they differ
        diff = Or([state[i][a][b] != state[j][a][b] for a in range(N) for b in range(N)])
        solver.add(diff)

# State at t1 equals state at t2
for a in range(N):
    for b in range(N):
        solver.add(state[T1][a][b] == state[T2][a][b])

# Optimize to minimize t1
solver.minimize(T1)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    t1 = m[T1].as_long()
    t2 = m[T2].as_long()
    period = t2 - t1
    # Extract states from t1 to t2-1
    states = []
    for t in range(t1, t2):
        grid = []
        for i in range(N):
            row = []
            for j in range(N):
                val = m[state[t][i][j]].as_long()
                row.append(val)
            grid.append(row)
        states.append(grid)
    # Output
    print("STATUS: sat")
    print("stable_patterns = [")
    print("  {")
    print("    'pattern_id': 1,")
    print(f"    'period': {period},")
    print("    'states': [")
    for grid in states:
        print("      [")
        for row in grid:
            print("        " + str(row) + ",")
        print("      ],")
    print("    ]")
    print("  }")
    print("]")
else:
    print("STATUS: unsat")
    if result == unknown:
        print("STATUS: unknown")