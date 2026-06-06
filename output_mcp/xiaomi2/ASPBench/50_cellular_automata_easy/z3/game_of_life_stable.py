from z3 import *

solver = Solver()

ROWS, COLS = 5, 5
MAX_STEPS = 10

# Grid states: grid[t][i][j] is a Bool representing alive/dead at time t
grid = [[[Bool(f'g_{t}_{i}_{j}') for j in range(COLS)] for i in range(ROWS)] for t in range(MAX_STEPS + 1)]

# Initial configuration
initial = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0]
]

# Set initial state (generation 0)
for i in range(ROWS):
    for j in range(COLS):
        solver.add(grid[0][i][j] == (initial[i][j] == 1))

# Neighbor count: count alive neighbors for cell (i,j) at time t
# Out-of-bounds cells are treated as dead (finite grid, no wrapping)
def neighbor_count(t, i, j):
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS:
                neighbors.append(If(grid[t][ni][nj], 1, 0))
    return Sum(neighbors)

# Apply Conway's Game of Life rules for each transition t -> t+1
for t in range(MAX_STEPS):
    for i in range(ROWS):
        for j in range(COLS):
            nc = neighbor_count(t, i, j)
            alive = grid[t][i][j]
            # Rule: alive cell with 2-3 neighbors survives; dead cell with exactly 3 is born
            next_state = Or(
                And(alive, Or(nc == 2, nc == 3)),
                And(Not(alive), nc == 3)
            )
            solver.add(grid[t+1][i][j] == next_state)

# Solve - the simulation is deterministic, so there's exactly one valid model
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract all generation states from the model
    states = []
    for t in range(MAX_STEPS + 1):
        state = []
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                val = model.evaluate(grid[t][i][j], model_completion=True)
                row.append(1 if is_true(val) else 0)
            state.append(row)
        states.append(state)
    
    # Print all generations for context
    print("=== All Generations ===")
    for t, s in enumerate(states):
        print(f"Generation {t}:")
        for row in s:
            print(f"  {row}")
    
    # Cycle detection: find the first (t1, t2) pair where t1 < t2 and states match
    # "First" means smallest t1, then smallest period (t2 - t1)
    cycle_found = False
    for t2 in range(1, MAX_STEPS + 1):
        for t1 in range(t2):
            if states[t1] == states[t2]:
                period = t2 - t1
                cycle_states = states[t1:t2]  # states from t1 to t2-1
                
                print("\n=== Stable Pattern Found ===")
                print("STATUS: sat")
                print(f"pattern_id: 1")
                print(f"period: {period}")
                print(f"cycle_start_generation: {t1}")
                print(f"cycle_end_generation: {t2}")
                print(f"stable_patterns:")
                print(f"  - pattern_id: 1")
                print(f"    period: {period}")
                print(f"    states:")
                for idx, s in enumerate(cycle_states):
                    gen = t1 + idx
                    print(f"      - generation_{gen}:")
                    for row in s:
                        print(f"          {row}")
                
                cycle_found = True
                break
        if cycle_found:
            break
    
    if not cycle_found:
        print("\nSTATUS: sat")
        print("No cycle detected within 10 generations")
        print("The pattern does not stabilize within the simulation window.")

elif result == unknown:
    print("STATUS: unknown")
    print("Z3 returned unknown - simulation could not be completed")
else:
    print("STATUS: unsat")
    print("Simulation constraints are unsatisfiable (unexpected)")