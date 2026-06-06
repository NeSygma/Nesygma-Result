from z3 import *

# Mapping pegs to integers
peg_names = ['A', 'B', 'C', 'D']
num_pegs = 4
num_disks = 4
max_steps = 19  # expected optimal moves

solver = Solver()

# Decision variables per step
disk = [Int(f'disk_{t}') for t in range(max_steps)]
from_peg = [Int(f'from_{t}') for t in range(max_steps)]
to_peg = [Int(f'to_{t}') for t in range(max_steps)]

# Position of each disk at each time (including initial time 0 and after each move)
pos = [[Int(f'pos_{d}_{t}') for t in range(max_steps+1)] for d in range(1, num_disks+1)]

# Domain constraints
for t in range(max_steps):
    solver.add(And(disk[t] >= 1, disk[t] <= num_disks))
    solver.add(And(from_peg[t] >= 0, from_peg[t] < num_pegs))
    solver.add(And(to_peg[t] >= 0, to_peg[t] < num_pegs))
    solver.add(from_peg[t] != to_peg[t])

for d in range(num_disks):
    for t in range(max_steps+1):
        solver.add(And(pos[d][t] >= 0, pos[d][t] < num_pegs))

# Initial state: all disks on A (peg 0)
for d in range(num_disks):
    solver.add(pos[d][0] == 0)

# Transition constraints per step
for t in range(max_steps):
    # moving disk must be on its from peg at time t
    solver.add(Select(Array('tmp', IntSort(), IntSort()), 0) == 0)  # dummy to avoid unused warning
    solver.add(And([If(disk[t] == d+1, pos[d][t] == from_peg[t], True) for d in range(num_disks)]))
    # top condition: no smaller disk on same peg as moving disk
    for s in range(num_disks):
        # s is index for smaller disk (size s+1)
        solver.add(Implies(And(disk[t] == s+2,  # moving disk larger than s+1
                               pos[s][t] == from_peg[t]),
                           False))  # cannot have smaller on same peg
    # destination condition: cannot place onto smaller disk
    for s in range(num_disks):
        solver.add(Implies(And(disk[t] == s+1,  # moving disk is size s+1
                               pos[s][t] == to_peg[t]),
                           False))
    # Update positions
    for d in range(num_disks):
        solver.add(If(disk[t] == d+1, pos[d][t+1] == to_peg[t], pos[d][t+1] == pos[d][t]))

# Goal state: all disks on D (peg 3) after last step
for d in range(num_disks):
    solver.add(pos[d][max_steps] == 3)

# Pilgrim's journey: each disk must land on B (1) and C (2) at least once
for d in range(1, num_disks+1):
    landed_on_B = [And(disk[t] == d, to_peg[t] == 1) for t in range(max_steps)]
    landed_on_C = [And(disk[t] == d, to_peg[t] == 2) for t in range(max_steps)]
    solver.add(Or(landed_on_B))
    solver.add(Or(landed_on_C))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print('STATUS: sat')
    # Extract moves
    for t in range(max_steps):
        d_val = m[disk[t]].as_long()
        f_val = m[from_peg[t]].as_long()
        to_val = m[to_peg[t]].as_long()
        print(f'step {t+1}: disk {d_val} from {peg_names[f_val]} to {peg_names[to_val]}')
    print('total_moves =', max_steps)
else:
    print('STATUS: unsat')