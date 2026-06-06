from z3 import *

# Problem data
jobs = [1, 2, 3]
ops = [1, 2, 3]

# Operation data: (machine, duration)
op_data = {
    (1, 1): (1, 3),  # j1o1: machine 1, duration 3
    (1, 2): (2, 2),  # j1o2: machine 2, duration 2
    (1, 3): (3, 4),  # j1o3: machine 3, duration 4
    (2, 1): (2, 2),  # j2o1: machine 2, duration 2
    (2, 2): (1, 5),  # j2o2: machine 1, duration 5
    (2, 3): (3, 1),  # j2o3: machine 3, duration 1
    (3, 1): (3, 4),  # j3o1: machine 3, duration 4
    (3, 2): (1, 1),  # j3o2: machine 1, duration 1
    (3, 3): (2, 3),  # j3o3: machine 2, duration 3
}

# Create optimization solver
opt = Optimize()

# Decision variables: start times for each operation
start = {}
end = {}
for j in jobs:
    for o in ops:
        start[(j, o)] = Int(f'start_{j}_{o}')
        end[(j, o)] = Int(f'end_{j}_{o}')
        machine, duration = op_data[(j, o)]
        # End time = start + duration
        opt.add(end[(j, o)] == start[(j, o)] + duration)
        # Non-negative start time
        opt.add(start[(j, o)] >= 0)

# Precedence constraints within each job
for j in jobs:
    for o in range(1, 3):  # o = 1, 2 (since we have 3 operations)
        curr = (j, o)
        next_op = (j, o + 1)
        machine_curr, duration_curr = op_data[curr]
        # Next operation must start after current finishes
        opt.add(start[next_op] >= end[curr])

# Machine constraints: no overlapping operations on same machine
# Group operations by machine
machine_ops = {1: [], 2: [], 3: []}
for (j, o), (machine, duration) in op_data.items():
    machine_ops[machine].append((j, o))

# For each machine, ensure no overlap between any two operations
for machine, ops_list in machine_ops.items():
    for i in range(len(ops_list)):
        for j in range(i + 1, len(ops_list)):
            op1 = ops_list[i]
            op2 = ops_list[j]
            # Either op1 finishes before op2 starts, or op2 finishes before op1 starts
            opt.add(Or(
                end[op1] <= start[op2],
                end[op2] <= start[op1]
            ))

# Makespan: maximum end time among all operations
makespan = Int('makespan')
for (j, o) in start:
    opt.add(makespan >= end[(j, o)])

# Minimize makespan
opt.minimize(makespan)

# Check for solution
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for j in jobs:
        for o in ops:
            machine, duration = op_data[(j, o)]
            start_time = model[start[(j, o)]].as_long()
            schedule.append({
                'job': j,
                'operation': o,
                'machine': machine,
                'start': start_time,
                'duration': duration
            })
    
    # Print schedule
    print("Schedule:")
    for entry in schedule:
        print(f"  Job {entry['job']}, Operation {entry['operation']}: "
              f"Machine {entry['machine']}, Start {entry['start']}, "
              f"Duration {entry['duration']}, End {entry['start'] + entry['duration']}")
    
    # Print makespan
    makespan_value = model[makespan].as_long()
    print(f"Makespan: {makespan_value}")
    print(f"Feasible: True")
    
    # Verify optimal makespan is 11 (as expected)
    if makespan_value == 11:
        print("Optimal makespan confirmed: 11")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")