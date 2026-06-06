from z3 import *

# ============================================================
# Data
# ============================================================
num_tasks = 10
durations = [4, 3, 5, 2, 6, 3, 4, 5, 2, 3]

eligible_machines = [
    [1],       # task 0
    [2],       # task 1
    [3],       # task 2
    [1],       # task 3
    [2],       # task 4
    [1],       # task 5
    [3],       # task 6
    [2],       # task 7
    [1],       # task 8
    [2, 3]     # task 9
]

prerequisites = [
    [],        # task 0
    [],        # task 1
    [],        # task 2
    [0],       # task 3
    [1],       # task 4
    [3],       # task 5
    [2, 4],    # task 6
    [4],       # task 7
    [5],       # task 8
    [7, 8]     # task 9
]

machines_set = [1, 2, 3]

# ============================================================
# Z3 Model
# ============================================================
opt = Optimize()

# Decision variables
start = [Int(f'start_{i}') for i in range(num_tasks)]
machine = [Int(f'machine_{i}') for i in range(num_tasks)]
makespan = Int('makespan')

# ----- Domain constraints -----
for i in range(num_tasks):
    opt.add(start[i] >= 0)
    # Machine must be one of the eligible machines
    opt.add(Or([machine[i] == m for m in eligible_machines[i]]))

# ----- Precedence constraints -----
for i in range(num_tasks):
    for p in prerequisites[i]:
        opt.add(start[i] >= start[p] + durations[p])

# ----- No overlap on same machine -----
# For every pair of tasks (i,j), if they share the same machine then
# their execution intervals cannot overlap.
for i in range(num_tasks):
    for j in range(i + 1, num_tasks):
        opt.add(Or(machine[i] != machine[j],
                   start[i] + durations[i] <= start[j],
                   start[j] + durations[j] <= start[i]))

# ----- Makespan definition -----
for i in range(num_tasks):
    opt.add(makespan >= start[i] + durations[i])

# Provide a reasonable upper bound to keep the search focused
opt.add(makespan <= 50)

# ----- Objective -----
opt.minimize(makespan)

# ============================================================
# Solve
# ============================================================
result = opt.check()

if result == sat:
    m = opt.model()
    ms = m[makespan].as_long()

    print("STATUS: sat")
    print(f"Makespan = {ms}")
    print()

    # Build schedule list
    schedule = []
    for i in range(num_tasks):
        s = m[start[i]].as_long()
        ma = m[machine[i]].as_long()
        e = s + durations[i]
        schedule.append((i, ma, s, e))

    print("Schedule (task, machine, start, end):")
    for i, ma, s, e in schedule:
        print(f"  Task {i}: Machine {ma}, Start={s}, End={e}")
    print()

    # Machine timelines
    for ma in machines_set:
        tasks_on_ma = [(i, s, e) for (i, m_a, s, e) in schedule if m_a == ma]
        tasks_on_ma.sort(key=lambda x: x[1])
        line = f"  Machine {ma}: "
        for i, s, e in tasks_on_ma:
            line += f"Task {i}[{s}-{e}]  "
        print(line)
    print()

    # ============================================================
    # Critical path computation (from precedence graph only)
    # ============================================================
    # Topological order: 0,1,2,3,4,5,6,7,8,9 respects all prerequisites
    topo_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # longest_path[i] = longest total duration from start to task i
    # (not including task i itself)
    longest_path = [0] * num_tasks
    predecessor = [-1] * num_tasks

    for i in topo_order:
        max_pred = 0
        best_pred = -1
        for p in prerequisites[i]:
            val = longest_path[p] + durations[p]
            if val > max_pred:
                max_pred = val
                best_pred = p
        longest_path[i] = max_pred
        predecessor[i] = best_pred

    # Find the task with the maximum completion time
    max_completion = 0
    last_task = -1
    for i in range(num_tasks):
        compl = longest_path[i] + durations[i]
        if compl > max_completion:
            max_completion = compl
            last_task = i

    # Trace back to get critical path
    crit_path = []
    curr = last_task
    while curr != -1:
        crit_path.append(curr)
        curr = predecessor[curr]

    crit_path.reverse()

    print("Critical Path (from precedence graph):")
    print(f"  Length (total duration): {max_completion}")
    print(f"  Tasks: {crit_path}")
    total_dur = sum(durations[t] for t in crit_path)
    print(f"  Sum of durations on path: {total_dur}")
    print(f"  Expected makespan (from critical path): {max_completion}")
    print(f"  Achieved makespan: {ms}")

    # Verify: all tasks on critical path should have zero slack
    # (earliest start = actual start in the optimal schedule)
    print()
    print("Critical Path Tasks in Schedule:")
    for t in crit_path:
        actual_s = m[start[t]].as_long()
        actual_e = actual_s + durations[t]
        # earliest start from precedence
        est = 0
        for p in prerequisites[t]:
            est = max(est, m[start[p]].as_long() + durations[p])
        print(f"  Task {t}: duration={durations[t]}, start={actual_s}, end={actual_e}, earliest_start={est}")

elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")