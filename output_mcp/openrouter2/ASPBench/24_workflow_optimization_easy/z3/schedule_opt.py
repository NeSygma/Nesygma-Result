from z3 import *

# Problem data
n = 8
# durations
D = [3,2,4,1,5,2,3,2]
# prerequisites list
prereqs = [[], [], [0], [1], [2,3], [0], [4], [5,6]]

solver = Optimize()
# start times
start = [Int(f'start_{i}') for i in range(n)]
# end times
end = [Int(f'end_{i}') for i in range(n)]
# makespan
makespan = Int('makespan')

# constraints
for i in range(n):
    solver.add(start[i] >= 0)
    solver.add(end[i] == start[i] + D[i])
    # prerequisites
    for p in prereqs[i]:
        solver.add(start[i] >= end[p])
    # makespan bounds
    solver.add(makespan >= end[i])

# objective
solver.minimize(makespan)

# solve
result = solver.check()
if result == sat:
    model = solver.model()
    # extract schedule
    schedule = []
    for i in range(n):
        s = model[start[i]].as_long()
        e = model[end[i]].as_long()
        schedule.append((i, s, e))
    # compute makespan
    m = model[makespan].as_long()
    # compute longest path lengths
    # use memoization
    from functools import lru_cache
    @lru_cache(None)
    def longest(i):
        if not prereqs[i]:
            return D[i]
        return D[i] + max(longest(p) for p in prereqs[i])
    # find a task with longest path equal to makespan
    target = None
    for i in range(n):
        if longest(i) == m:
            target = i
            break
    # backtrack to build chain
    critical_path = []
    cur = target
    while cur is not None:
        critical_path.append(cur)
        # find predecessor that satisfies longest(cur) == D[cur] + longest(pred)
        preds = prereqs[cur]
        pred_found = None
        for p in preds:
            if longest(p) + D[cur] == longest(cur):
                pred_found = p
                break
        cur = pred_found
    critical_path = list(reversed(critical_path))
    # output
    print("STATUS: sat")
    print("schedule:")
    for t,s,e in schedule:
        print(f"  task: {t}, start_time: {s}, end_time: {e}")
    print(f"makespan: {m}")
    print("critical_path:")
    print("  ", critical_path)
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")
    else:
        print("RAW_RESULT: unsat")