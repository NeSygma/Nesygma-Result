from z3 import *

# Problem parameters
T = 10  # Maximum time steps to simulate
N = 5   # Grid size

# Create 3D array of Int variables: grid[t][i][j]
grid = [[[Int(f'grid_{t}_{i}_{j}') for j in range(N)] for i in range(N)] for t in range(T+1)]

solver = Solver()

# Add constraints that all cells are 0 or 1
for t in range(T+1):
    for i in range(N):
        for j in range(N):
            solver.add(Or(grid[t][i][j] == 0, grid[t][i][j] == 1))

# Initial state constraints
initial = [
    [0,1,0,1,0],
    [1,0,1,0,1],
    [0,1,0,1,0],
    [1,0,1,0,1],
    [0,1,0,1,0]
]

for i in range(N):
    for j in range(N):
        solver.add(grid[0][i][j] == initial[i][j])

# Transition constraints for each time step
for t in range(T):
    for i in range(N):
        for j in range(N):
            # Count living neighbors at time t
            neighbors = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < N and 0 <= nj < N:
                        neighbors.append(grid[t][ni][nj])
            
            num_neighbors = Sum(neighbors)
            alive_t = grid[t][i][j]
            alive_t1 = grid[t+1][i][j]
            
            # Game of Life rules:
            # - Living cell with 2-3 neighbors survives
            # - Dead cell with exactly 3 neighbors becomes alive
            # - Otherwise dies/stays dead
            solver.add(alive_t1 == If(alive_t == 1,
                                      If(Or(num_neighbors == 2, num_neighbors == 3), 1, 0),
                                      If(num_neighbors == 3, 1, 0)))

# Check satisfiability
result = solver.check()
if result != sat:
    print("STATUS: unsat")
    print("No valid evolution sequence found")
    exit()

# Extract the model
model = solver.model()

# Get grid values for all time steps
grid_values = []
for t in range(T+1):
    state = []
    for i in range(N):
        row = []
        for j in range(N):
            val = model.evaluate(grid[t][i][j], model_completion=True)
            row.append(int(str(val)))
        state.append(row)
    grid_values.append(state)

# Detect the first cycle
cycle_start = None
cycle_period = None
for t in range(1, T+1):
    for s in range(t):
        if grid_values[t] == grid_values[s]:
            cycle_start = s
            cycle_period = t - s
            break
    if cycle_start is not None:
        break

if cycle_start is None:
    print("STATUS: unknown")
    print("No cycle found within 10 steps")
    exit()

# Extract states in the cycle
cycle_states = grid_values[cycle_start:cycle_start+cycle_period]

# Prepare output
stable_patterns = [{
    'pattern_id': 1,
    'period': cycle_period,
    'states': cycle_states
}]

# Print results
print("STATUS: sat")
print("stable_patterns:", stable_patterns)
print("pattern_id:", stable_patterns[0]['pattern_id'])
print("period:", stable_patterns[0]['period'])
print("states:")
for idx, state in enumerate(cycle_states):
    print(f"  State {idx}:")
    for row in state:
        print(f"    {row}")