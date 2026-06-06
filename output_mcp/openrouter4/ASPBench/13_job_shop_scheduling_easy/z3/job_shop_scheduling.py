from z3 import *

opt = Optimize()

# durations[j][op] = duration
durations = [
    [3, 2, 4],
    [2, 5, 1],
    [4, 1, 3]
]

# machines[j][op] = machine index (0,1,2 for m1,m2,m3)
machines = [
    [0, 1, 2],  # job 1: m1, m2, m3
    [1, 0, 2],  # job 2: m2, m1, m3
    [2, 0, 1]   # job 3: m3, m1, m2
]

num_jobs = 3
num_ops = 3

# Start time variables
start = [[Int(f"start_j{j+1}_o{o+1}") for o in range(num_ops)] for j in range(num_jobs)]

# Makespan variable
makespan = Int('makespan')

# Domain: start times non-negative and reasonable upper bound
UB = 50
for j in range(num_jobs):
    for o in range(num_ops):
        opt.add(start[j][o] >= 0)
        opt.add(start[j][o] <= UB)

# Precedence constraints: operations within each job must be sequential
for j in range(num_jobs):
    for o in range(num_ops - 1):
        opt.add(start[j][o] + durations[j][o] <= start[j][o+1])

# Resource constraints: no two operations on same machine overlap
for j1 in range(num_jobs):
    for o1 in range(num_ops):
        for j2 in range(num_jobs):
            for o2 in range(num_ops):
                # Skip same operation
                if j1 == j2 and o1 == o2:
                    continue
                # Only constrain if they use the same machine
                if machines[j1][o1] == machines[j2][o2]:
                    # Either op1 before op2, or op2 before op1
                    opt.add(Or(
                        start[j1][o1] + durations[j1][o1] <= start[j2][o2],
                        start[j2][o2] + durations[j2][o2] <= start[j1][o1]
                    ))

# Makespan definition: makespan >= end time of every operation
for j in range(num_jobs):
    for o in range(num_ops):
        opt.add(makespan >= start[j][o] + durations[j][o])

# Minimize makespan
opt.minimize(makespan)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"makespan = {m[makespan]}")
    print()
    print("Schedule:")
    for j in range(num_jobs):
        for o in range(num_ops):
            s = m[start[j][o]]
            d = durations[j][o]
            mac = machines[j][o] + 1  # 1-indexed
            print(f"  Job {j+1}, Op {o+1}: machine m{mac}, start={s}, end={s+d}")
    print()
    print("Feasible: True")
else:
    print("STATUS: unsat")
    print("No feasible schedule found")