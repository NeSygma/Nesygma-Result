from z3 import *

# Task data
tasks = list(range(10))
durations = [4, 3, 5, 2, 6, 3, 4, 5, 2, 3]
eligible_machines = [
    [1],        # Task 0
    [2],        # Task 1
    [3],        # Task 2
    [1],        # Task 3
    [2],        # Task 4
    [1],        # Task 5
    [3],        # Task 6
    [2],        # Task 7
    [1],        # Task 8
    [2, 3],     # Task 9
]
prerequisites = [
    [],         # Task 0
    [],         # Task 1
    [],         # Task 2
    [0],        # Task 3
    [1],        # Task 4
    [3],        # Task 5
    [2, 4],     # Task 6
    [4],        # Task 7
    [5],        # Task 8
    [7, 8],     # Task 9
]

# Machines
machines = [1, 2, 3]

# Declare Z3 variables
start_time = [Int(f'start_time_{t}') for t in tasks]
end_time = [Int(f'end_time_{t}') for t in tasks]
machine_assignment = [Int(f'machine_{t}') for t in tasks]

# Initialize optimizer
opt = Optimize()

# Constraint 1: Assignment to eligible machines
for t in tasks:
    opt.add(Or([machine_assignment[t] == m for m in eligible_machines[t]]))

# Constraint 2: Duration and end_time
for t in tasks:
    opt.add(end_time[t] == start_time[t] + durations[t])

# Constraint 3: Precedence
for t in tasks:
    for p in prerequisites[t]:
        opt.add(start_time[t] >= end_time[p])

# Constraint 4: Machine exclusivity (no overlap on same machine)
for m in machines:
    # Get all tasks assigned to machine m
    tasks_on_m = [t for t in tasks if m in eligible_machines[t]]
    # For every pair of tasks on the same machine, ensure no overlap
    for i in range(len(tasks_on_m)):
        for j in range(i + 1, len(tasks_on_m)):
            t1 = tasks_on_m[i]
            t2 = tasks_on_m[j]
            # Either t1 finishes before t2 starts, or t2 finishes before t1 starts
            opt.add(Or(
                end_time[t1] <= start_time[t2],
                end_time[t2] <= start_time[t1]
            ))

# Constraint 5: Non-negative start times
for t in tasks:
    opt.add(start_time[t] >= 0)

# Objective: Minimize makespan
makespan = Int('makespan')
# Compute makespan as the maximum end_time
opt.add(makespan >= end_time[t] for t in tasks)
opt.minimize(makespan)

# Check and print result
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("makespan =", model[makespan])
    # Print schedule
    print("schedule = [")
    for t in tasks:
        print(f"  {{task: {t}, machine: {model[machine_assignment[t]]}, start_time: {model[start_time[t]]}, end_time: {model[end_time[t]]}}},")
    print("]")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")