from z3 import *

# Grid size
N = 14

# Pattern shapes as list of (dr, dc)
block_shape = [(0,0),(0,1),(1,0),(1,1)]
boat_shape = [(0,0),(0,1),(1,0),(1,2),(2,1)]
loaf_shape = [(0,1),(0,2),(1,0),(1,3),(2,1),(2,3),(3,2)]

# Variables for top-left corners (row, col) of each pattern
br, bc = Ints('br bc')
boatr, boatc = Ints('boatr boatc')
loafr, loafc = Ints('loafr loafc')

solver = Solver()

# Boundary constraints
solver.add(br >= 0, br <= N - 2)  # block height 2
solver.add(bc >= 0, bc <= N - 2)
solver.add(boatr >= 0, boatr <= N - 3)  # boat height 3
solver.add(boatc >= 0, boatc <= N - 3)
solver.add(loafr >= 0, loafr <= N - 4)  # loaf height 4
solver.add(loafc >= 0, loafc <= N - 4)

# Create Bool matrices for each cell
cells = [[Bool(f'c_{i}_{j}') for j in range(N)] for i in range(N)]
block_here = [[Bool(f'block_{i}_{j}') for j in range(N)] for i in range(N)]
boat_here = [[Bool(f'boat_{i}_{j}') for j in range(N)] for i in range(N)]
loaf_here = [[Bool(f'loaf_{i}_{j}') for j in range(N)] for i in range(N)]

# Define occupancy predicates
for i in range(N):
    for j in range(N):
        # block occupancy
        block_cases = []
        for dr, dc in block_shape:
            block_cases.append(And(br == i - dr, bc == j - dc))
        solver.add(block_here[i][j] == Or(block_cases))
        # boat occupancy
        boat_cases = []
        for dr, dc in boat_shape:
            boat_cases.append(And(boatr == i - dr, boatc == j - dc))
        solver.add(boat_here[i][j] == Or(boat_cases))
        # loaf occupancy
        loaf_cases = []
        for dr, dc in loaf_shape:
            loaf_cases.append(And(loafr == i - dr, loafc == j - dc))
        solver.add(loaf_here[i][j] == Or(loaf_cases))
        # No overlap: at most one pattern occupies a cell
        solver.add(If(block_here[i][j], 1, 0) + If(boat_here[i][j], 1, 0) + If(loaf_here[i][j], 1, 0) <= 1)
        # cell is live if any pattern occupies it
        solver.add(cells[i][j] == Or(block_here[i][j], boat_here[i][j], loaf_here[i][j]))

# Neighbor constraints for still life
for i in range(N):
    for j in range(N):
        # collect neighbor cells
        neigh = []
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < N and 0 <= nj < N:
                    neigh.append(cells[ni][nj])
        live_neighbors = Sum([If(c, 1, 0) for c in neigh])
        # still life constraints
        solver.add(Implies(cells[i][j], Or(live_neighbors == 2, live_neighbors == 3)))
        solver.add(Implies(Not(cells[i][j]), live_neighbors != 3))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("block_top_left = (", m[br].as_long(), ",", m[bc].as_long(), ")")
    print("boat_top_left = (", m[boatr].as_long(), ",", m[boatc].as_long(), ")")
    print("loaf_top_left = (", m[loafr].as_long(), ",", m[loafc].as_long(), ")")
    # Optionally print grid
    grid = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if is_true(m.eval(cells[i][j])):
                grid[i][j] = 1
    print("grid:")
    for row in grid:
        print(''.join(str(v) for v in row))
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")