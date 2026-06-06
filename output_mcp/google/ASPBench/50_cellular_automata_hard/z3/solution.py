from z3 import *

def solve():
    solver = Solver()
    
    # Grid size
    N = 14
    
    # Grid variables
    grid = [[Bool(f'grid_{r}_{c}') for c in range(N)] for r in range(N)]
    
    # Pattern top-left positions
    # Block: 2x2
    rb, cb = Int('rb'), Int('cb')
    # Boat: 3x3
    ro, co = Int('ro'), Int('co')
    # Loaf: 4x4
    rl, cl = Int('rl'), Int('cl')
    
    # Bounds
    solver.add(rb >= 0, rb <= N-2, cb >= 0, cb <= N-2)
    solver.add(ro >= 0, ro <= N-3, co >= 0, co <= N-3)
    solver.add(rl >= 0, rl <= N-4, cl >= 0, cl <= N-4)
    
    # Define pattern cells
    def get_block_cells(r, c):
        return [(r+0, c+0), (r+0, c+1), (r+1, c+0), (r+1, c+1)]
    
    def get_boat_cells(r, c):
        return [(r+0, c+0), (r+0, c+1), (r+1, c+0), (r+1, c+2), (r+2, c+1)]
    
    def get_loaf_cells(r, c):
        return [(r+0, c+1), (r+0, c+2), (r+1, c+0), (r+1, c+3), (r+2, c+1), (r+2, c+3), (r+3, c+2)]
    
    block_cells = get_block_cells(rb, cb)
    boat_cells = get_boat_cells(ro, co)
    loaf_cells = get_loaf_cells(rl, cl)
    
    # No overlap
    all_cells = block_cells + boat_cells + loaf_cells
    for i in range(len(all_cells)):
        for j in range(i + 1, len(all_cells)):
            solver.add(Or(all_cells[i][0] != all_cells[j][0], all_cells[i][1] != all_cells[j][1]))
            
    # Grid mapping
    for r in range(N):
        for c in range(N):
            is_in_block = Or([And(r == br, c == bc) for br, bc in block_cells])
            is_in_boat = Or([And(r == orr, c == oc) for orr, oc in boat_cells])
            is_in_loaf = Or([And(r == lr, c == lc) for lr, lc in loaf_cells])
            solver.add(grid[r][c] == Or(is_in_block, is_in_boat, is_in_loaf))
            
    # Still life conditions
    def get_neighbors(r, c):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    neighbors.append(grid[nr][nc])
        return neighbors

    for r in range(N):
        for c in range(N):
            ns = get_neighbors(r, c)
            n_sum = Sum([If(n, 1, 0) for n in ns])
            
            # If live, 2 or 3 neighbors
            solver.add(Implies(grid[r][c], Or(n_sum == 2, n_sum == 3)))
            # If dead, not 3 neighbors
            solver.add(Implies(Not(grid[r][c]), n_sum != 3))
            
    if solver.check() == sat:
        print("STATUS: sat")
        m = solver.model()
        print(f"Block: ({m[rb]}, {m[cb]})")
        print(f"Boat: ({m[ro]}, {m[co]})")
        print(f"Loaf: ({m[rl]}, {m[cl]})")
    else:
        print("STATUS: unsat")

solve()