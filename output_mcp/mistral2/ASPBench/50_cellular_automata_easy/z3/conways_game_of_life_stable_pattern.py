from z3 import *

# BENCHMARK_MODE: OFF (since unsat is a valid result for simulation)
BENCHMARK_MODE = False

def count_neighbors(grid, t, i, j):
    """Count the number of live neighbors for cell (i, j) at generation t."""
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue  # Skip the cell itself
            ni, nj = i + di, j + dj
            if 0 <= ni < 5 and 0 <= nj < 5:
                count += grid[t][ni][nj]
    return count

def next_generation(grid, t):
    """Compute the next generation of the grid."""
    new_grid = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            neighbors = count_neighbors(grid, t, i, j)
            if grid[t][i][j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = 0  # Dies
                else:
                    new_grid[i][j] = 1  # Survives
            else:
                if neighbors == 3:
                    new_grid[i][j] = 1  # Reproduction
                else:
                    new_grid[i][j] = 0  # Stays dead
    return new_grid

def simulate_until_stable(initial_grid, max_generations=10):
    """Simulate the grid until a stable pattern (cycle) is found."""
    grid = [initial_grid]
    seen = {}
    for t in range(1, max_generations + 1):
        next_grid = next_generation(grid, t - 1)
        grid.append(next_grid)
        # Convert grid to a tuple of tuples for hashing
        grid_tuple = tuple(tuple(row) for row in next_grid)
        if grid_tuple in seen:
            # Cycle detected
            first_occurrence = seen[grid_tuple]
            period = t - first_occurrence
            states = grid[first_occurrence:t]
            return {
                "pattern_id": 1,
                "period": period,
                "states": states,
            }
        seen[grid_tuple] = t
    return None  # No stable pattern found within max_generations

# Initial 5x5 grid configuration
initial_grid = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0]
]

# Simulate and find the first stable pattern
result = simulate_until_stable(initial_grid)

if result:
    print("STATUS: sat")
    print(f"pattern_id: {result['pattern_id']}")
    print(f"period: {result['period']}")
    print("states:")
    for state in result['states']:
        for row in state:
            print(row)
        print()  # Separate states
else:
    print("STATUS: unsat")
    print("No stable pattern found within 10 generations.")