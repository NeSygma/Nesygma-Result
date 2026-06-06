from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Declare grid over time: grid[t][i][j] for t in 0..10, i in 0..4, j in 0..4
# We use 11 steps (0 to 10) to allow cycle detection within 10 steps
T = 10  # max time steps to simulate
N = 5  # grid size

# Create 3D list of Z3 integers for the grid
grid = [[[Int(f"grid_{t}_{i}_{j}") for j in range(N)] for i in range(N)] for t in range(T+1)]

# Helper: Define neighbors for cell (i,j) at time t-1
# We need to access grid[t-1][i][j] for neighbors
def get_neighbors(t, i, j):
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N:
                neighbors.append(grid[t-1][ni][nj])
    return neighbors

# Set initial state (t=0)
initial = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0]
]
for i in range(N):
    for j in range(N):
        solver.add(grid[0][i][j] == initial[i][j])

# Enforce Game of Life rules for each time step from 1 to T
for t in range(1, T+1):
    for i in range(N):
        for j in range(N):
            neighbors = get_neighbors(t, i, j)
            live_neighbors = Sum(neighbors)
            current = grid[t][i][j]
            prev = grid[t-1][i][j]
            
            # Rule 1: Living cell with < 2 neighbors dies
            # Rule 2: Living cell with 2-3 neighbors survives
            # Rule 3: Living cell with > 3 neighbors dies
            # Rule 4: Dead cell with exactly 3 neighbors becomes alive
            
            # If previous cell was alive:
            solver.add(Implies(prev == 1, 
                               Or(And(live_neighbors == 2, current == 1),
                                  And(live_neighbors == 3, current == 1),
                                  And(Or(live_neighbors < 2, live_neighbors > 3), current == 0))))
            # If previous cell was dead:
            solver.add(Implies(prev == 0,
                               If(live_neighbors == 3, current == 1, current == 0)))

# Check for satisfiability (simulate the grid)
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract all states as tuples of tuples for cycle detection
    states = []
    for t in range(T+1):
        state = []
        for i in range(N):
            row = []
            for j in range(N):
                val = model[grid[t][i][j]]
                row.append(int(val.as_long()))
            state.append(tuple(row))
        states.append(tuple(state))
    
    # Detect the first cycle (smallest period > 0 such that states[i] == states[i+period])
    cycle_info = None
    for i in range(len(states)):
        for period in range(1, len(states) - i):
            if i + period >= len(states):
                break
            if states[i] == states[i + period]:
                # Extract the cycle: from i to i+period-1
                cycle_states = list(states[i:i+period])
                cycle_info = (i, period, cycle_states)
                break
        if cycle_info is not None:
            break
    
    if cycle_info:
        start_idx, period, cycle_states = cycle_info
        print(f"pattern_id: 1")
        print(f"period: {period}")
        print("states:")
        for idx, state in enumerate(cycle_states):
            print(f"  State {idx}:")
            for row in state:
                print(f"    {list(row)}")
    else:
        print("No cycle found in the simulated states.")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")