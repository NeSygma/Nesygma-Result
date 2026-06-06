from z3 import *

# Problem data
# Operations: (job, op_index, machine, duration)
operations = [
    (1, 1, 1, 3),  # j1o1: m1, dur 3
    (1, 2, 2, 2),  # j1o2: m2, dur 2
    (1, 3, 3, 4),  # j1o3: m3, dur 4
    (2, 1, 2, 2),  # j2o1: m2, dur 2
    (2, 2, 1, 5),  # j2o2: m1, dur 5
    (2, 3, 3, 1),  # j2o3: m3, dur 1
    (3, 1, 3, 4),  # j3o1: m3, dur 4
    (3, 2, 1, 1),  # j3o2: m1, dur 1
    (3, 3, 2, 3),  # j3o3: m2, dur 3
]

# Create start time variables for each operation
start = {}
for (j, o, m, d) in operations:
    start[(j, o)] = Int(f'start_j{j}o{o}')

# Makespan variable
makespan = Int('makespan')

opt = Optimize()

# 1. All start times >= 0
for key in start:
    opt.add(start[key] >= 0)

# 2. Makespan >= end time of every operation
for (j, o, m, d) in operations:
    opt.add(makespan >= start[(j, o)] + d)

# 3. Precedence constraints within each job
# Job 1: j1o1 before j1o2, j1o2 before j1o3
opt.add(start[(1, 1)] + 3 <= start[(1, 2)])
opt.add(start[(1, 2)] + 2 <= start[(1, 3)])

# Job 2: j2o1 before j2o2, j2o2 before j2o3
opt.add(start[(2, 1)] + 2 <= start[(2, 2)])
opt.add(start[(2, 2)] + 5 <= start[(2, 3)])

# Job 3: j3o1 before j3o2, j3o2 before j3o3
opt.add(start[(3, 1)] + 4 <= start[(3, 2)])
opt.add(start[(3, 2)] + 1 <= start[(3, 3)])

# 4. Machine non-overlap constraints
# Group operations by machine
machine_ops = {}
for (j, o, m, d) in operations:
    if m not in machine_ops:
        machine_ops[m] = []
    machine_ops[m].append((j, o, d))

# For each pair of operations on the same machine, they must not overlap
for m in machine_ops:
    ops_list = machine_ops[m]
    for i in range(len(ops_list)):
        for k in range(i + 1, len(ops_list)):
            j1, o1, d1 = ops_list[i]
            j2, o2, d2 = ops_list[k]
            # Either op1 finishes before op2 starts, or op2 finishes before op1 starts
            opt.add(Or(
                start[(j1, o1)] + d1 <= start[(j2, o2)],
                start[(j2, o2)] + d2 <= start[(j1, o1)]
            ))

# Objective: minimize makespan
opt.minimize(makespan)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for (j, o, m, d) in operations:
        s = model[start[(j, o)]].as_long()
        schedule.append({
            'job': j,
            'operation': o,
            'machine': m,
            'start': s,
            'duration': d,
            'end': s + d
        })
    
    ms = model[makespan].as_long()
    print(f"makespan = {ms}")
    print(f"feasible = True")
    print()
    print("Schedule:")
    print(f"{'Job':<6} {'Op':<6} {'Machine':<10} {'Start':<8} {'Duration':<10} {'End':<6}")
    print("-" * 50)
    for entry in sorted(schedule, key=lambda x: (x['job'], x['operation'])):
        print(f"j{entry['job']}o{entry['operation']:<4} m{entry['machine']:<8} {entry['start']:<8} {entry['duration']:<10} {entry['end']:<6}")
    
    print()
    print("Machine timelines:")
    for m in sorted(machine_ops.keys()):
        ops_on_m = [e for e in schedule if e['machine'] == m]
        ops_on_m.sort(key=lambda x: x['start'])
        print(f"  m{m}: ", end="")
        for e in ops_on_m:
            print(f"[{e['start']}-{e['end']}: j{e['job']}o{e['operation']}] ", end="")
        print()
    
    # Verify optimality
    if ms == 11:
        print("\nOptimal makespan matches expected value of 11.")
    else:
        print(f"\nNote: Got makespan {ms}, expected 11.")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")