from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Create solver for optimization
opt = Optimize()

# Task data: (duration, eligible_machines, prerequisites)
task_data = {
    0: (4, [1], []),
    1: (3, [2], []),
    2: (5, [3], []),
    3: (2, [1], [0]),
    4: (6, [2], [1]),
    5: (3, [1], [3]),
    6: (4, [3], [2, 4]),
    7: (5, [2], [4]),
    8: (2, [1], [5]),
    9: (3, [2, 3], [7, 8]),
}

# Number of tasks and machines
num_tasks = 10
machines = [1, 2, 3]

# Decision variables
# Assignment: which machine each task runs on
assignment = [Int(f"assignment_{i}") for i in range(num_tasks)]

# Start and end times for each task
start_time = [Int(f"start_{i}") for i in range(num_tasks)]
end_time = [Int(f"end_{i}") for i in range(num_tasks)]

# Makespan (objective)
makespan = Int("makespan")

# Helper: duration of each task
duration = [Int(f"duration_{i}") for i in range(num_tasks)]
for i in range(num_tasks):
    opt.add(duration[i] == task_data[i][0])

# Constraint 1: Each task must be assigned to exactly one of its eligible machines
for i in range(num_tasks):
    eligible = task_data[i][1]
    opt.add(Or([assignment[i] == m for m in eligible]))
    # Ensure assignment is to one of the eligible machines only
    opt.add(Or([assignment[i] == m for m in machines if m in eligible]))

# Constraint 2: End time = start time + duration
for i in range(num_tasks):
    opt.add(end_time[i] == start_time[i] + duration[i])

# Constraint 3: Precedence constraints (task i cannot start until all prerequisites complete)
for i in range(num_tasks):
    prereqs = task_data[i][2]
    for p in prereqs:
        opt.add(start_time[i] >= end_time[p])

# Constraint 4: No overlap on the same machine
# For each machine, ensure that for any two tasks assigned to it, their intervals do not overlap
for m in machines:
    # Get all tasks eligible for this machine
    tasks_on_m = [i for i in range(num_tasks) if m in task_data[i][1]]
    # For every pair of tasks on this machine, ensure no overlap
    for i in range(len(tasks_on_m)):
        for j in range(i + 1, len(tasks_on_m)):
            ti = tasks_on_m[i]
            tj = tasks_on_m[j]
            # Either task i ends before task j starts, or task j ends before task i starts
            opt.add(Or(end_time[ti] <= start_time[tj], end_time[tj] <= start_time[ti]))

# Constraint 5: Makespan is the maximum end time
# Compute makespan as the maximum of all end times
opt.add(makespan >= end_time[i] for i in range(num_tasks))
opt.add(makespan == end_time[0])
for i in range(1, num_tasks):
    opt.add(If(end_time[i] > makespan, makespan == end_time[i], True))

# Objective: Minimize makespan
opt.minimize(makespan)

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal makespan:", model[makespan])
    
    # Print schedule
    print("\nSchedule:")
    for i in range(num_tasks):
        print(f"Task {i}: machine={model[assignment[i]]}, start={model[start_time[i]]}, end={model[end_time[i]]}, duration={model[duration[i]]}")
    
    # Print critical path (longest path in the precedence graph)
    # We can approximate this by finding the task with end_time == makespan
    # and backtracking through prerequisites
    critical_path = []
    current = None
    for i in range(num_tasks):
        if model[end_time[i]] == model[makespan]:
            current = i
            break
    
    if current is not None:
        critical_path.append(current)
        # Backtrack through prerequisites
        while task_data[current][2]:
            # Find the prerequisite that finishes last
            last_prereq = max(task_data[current][2], key=lambda p: model[end_time[p]])
            critical_path.append(last_prereq)
            current = last_prereq
        critical_path.reverse()
        print("\nCritical path (approximate):", critical_path)
    
    # Verify expected optimal makespan
    if model[makespan] == 17:
        print("\nExpected optimal makespan achieved: 17")
    else:
        print(f"\nWarning: Expected makespan 17, got {model[makespan]}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")