from z3 import *

# Data
N = 8
durations = [3,2,4,1,5,2,3,2]
prereqs = [
    [],        # 0
    [],        # 1
    [0],       # 2
    [1],       # 3
    [2,3],     # 4
    [0],       # 5
    [4],       # 6
    [5,6]      # 7
]

# Variables
starts = [Int(f'start_{i}') for i in range(N)]
ends   = [Int(f'end_{i}')   for i in range(N)]
makespan = Int('makespan')

opt = Optimize()

# Basic constraints
for i in range(N):
    opt.add(starts[i] >= 0)
    opt.add(ends[i] == starts[i] + durations[i])
    for p in prereqs[i]:
        opt.add(starts[i] >= ends[p])

# makespan constraints
for i in range(N):
    opt.add(makespan >= ends[i])

# Objective: minimize makespan
opt.minimize(makespan)

# Solve
if opt.check() == sat:
    m = opt.model()
    ms_val = m.eval(makespan).as_long()
    # Extract start/end values
    start_vals = [m.eval(starts[i]).as_long() for i in range(N)]
    end_vals   = [m.eval(ends[i]).as_long()   for i in range(N)]
    # Compute longest path lengths (DP)
    longest = [0]*N
    order = list(range(N))  # tasks are already topologically sorted by IDs given dependencies
    for i in order:
        if not prereqs[i]:
            longest[i] = durations[i]
        else:
            longest[i] = durations[i] + max(longest[p] for p in prereqs[i])
    # Identify a task that achieves makespan on longest path
    end_task = None
    for i in range(N):
        if longest[i] == ms_val:
            end_task = i
            break
    # Reconstruct critical path backwards
    critical = []
    cur = end_task
    while cur is not None:
        critical.append(cur)
        if not prereqs[cur]:
            break
        # choose predecessor that satisfies longest[p] == longest[cur] - durations[cur]
        found = None
        for p in prereqs[cur]:
            if longest[p] == longest[cur] - durations[cur]:
                found = p
                break
        cur = found
    critical_path = list(reversed(critical))
    # Output
    print("STATUS: sat")
    print(f"makespan = {ms_val}")
    for i in range(N):
        print(f"task {i}: start_time = {start_vals[i]}, end_time = {end_vals[i]}")
    print("critical_path =", critical_path)
else:
    print("STATUS: unsat")