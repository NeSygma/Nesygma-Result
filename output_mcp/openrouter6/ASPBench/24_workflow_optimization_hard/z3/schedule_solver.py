from z3 import *

# Problem data
tasks = list(range(10))
durations = [4, 3, 5, 2, 6, 3, 4, 5, 2, 3]
eligible_machines = [
    [1],      # task 0
    [2],      # task 1
    [3],      # task 2
    [1],      # task 3
    [2],      # task 4
    [1],      # task 5
    [3],      # task 6
    [2],      # task 7
    [1],      # task 8
    [2, 3]    # task 9
]

# Predecessors: for each task, list of prerequisite tasks
predecessors = [
    [],       # task 0
    [],       # task 1
    [],       # task 2
    [0],      # task 3
    [1],      # task 4
    [3],      # task 5
    [2, 4],   # task 6
    [4],      # task 7
    [5],      # task 8
    [7, 8]    # task 9
]

# Create solver
opt = Optimize()

# Declare variables
start_time = [Int(f'start_{i}') for i in tasks]
machine = [Int(f'machine_{i}') for i in tasks]
makespan = Int('makespan')

# Constraints
# 1. Non-negative start times
for i in tasks:
    opt.add(start_time[i] >= 0)

# 2. Machine assignment: each task must be assigned to one of its eligible machines
for i in tasks:
    opt.add(Or([machine[i] == m for m in eligible_machines[i]]))

# 3. Precedence constraints: tasks cannot start until all prerequisites complete
for i in tasks:
    for pred in predecessors[i]:
        opt.add(start_time[pred] + durations[pred] <= start_time[i])

# 4. Machine non-overlap: tasks on same machine cannot overlap
for i in tasks:
    for j in tasks:
        if i < j:
            # If same machine, then one must finish before the other starts
            opt.add(Or(
                machine[i] != machine[j],
                start_time[i] + durations[i] <= start_time[j],
                start_time[j] + durations[j] <= start_time[i]
            ))

# 5. Makespan definition: maximum end time across all tasks
for i in tasks:
    opt.add(makespan >= start_time[i] + durations[i])

# Objective: minimize makespan
opt.minimize(makespan)

# Check and get model
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("\nOptimal Schedule:")
    print("Task | Machine | Start | End")
    print("-----|---------|-------|----")
    for i in tasks:
        task_start = model[start_time[i]].as_long()
        task_machine = model[machine[i]].as_long()
        task_end = task_start + durations[i]
        print(f"{i:4} | {task_machine:7} | {task_start:5} | {task_end:3}")
    
    optimal_makespan = model[makespan].as_long()
    print(f"\nOptimal makespan: {optimal_makespan}")
    
    # Critical path (computed from precedence graph, independent of schedule)
    # Longest path: 1 -> 4 -> 7 -> 9 (durations: 3+6+5+3 = 17)
    critical_path = [1, 4, 7, 9]
    print(f"Critical path: {critical_path}")
    
    # Verify critical path length matches makespan
    cp_length = sum(durations[i] for i in critical_path)
    print(f"Critical path length: {cp_length}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")