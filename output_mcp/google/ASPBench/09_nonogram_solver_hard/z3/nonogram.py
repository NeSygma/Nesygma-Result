from z3 import *

def solve_nonogram():
    solver = Solver()
    N = 24
    grid = [[Int(f"grid_{r}_{c}") for c in range(N)] for r in range(N)]

    # Domain constraints
    for r in range(N):
        for c in range(N):
            solver.add(grid[r][c] >= 0, grid[r][c] <= 3)

    row_clues = [
        [(1,10), (2,4), (1,10)], [(1,10), (2,4), (1,10)],
        [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)],
        [(1,2), (3,8), (1,2)], [(1,2), (3,8), (1,2)],
        [(1,2), (2,6), (3,8), (2,6), (1,2)], [(1,2), (2,6), (3,8), (2,6), (1,2)], [(1,2), (2,6), (3,8), (2,6), (1,2)], [(1,2), (2,6), (3,8), (2,6), (1,2)],
        [(1,2), (3,8), (1,2)], [(1,2), (3,8), (1,2)],
        [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)],
        [(1,10), (2,4), (1,10)], [(1,10), (2,4), (1,10)]
    ]

    col_clues = [
        [(1,24)], [(1,24)],
        [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)],
        [(1,2), (3,8), (1,2)], [(1,2), (3,8), (1,2)],
        [(2,8), (3,8), (2,8)], [(2,8), (3,8), (2,8)], [(2,8), (3,8), (2,8)], [(2,8), (3,8), (2,8)],
        [(1,2), (3,8), (1,2)], [(1,2), (3,8), (1,2)],
        [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)], [(1,2), (2,4), (1,2)],
        [(1,24)], [(1,24)]
    ]

    def add_line_constraints(line_vars, clues, line_idx, is_row):
        num_runs = len(clues)
        starts = [Int(f"start_{'r' if is_row else 'c'}_{line_idx}_{j}") for j in range(num_runs)]
        
        # Run position constraints
        for j in range(num_runs):
            color, length = clues[j]
            solver.add(starts[j] >= 0, starts[j] + length <= N)
            if j > 0:
                prev_color, prev_length = clues[j-1]
                # If same color, must be separated by at least one white cell
                if color == prev_color:
                    solver.add(starts[j] >= starts[j-1] + prev_length + 1)
                else:
                    solver.add(starts[j] >= starts[j-1] + prev_length)
        
        # Cell color constraints
        for i in range(N):
            # Cell i is part of run j if starts[j] <= i < starts[j] + length_j
            is_in_run = []
            for j in range(num_runs):
                color, length = clues[j]
                is_in_run.append(And(i >= starts[j], i < starts[j] + length))
                solver.add(Implies(is_in_run[j], line_vars[i] == color))
            
            # If not in any run, must be 0
            solver.add(Implies(Not(Or(is_in_run)), line_vars[i] == 0))

    # Apply row constraints
    for r in range(N):
        add_line_constraints(grid[r], row_clues[r], r, True)
    
    # Apply column constraints
    for c in range(N):
        col_vars = [grid[r][c] for r in range(N)]
        add_line_constraints(col_vars, col_clues[c], c, False)

    # Diagonals
    diag_seq = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
    for i in range(N):
        solver.add(grid[i][i] == diag_seq[i])
        solver.add(grid[i][N-1-i] == diag_seq[i])

    result = solver.check()
    if result == sat:
        print("STATUS: sat")
        m = solver.model()
        for r in range(N):
            row_str = "".join([str(m.evaluate(grid[r][c])) for c in range(N)])
            print(row_str)
    else:
        print("STATUS: unsat")

solve_nonogram()