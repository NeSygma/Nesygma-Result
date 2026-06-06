from z3 import *
import itertools

def solve_nonogram():
    # Grid size
    N = 5
    
    # Grid variables
    grid = [[Int(f'grid_{i}_{j}') for j in range(N)] for i in range(N)]
    
    solver = Solver()
    
    # Constraint 1: Grid values are 0 or 1
    for i in range(N):
        for j in range(N):
            solver.add(Or(grid[i][j] == 0, grid[i][j] == 1))
            
    # Helper function to check clues for a line (row or column)
    def check_line(line, clues, n):
        # Generate all possible valid configurations for the line
        possible_configs = []
        for p in itertools.product([0, 1], repeat=n):
            # Check if p satisfies clues
            groups = []
            current_group = 0
            for val in p:
                if val == 1:
                    current_group += 1
                else:
                    if current_group > 0:
                        groups.append(current_group)
                    current_group = 0
            if current_group > 0:
                groups.append(current_group)
            
            if groups == clues:
                possible_configs.append(p)
        
        # The line must match one of the possible_configs
        solver.add(Or([And([line[i] == config[i] for i in range(n)]) for config in possible_configs]))

    # Row clues
    row_clues = [
        [2],
        [1],
        [3],
        [1, 1],
        [2]
    ]
    for i in range(N):
        check_line(grid[i], row_clues[i], N)
        
    # Column clues
    col_clues = [
        [1, 1],
        [1, 3],
        [2],
        [1],
        [1]
    ]
    for j in range(N):
        col = [grid[i][j] for i in range(N)]
        check_line(col, col_clues[j], N)
        
    result = solver.check()
    if result == sat:
        print("STATUS: sat")
        m = solver.model()
        for i in range(N):
            row_vals = [str(m.eval(grid[i][j])) for j in range(N)]
            print(" ".join(row_vals))
    else:
        print("STATUS: unsat")

solve_nonogram()