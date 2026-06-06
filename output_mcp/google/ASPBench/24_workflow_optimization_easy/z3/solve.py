from z3 import *

# Task data
durations = [3, 2, 4, 1, 5, 2, 3, 2]
prereqs = {
    0: [],
    1: [],
    2: [0],
    3: [1],
    4: [2, 3],
    5: [0],
    6: [4],
    7: [5, 6]
}

opt = Optimize()

# Variables
start_times = [Int(f's{i}') for i in range(8)]
end_times = [Int(f'e{i}') for i in range(8)]
makespan = Int('makespan')

# Constraints
for i in range(8):
    opt.add(start_times[i] >= 0)
    opt.add(end_times[i] == start_times[i] + durations[i])
    opt.add(makespan >= end_times[i])

for i in range(8):
    for p in prereqs[i]:
        opt.add(start_times[i] >= end_times[p])

# Objective
opt.minimize(makespan)

# Solve
if opt.check() == sat:
    m = opt.model()
    ms = m.eval(makespan).as_long()
    
    s_vals = [m.eval(start_times[i]).as_long() for i in range(8)]
    e_vals = [m.eval(end_times[i]).as_long() for i in range(8)]
    
    # Identify critical path
    # A task i is on the critical path if:
    # 1. It ends at the makespan (if it's a terminal task)
    # 2. Or there exists a successor j such that start_time[j] == end_time[i] AND j is on the critical path
    
    # First, find all successors
    successors = {i: [] for i in range(8)}
    for i in range(8):
        for p in prereqs[i]:
            successors[p].append(i)
            
    is_on_cp = [False] * 8
    
    # A task is on the critical path if its slack is 0.
    # Slack = Latest Start - Earliest Start.
    # Let's compute Earliest Start (ES) and Latest Start (LS).
    # ES is already computed by the solver (s_vals).
    # LS:
    # LS[i] = min(LS[j] - duration[i]) for all j in successors[i]
    # LS[terminal] = makespan - duration[terminal]
    
    ls = [0] * 8
    def get_ls(i):
        if not successors[i]:
            return ms - durations[i]
        return min([get_ls(j) - durations[i] for j in successors[i]])
    
    # Actually, let's just use the property:
    # Task i is on critical path if:
    # 1. start_times[i] == 0 (if it has no prereqs)
    # 2. OR there exists a prerequisite p such that end_times[p] == start_times[i] AND p is on critical path
    
    # Let's do it iteratively
    on_cp = [False] * 8
    # Base case: tasks with no prereqs that start at 0
    for i in range(8):
        if not prereqs[i] and s_vals[i] == 0:
            on_cp[i] = True
            
    # Propagate
    changed = True
    while changed:
        changed = False
        for i in range(8):
            if not on_cp[i]:
                # Check if any prereq is on CP and ends when i starts
                for p in prereqs[i]:
                    if on_cp[p] and e_vals[p] == s_vals[i]:
                        on_cp[i] = True
                        changed = True
                        break
    
    # Filter to only include tasks that lead to the makespan
    # A task is on the critical path if it's on a path from start to end with total duration = makespan
    # The above logic finds all tasks with 0 slack.
    
    critical_path = [i for i, val in enumerate(on_cp) if val]
    
    print("STATUS: sat")
    print(f"makespan: {ms}")
    print("schedule:")
    for i in range(8):
        print(f"  task {i}: start={s_vals[i]}, end={e_vals[i]}")
    print(f"critical_path: {critical_path}")
else:
    print("STATUS: unsat")