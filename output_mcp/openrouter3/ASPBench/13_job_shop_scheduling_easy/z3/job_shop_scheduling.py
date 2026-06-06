from z3 import *

# Problem data
jobs = [1, 2, 3]
operations = [1, 2, 3]
machines = [1, 2, 3]

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

# Create solver
opt = Optimize()

# Declare start time variables for each operation
start = {}
end = {}
for j in jobs:
    for o in operations:
        start[(j, o)] = Int(f'start_{j}_{o}')
        end[(j, o)] = Int(f'end_{j}_{o}')
        machine, duration = op_data[(j, o)]
        # Non-negative start time
        opt.add(start[(j, o)] >= 0)
        # End time = start + duration
        opt.add(end[(j, o)] == start[(j, o)] + duration)

# Precedence constraints: operations within each job must be sequential
for j in jobs:
    for o in range(1, 3):  # o = 1, 2 (before next operation)
        # Operation o must finish before operation o+1 starts
        opt.add(end[(j, o)] <= start[(j, o + 1)])

# Machine non-overlap constraints: operations on same machine cannot overlap
for m in machines:
    # Get all operations that use machine m
    ops_on_m = [(j, o) for (j, o), (mach, dur) in op_data.items() if mach == m]
    # For each pair of operations on the same machine, they cannot overlap
    for i in range(len(ops_on_m)):
        for k in range(i + 1, len(ops_on_m)):
            j1, o1 = ops_on_m[i]
            j2, o2 = ops_on_m[k]
            # Either operation 1 finishes before operation 2 starts, or vice versa
            opt.add(Or(
                end[(j1, o1)] <= start[(j2, o2)],
                end[(j2, o2)] <= start[(j1, o1)]
            ))

# Define makespan as the maximum end time
makespan = Int('makespan')
for j in jobs:
    for o in operations:
        opt.add(makespan >= end[(j, o)])

# Minimize makespan
opt.minimize(makespan)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for j in jobs:
        for o in operations:
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
    
    # Verify expected optimal makespan
    if makespan_value == 11:
        print("Optimal makespan matches expected value: 11")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")