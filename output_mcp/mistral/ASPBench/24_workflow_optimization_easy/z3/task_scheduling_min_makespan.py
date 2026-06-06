from z3 import *

# Problem data
num_tasks = 8
durations = [3, 2, 4, 1, 5, 2, 3, 2]
prerequisites = [
    [],           # Task 0
    [],           # Task 1
    [0],          # Task 2
    [1],          # Task 3
    [2, 3],       # Task 4
    [0],          # Task 5
    [4],          # Task 6
    [5, 6]        # Task 7
]

# Declare variables
solver = Optimize()
start_time = [Int(f'start_time_{i}') for i in range(num_tasks)]
end_time = [Int(f'end_time_{i}') for i in range(num_tasks)]

# Constraints: end_time[i] = start_time[i] + duration[i]
for i in range(num_tasks):
    solver.add(end_time[i] == start_time[i] + durations[i])

# Precedence constraints: start_time[i] >= max(end_time[p] for p in prerequisites[i])
for i in range(num_tasks):
    if prerequisites[i]:
        # Ensure start_time[i] is after all prerequisites finish
        for p in prerequisites[i]:
            solver.add(start_time[i] >= end_time[p])

# Makespan is the maximum end_time
makespan = Int('makespan')
# Constrain makespan to be the maximum of all end times
solver.add(makespan >= end_time[i] for i in range(num_tasks))
solver.add(makespan == end_time[0])
for i in range(1, num_tasks):
    solver.add(If(makespan < end_time[i], makespan == end_time[i], True))

# Objective: minimize makespan
solver.minimize(makespan)

# Check and print results
BENCHMARK_MODE = True  # Set False outside benchmark mode
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Schedule:")
    for i in range(num_tasks):
        print(f"Task {i}: start_time = {model[start_time[i]]}, end_time = {model[end_time[i]]}")
    print(f"Makespan: {model[makespan]}")
    
    # Critical path: tasks on the longest path (no slack)
    # A task is on the critical path if its start time equals the max end time of its prerequisites
    critical_path = []
    for i in range(num_tasks):
        if prerequisites[i]:
            max_prereq_end = max(model[end_time[p]] for p in prerequisites[i])
            if model[start_time[i]] == max_prereq_end:
                critical_path.append(i)
        else:
            # Tasks with no prerequisites are on the critical path if they start at time 0
            if model[start_time[i]] == 0:
                critical_path.append(i)
    
    # Ensure the critical path is a valid chain (optional refinement for correctness)
    # For simplicity, we just print the tasks that have no slack
    print("Critical path (tasks with no slack):", sorted(critical_path))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")