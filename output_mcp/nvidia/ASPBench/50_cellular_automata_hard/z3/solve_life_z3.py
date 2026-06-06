from z3 import *

N = 14
BENCHMARK_MODE = True

# Array for live cells
live = Array('live', IntSort(), BoolSort())

solver = Solver()

# Pattern top-left variables
r_block = Int('r_block')
c_block = Int('c_block')
r_boat  = Int('r_boat')
c_boat  = Int('c_boat')
r_loaf  = Int('r_loaf')
c_loaf  = Int('c_loaf')

# Offsets
block_offsets = [(0,0),(0,1),(1,0),(1,1)]
boat_offsets  = [(0,0),(0,1),(1,0),(1,2),(2,1)]
loaf_offsets  = [(0,1),(0,2),(1,0),(1,3),(2,1),(2,3),(3,2)]

neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

# Boundary constraints
solver.add(r_block >= 0, c_block >= 0)
solver.add(r_block + 1 < N, c_block + 1 < N)

solver.add(r_boat >= 0, c_boat >= 0)
solver.add(r_boat + 2 < N, c_boat + 2 < N)

solver.add(r_loaf >= 0, c_loaf >= 0)
solver.add(r_loaf + 3 < N, c_loaf + 3 < N)

# Mark pattern cells as live
for dr,dc in block_offsets:
    solver.add(Select(live, (r_block+dr)*N + (c_block+dc)) == True)

for dr,dc in boat_offsets:
    solver.add(Select(live, (r_boat+dr)*N + (c_boat+dc)) == True)

for dr,dc in loaf_offsets:
    solver.add(Select(live, (r_loaf+dr)*N + (c_loaf+dc)) == True)

# Exactly 16 live cells
live_cells = [If(Select(live, i*N + j), 1, 0) for i in range(N) for j in range(N)]
solver.add(Sum(live_cells) == 16)

# Still-life constraints
for i in range(N):
    for j in range(N):
        cell = Select(live, i*N + j)
        # neighbor bools
        neighbor_bools = []
        for dx,dy in neighbors:
            ni, nj = i+dx, j+dy
            if 0 <= ni < N and 0 <= nj < N:
                nbr = Select(live, ni*N + nj)
                neighbor_bools.append(If(nbr, 1, 0))
        neighbor_sum = Sum(neighbor_bools)
        solver.add(Implies(cell, Or(neighbor_sum == 2, neighbor_sum == 3)))
        solver.add(Implies(Not(cell), neighbor_sum != 3))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("block at", m[r_block].as_long(), m[c_block].as_long())
    print("boat at",  m[r_boat].as_long(),  m[c_boat].as_long())
    print("loaf at",  m[r_loaf].as_long(),  m[c_loaf].as_long())
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")