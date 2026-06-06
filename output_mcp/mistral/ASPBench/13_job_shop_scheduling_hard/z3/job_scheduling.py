from z3 import *

# ============================================================================
# Problem Data
# ============================================================================

# Jobs: list of (due_date, penalty_weight, list_of_operations)
# Each operation: (duration, machine, requires_master)
jobs = [
    # Job 0: Job 1
    (20, 3, [
        (4, 1, False),   # Op 0
        (5, 3, True),    # Op 1
        (3, 2, False)    # Op 2
    ]),
    # Job 1: Job 2
    (25, 1, [
        (6, 2, False),   # Op 0
        (4, 4, False),   # Op 1
        (2, 1, False),   # Op 2
        (3, 3, False)    # Op 3
    ]),
    # Job 2: Job 3
    (22, 2, [
        (7, 4, True),    # Op 0
        (6, 1, False),   # Op 1
        (2, 3, False)    # Op 2
    ]),
    # Job 3: Job 4
    (30, 1, [
        (2, 3, False),   # Op 0
        (5, 2, False),   # Op 1
        (3, 4, False),   # Op 2
        (4, 1, True)     # Op 3
    ])
]

# Machine maintenance windows: machine -> (start, end)
maintenance = {
    1: None,  # No maintenance
    2: (10, 11),
    3: None,
    4: (15, 16)
}

# Time horizon
TIME_HORIZON = 40

# ============================================================================
# Z3 Model
# ============================================================================

opt = Optimize()

# Decision variables: start time for each operation
# start[j][o] where j is job index, o is operation index
start = [[Int(f"start_{j}_{o}") for o in range(len(jobs[j][2]))] for j in range(len(jobs))]

# Derived end times
end = [[Int(f"end_{j}_{o}") for o in range(len(jobs[j][2]))] for j in range(len(jobs))]

# For each operation, end = start + duration
for j in range(len(jobs)):
    for o in range(len(jobs[j][2])):
        duration = jobs[j][2][o][0]
        opt.add(end[j][o] == start[j][o] + duration)

# ============================================================================
# Constraints
# ============================================================================

# 1. Precedence: operations within each job must be sequential
for j in range(len(jobs)):
    for o in range(len(jobs[j][2]) - 1):
        opt.add(end[j][o] <= start[j][o+1])

# 2. Machine exclusivity: no two operations on the same machine overlap
# We'll collect all operations per machine and add no-overlap constraints
machine_ops = {m: [] for m in range(1, 5)}  # Machines 1-4
for j in range(len(jobs)):
    for o in range(len(jobs[j][2])):
        m = jobs[j][2][o][1]
        machine_ops[m].append((j, o))

# For each machine, ensure no overlap between any two operations
for m in range(1, 5):
    ops = machine_ops[m]
    if len(ops) > 1:
        # Sort operations by start time (we'll enforce ordering via constraints)
        for i in range(len(ops)):
            for k in range(i+1, len(ops)):
                j1, o1 = ops[i]
                j2, o2 = ops[k]
                # Either op1 finishes before op2 starts, or op2 finishes before op1 starts
                opt.add(Or(end[j1][o1] <= start[j2][o2], end[j2][o2] <= start[j1][o1]))

# 3. Master operator exclusivity: at most one operation requiring master operator at a time
master_ops = []
for j in range(len(jobs)):
    for o in range(len(jobs[j][2])):
        if jobs[j][2][o][2]:  # requires_master
            master_ops.append((j, o))

# If there are master operations, ensure no two overlap
if len(master_ops) > 1:
    for i in range(len(master_ops)):
        for k in range(i+1, len(master_ops)):
            j1, o1 = master_ops[i]
            j2, o2 = master_ops[k]
            opt.add(Or(end[j1][o1] <= start[j2][o2], end[j2][o2] <= start[j1][o1]))

# 4. Maintenance windows: no operation can run during maintenance on its machine
for j in range(len(jobs)):
    for o in range(len(jobs[j][2])):
        m = jobs[j][2][o][1]
        maint = maintenance[m]
        if maint is not None:
            maint_start, maint_end = maint
            # Operation cannot overlap with maintenance window
            opt.add(Or(end[j][o] <= maint_start, start[j][o] >= maint_end))

# 5. Non-negative start times and within horizon
for j in range(len(jobs)):
    for o in range(len(jobs[j][2])):
        opt.add(start[j][o] >= 0)
        opt.add(start[j][o] < TIME_HORIZON)

# ============================================================================
# Objective: Minimize Total Cost = Makespan + Total Weighted Tardiness Penalty
# ============================================================================

# Makespan: maximum end time across all operations
makespan = Int("makespan")
# Collect all end times as Z3 expressions
end_times = [end[j][o] for j in range(len(jobs)) for o in range(len(jobs[j][2]))]
opt.add(makespan == Max(end_times))

# Tardiness for each job: max(0, finish_time - due_date) * penalty_weight
# Finish time for job j is end[j][last_op]
tardiness = []
total_penalty = Int("total_penalty")

for j in range(len(jobs)):
    due_date = jobs[j][0]
    penalty_weight = jobs[j][1]
    last_op = len(jobs[j][2]) - 1
    finish_time = end[j][last_op]
    tardy = Int(f"tardy_{j}")
    opt.add(tardy == If(finish_time > due_date, (finish_time - due_date) * penalty_weight, 0))
    tardiness.append(tardy)

opt.add(total_penalty == Sum(tardiness))

# Total cost = makespan + total_penalty
total_cost = Int("total_cost")
opt.add(total_cost == makespan + total_penalty)

# Minimize total cost
opt.minimize(total_cost)

# ============================================================================
# Solve and Output
# ============================================================================

BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for j in range(len(jobs)):
        for o in range(len(jobs[j][2])):
            schedule.append({
                "job": j + 1,
                "operation": o + 1,
                "machine": jobs[j][2][o][1],
                "start_time": model[start[j][o]],
                "duration": jobs[j][2][o][0],
                "requires_master": jobs[j][2][o][2]
            })
    
    # Sort schedule by start time for readability
    schedule.sort(key=lambda x: int(str(model[start[x["job"]-1][x["operation"]-1]])))
    
    # Extract metrics
    makespan_val = model[makespan]
    total_penalty_val = model[total_penalty]
    total_cost_val = model[total_cost]
    
    # Job completion info
    job_completion = []
    for j in range(len(jobs)):
        due_date = jobs[j][0]
        penalty_weight = jobs[j][1]
        last_op = len(jobs[j][2]) - 1
        finish_time = model[end[j][last_op]]
        tardy = max(0, int(finish_time) - due_date) * penalty_weight
        job_completion.append({
            "job": j + 1,
            "finish_time": finish_time,
            "due_date": due_date,
            "tardiness": tardy
        })
    
    # Feasibility (if we got a model, it's feasible)
    feasible = True
    
    print("schedule:")
    for op in schedule:
        print(f"  Job {op['job']}, Operation {op['operation']}: Machine {op['machine']}, Start {op['start_time']}, Duration {op['duration']}")
    
    print("metrics:")
    print(f"  makespan: {makespan_val}")
    print(f"  total_penalty: {total_penalty_val}")
    print(f"  total_cost: {total_cost_val}")
    
    print("job_completion:")
    for jc in job_completion:
        print(f"  Job {jc['job']}: Finish {jc['finish_time']}, Due {jc['due_date']}, Tardiness {jc['tardiness']}")
    
    print(f"feasible: {feasible}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")