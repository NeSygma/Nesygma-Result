from z3 import *

# Problem data
tasks = list(range(10))
durations = [4, 3, 5, 2, 6, 3, 4, 5, 2, 3]
eligible_machines = {
    0: [1],
    1: [2],
    2: [3],
    3: [1],
    4: [2],
    5: [1],
    6: [3],
    7: [2],
    8: [1],
    9: [2, 3]
}
prerequisites = {
    0: [],
    1: [],
    2: [],
    3: [0],
    4: [1],
    5: [3],
    6: [2, 4],
    7: [4],
    8: [5],
    9: [7, 8]
}
machines = [1, 2, 3]

# Create solver
opt = Optimize()

# Declare variables
start_time = [Int(f'start_{i}') for i in tasks]
machine = [Int(f'machine_{i}') for i in tasks]
end_time = [Int(f'end_{i}') for i in tasks]

# Add constraints for each task
for i in tasks:
    # End time = start time + duration
    opt.add(end_time[i] == start_time[i] + durations[i])
    
    # Task must start at non-negative time
    opt.add(start_time[i] >= 0)
    
    # Machine assignment must be from eligible machines
    machine_options = [machine[i] == m for m in eligible_machines[i]]
    opt.add(Or(machine_options))
    
    # Precedence constraints: task i cannot start until all prerequisites complete
    for prereq in prerequisites[i]:
        opt.add(start_time[i] >= end_time[prereq])

# No overlapping tasks on same machine
for m in machines:
    for i in tasks:
        for j in tasks:
            if i < j:  # Avoid duplicate pairs
                # If both tasks assigned to same machine, they cannot overlap
                # Either i finishes before j starts, or j finishes before i starts
                opt.add(Implies(
                    And(machine[i] == m, machine[j] == m),
                    Or(
                        end_time[i] <= start_time[j],
                        end_time[j] <= start_time[i]
                    )
                ))

# Makespan variable
makespan = Int('makespan')
for i in tasks:
    opt.add(makespan >= end_time[i])

# Objective: minimize makespan
opt.minimize(makespan)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for i in tasks:
        task_info = {
            'task': i,
            'machine': model[machine[i]].as_long(),
            'start_time': model[start_time[i]].as_long(),
            'end_time': model[end_time[i]].as_long()
        }
        schedule.append(task_info)
    
    # Print schedule
    print("\nSchedule:")
    print("Task | Machine | Start | End")
    print("-" * 30)
    for task in schedule:
        print(f"{task['task']:4} | {task['machine']:7} | {task['start_time']:5} | {task['end_time']:3}")
    
    # Print makespan
    makespan_value = model[makespan].as_long()
    print(f"\nMakespan: {makespan_value}")
    
    # Find critical path (longest dependency chain)
    # Calculate earliest start and end times for each task
    earliest_start = [0] * 10
    earliest_end = [0] * 10
    for i in tasks:
        earliest_start[i] = model[start_time[i]].as_long()
        earliest_end[i] = earliest_start[i] + durations[i]
    
    # Find the task with maximum end time (makespan)
    max_end_task = max(tasks, key=lambda i: earliest_end[i])
    
    # Backtrack to find critical path
    critical_path = []
    current = max_end_task
    while True:
        critical_path.insert(0, current)
        # Find prerequisite that determines the start time
        if not prerequisites[current]:
            break
        # Find which prerequisite ends latest
        latest_prereq = max(prerequisites[current], key=lambda p: earliest_end[p])
        if earliest_end[latest_prereq] == earliest_start[current]:
            current = latest_prereq
        else:
            # This shouldn't happen in optimal schedule
            break
    
    print(f"\nCritical path: {critical_path}")
    
    # Verify makespan matches expected
    if makespan_value == 17:
        print(f"\n✓ Optimal makespan of 17 achieved!")
    else:
        print(f"\n⚠ Makespan is {makespan_value}, expected 17")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")