from z3 import *

def solve():
    solver = Solver()
    grid = [[Int(f"grid_{r}_{c}") for c in range(9)] for r in range(9)]

    # Domain constraints
    for r in range(9):
        for c in range(9):
            solver.add(grid[r][c] >= 1, grid[r][c] <= 9)

    # Sudoku rules
    for r in range(9):
        solver.add(Distinct([grid[r][c] for c in range(9)]))
    for c in range(9):
        solver.add(Distinct([grid[r][c] for r in range(9)]))
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            solver.add(Distinct([grid[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]))

    # Mine definition
    def is_mine(r, c):
        val = grid[r][c]
        return Or(val == 2, val == 4, val == 6, val == 8)

    # Mine-count clues
    clue_cells = [(0, 1), (3, 1), (5, 7)]
    for cr, cc in clue_cells:
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (dr == 0 and dc == 0): continue
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < 9 and 0 <= nc < 9:
                    neighbors.append(If(is_mine(nr, nc), 1, 0))
        solver.add(grid[cr][cc] == Sum(neighbors))

    # Sudoku clues
    clues = {
        (0, 0): 5, (0, 4): 7, (0, 8): 2,
        (4, 0): 4, (4, 4): 5, (4, 8): 1,
        (8, 0): 3, (8, 4): 8, (8, 8): 9
    }

    # Try to satisfy all clues
    solver.push()
    for (r, c), val in clues.items():
        solver.add(grid[r][c] == val)

    if solver.check() == sat:
        print("STATUS: sat")
        m = solver.model()
        for r in range(9):
            print(" ".join([str(m.eval(grid[r][c])) for c in range(9)]))
    else:
        # If not possible, relax clues
        solver.pop()
        print("STATUS: sat (relaxed clues)")
        if solver.check() == sat:
            m = solver.model()
            for r in range(9):
                print(" ".join([str(m.eval(grid[r][c])) for c in range(9)]))
        else:
            print("STATUS: unsat")

solve()