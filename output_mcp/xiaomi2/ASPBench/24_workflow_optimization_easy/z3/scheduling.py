from z3 import *

# Task data
durations = [3, 2, 4, 1, 5, 2, 3, 2]
prerequisites = {
    0: [],
    1: [],
    2: [0],
    3: [1],
    4: [2, 3],
    5: [0],
    6: [4],
    7: [5, 6]
}

n = 8

opt = Optimize()

# Start and end times for each task
start = [Int(f'start_{i}') for i in range(n)]
end = [Int(f'end_{i}') for i in range(n)]
makespan = Int('makespan')

# 1. Non-negative start times and end = start + duration
for i in range(n):
    opt.add(start[i] >= 0)
    opt.add(end[i] == start[i] + durations[i])

# 2. Precedence constraints: task cannot start until all prerequisites finish
for i in range(n):
    for p in prerequisites[i]:
        opt.add(start[i] >= end[p])

# 3. Makespan is the max end time
for i in range(n):
    opt.add(makespan >= end[i])

# Objective: minimize makespan
opt.minimize(makespan)

result = opt.check()
if result == sat:
    m = opt.model()
    ms = m[makespan].as_long()
    print("STATUS: sat")
    print(f"makespan = {ms}")
    
    # Print schedule
    schedule = []
    for i in range(n):
        s = m[start[i]].as_long()
        e = m[end[i]].as_long()
        schedule.append((i, s, e))
        print(f"Task {i}: start={s}, end={e}, duration={durations[i]}")
    
    # Find critical path: the longest dependency chain
    # A task is on the critical path if it has zero slack
    # slack[i] = latest_start[i] - earliest_start[i]
    # We compute latest start times by working backward from makespan
    
    # First, let's find the critical path by identifying tasks with zero slack
    # Latest start for task i = min(latest_start[j] for j in successors of i) - duration[i]
    # If no successors, latest_start[i] = makespan - duration[i]
    
    # Build successor map
    successors = {i: [] for i in range(n)}
    for i in range(n):
        for p in prerequisites[i]:
            successors[p].append(i)
    
    # Compute latest start times
    latest_start = [0] * n
    # Topological order for backward pass
    topo_order = []
    visited = [False] * n
    def dfs(u):
        visited[u] = True
        for s in successors[u]:
            if not visited[s]:
                dfs(s)
        topo_order.append(u)
    for i in range(n):
        if not visited[i]:
            dfs(i)
    # topo_order is in reverse topological order (sinks first)
    
    for i in topo_order:
        if not successors[i]:
            latest_start[i] = ms - durations[i]
        else:
            latest_start[i] = min(latest_start[s] - durations[i] for s in successors[i])
    
    # Critical tasks: start == latest_start (zero slack)
    critical_tasks = []
    for i in range(n):
        s_val = m[start[i]].as_long()
        if s_val == latest_start[i]:
            critical_tasks.append(i)
    
    # Find the critical path (longest chain among critical tasks)
    # Build the critical path by following dependencies among critical tasks
    # Start from the task(s) that end at makespan
    critical_set = set(critical_tasks)
    
    # Find all paths through critical tasks and pick the longest
    def find_critical_paths():
        paths = []
        def dfs_path(node, path):
            if node in critical_set:
                path = path + [node]
            else:
                path = path
            # Find critical predecessors
            crit_preds = [p for p in prerequisites[node] if p in critical_set]
            if not crit_preds:
                paths.append(path)
            else:
                for p in crit_preds:
                    dfs_path(p, path)
        # Start from tasks ending at makespan
        for i in critical_tasks:
            if m[end[i]].as_long() == ms:
                dfs_path(i, [])
        return paths
    
    paths = find_critical_paths()
    # Pick the longest path
    if paths:
        crit_path = max(paths, key=len)
        # Reverse to get start-to-end order
        crit_path.reverse()
    else:
        crit_path = critical_tasks
    
    print(f"critical_path = {crit_path}")
    
    # Verify
    print(f"\nVerification:")
    print(f"  Expected makespan: 17")
    print(f"  Computed makespan: {ms}")
    print(f"  Match: {ms == 17}")
else:
    print("STATUS: unsat")
    print("No solution found")