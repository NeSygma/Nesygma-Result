from z3 import *

# Problem data
n = 10
# durations
duration = [4,3,5,2,6,3,4,5,2,3]
# eligible machines per task
eligible = [[1],[2],[3],[1],[2],[1],[3],[2],[1],[2,3]]
# prerequisites per task
prereq = [[],[],[],[0],[1],[3],[2,4],[4],[5],[7,8]]

solver = Optimize()
# Variables
start = [Int(f'start_{i}') for i in range(n)]
end = [Int(f'end_{i}') for i in range(n)]
machine = [Int(f'machine_{i}') for i in range(n)]
makespan = Int('makespan')

# Constraints
for i in range(n):
    solver.add(start[i] >= 0)
    solver.add(end[i] == start[i] + duration[i])
    # machine eligibility
    solver.add(Or([machine[i] == m_id for m_id in eligible[i]]))
    # precedence
    for p in prereq[i]:
        solver.add(start[i] >= end[p])

# Non-overlap on same machine
for i in range(n):
    for j in range(i+1, n):
        solver.add(Implies(machine[i] == machine[j], Or(end[i] <= start[j], end[j] <= start[i])))

# Makespan constraints
for i in range(n):
    solver.add(makespan >= end[i])

# Objective
solver.minimize(makespan)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    # Extract values
    start_vals = [model[start[i]].as_long() for i in range(n)]
    end_vals = [model[end[i]].as_long() for i in range(n)]
    machine_vals = [model[machine[i]].as_long() for i in range(n)]
    makespan_val = model[makespan].as_long()

    # Compute critical path: backtrack from a task that ends at makespan
    # Find any task with end == makespan
    candidate_tasks = [i for i in range(n) if end_vals[i] == makespan_val]
    if not candidate_tasks:
        # fallback: choose task with max end
        candidate_tasks = [max(range(n), key=lambda i: end_vals[i])]
    # choose smallest id for determinism
    end_task = min(candidate_tasks)
    # backtrack
    critical_path_rev = [end_task]
    cur = end_task
    while True:
        # find a predecessor that satisfies end[pre] + duration[pre] == start[cur]
        preds = prereq[cur]
        found = None
        for p in preds:
            if end_vals[p] + duration[p] == start_vals[cur]:
                if found is None or p < found:
                    found = p
        if found is None:
            break
        critical_path_rev.append(found)
        cur = found
    critical_path = list(reversed(critical_path_rev))

    # Output
    print("STATUS: sat")
    print(f"makespan: {makespan_val}")
    print("schedule:")
    for i in range(n):
        print(f"{i} machine={machine_vals[i]} start={start_vals[i]} end={end_vals[i]}")
    print("critical_path: " + " ".join(str(x) for x in critical_path))
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")