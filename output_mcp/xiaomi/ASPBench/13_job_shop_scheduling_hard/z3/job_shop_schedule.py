from z3 import *

# Problem data
jobs = {
    1: {"due": 20, "weight": 3, "ops": [
        {"dur": 4, "machine": 1, "master": False},
        {"dur": 5, "machine": 3, "master": True},
        {"dur": 3, "machine": 2, "master": False}
    ]},
    2: {"due": 25, "weight": 1, "ops": [
        {"dur": 6, "machine": 2, "master": False},
        {"dur": 4, "machine": 4, "master": False},
        {"dur": 2, "machine": 1, "master": False},
        {"dur": 3, "machine": 3, "master": False}
    ]},
    3: {"due": 22, "weight": 2, "ops": [
        {"dur": 7, "machine": 4, "master": True},
        {"dur": 6, "machine": 1, "master": False},
        {"dur": 2, "machine": 3, "master": False}
    ]},
    4: {"due": 30, "weight": 1, "ops": [
        {"dur": 2, "machine": 3, "master": False},
        {"dur": 5, "machine": 2, "master": False},
        {"dur": 3, "machine": 4, "master": False},
        {"dur": 4, "machine": 1, "master": True}
    ]}
}

# Maintenance windows: machine -> list of (start, end) inclusive
maintenance = {
    2: [(10, 11)],
    4: [(15, 16)]
}

# Create optimizer
opt = Optimize()

# Decision variables: start time for each operation
start = {}
for j in jobs:
    for i, op in enumerate(jobs[j]["ops"]):
        start[(j, i)] = Int(f'start_{j}_{i}')

# Makespan variable
makespan = Int('makespan')

# Constraints
# 1. All operations start at non-negative times
for (j, i) in start:
    opt.add(start[(j, i)] >= 0)

# 2. Precedence within jobs
for j in jobs:
    ops = jobs[j]["ops"]
    for i in range(len(ops) - 1):
        opt.add(start[(j, i)] + ops[i]["dur"] <= start[(j, i+1)])

# 3. Machine exclusivity
# Group operations by machine
machine_ops = {}
for j in jobs:
    for i, op in enumerate(jobs[j]["ops"]):
        m = op["machine"]
        if m not in machine_ops:
            machine_ops[m] = []
        machine_ops[m].append((j, i, op["dur"]))

# For each machine, operations must not overlap
for m in machine_ops:
    ops_list = machine_ops[m]
    for idx1 in range(len(ops_list)):
        for idx2 in range(idx1 + 1, len(ops_list)):
            j1, i1, dur1 = ops_list[idx1]
            j2, i2, dur2 = ops_list[idx2]
            # Either op1 finishes before op2 starts, or op2 finishes before op1 starts
            opt.add(Or(
                start[(j1, i1)] + dur1 <= start[(j2, i2)],
                start[(j2, i2)] + dur2 <= start[(j1, i1)]
            ))

# 4. Master operator exclusivity
master_ops = []
for j in jobs:
    for i, op in enumerate(jobs[j]["ops"]):
        if op["master"]:
            master_ops.append((j, i, op["dur"]))

# At most one master operation at a time
for idx1 in range(len(master_ops)):
    for idx2 in range(idx1 + 1, len(master_ops)):
        j1, i1, dur1 = master_ops[idx1]
        j2, i2, dur2 = master_ops[idx2]
        opt.add(Or(
            start[(j1, i1)] + dur1 <= start[(j2, i2)],
            start[(j2, i2)] + dur2 <= start[(j1, i1)]
        ))

# 5. Maintenance windows
for m in maintenance:
    for (win_start, win_end) in maintenance[m]:
        for (j, i, dur) in machine_ops.get(m, []):
            # Operation must either finish before window starts or start after window ends
            opt.add(Or(
                start[(j, i)] + dur <= win_start,
                start[(j, i)] >= win_end + 1
            ))

# 6. Makespan definition
for j in jobs:
    ops = jobs[j]["ops"]
    last_op_idx = len(ops) - 1
    opt.add(makespan >= start[(j, last_op_idx)] + ops[last_op_idx]["dur"])

# 7. Total weighted tardiness penalty
tardiness = {}
penalty_terms = []
for j in jobs:
    ops = jobs[j]["ops"]
    last_op_idx = len(ops) - 1
    finish_j = start[(j, last_op_idx)] + ops[last_op_idx]["dur"]
    due_j = jobs[j]["due"]
    weight_j = jobs[j]["weight"]
    
    # Tardiness = max(0, finish - due)
    tard = Int(f'tardiness_{j}')
    tardiness[j] = tard
    opt.add(tard == If(finish_j > due_j, finish_j - due_j, 0))
    penalty_terms.append(tard * weight_j)

total_penalty = Int('total_penalty')
opt.add(total_penalty == Sum(penalty_terms))

# Total cost = makespan + total_penalty
total_cost = Int('total_cost')
opt.add(total_cost == makespan + total_penalty)

# Objective: minimize total cost
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    print("\nSchedule:")
    schedule = []
    for j in jobs:
        for i, op in enumerate(jobs[j]["ops"]):
            s = model.evaluate(start[(j, i)]).as_long()
            dur = op["dur"]
            m = op["machine"]
            schedule.append({
                "job": j, "op": i+1, "machine": m,
                "start": s, "duration": dur, "end": s + dur
            })
            print(f"  Job {j}, Op {i+1}: Machine {m}, Start={s}, Duration={dur}, End={s+dur}")
    
    # Extract metrics
    makespan_val = model.evaluate(makespan).as_long()
    total_penalty_val = model.evaluate(total_penalty).as_long()
    total_cost_val = model.evaluate(total_cost).as_long()
    
    print(f"\nMetrics:")
    print(f"  Makespan: {makespan_val}")
    print(f"  Total Penalty: {total_penalty_val}")
    print(f"  Total Cost: {total_cost_val}")
    
    # Job completion info
    print(f"\nJob Completion:")
    for j in jobs:
        ops = jobs[j]["ops"]
        last_op_idx = len(ops) - 1
        finish = model.evaluate(start[(j, last_op_idx)] + ops[last_op_idx]["dur"]).as_long()
        due = jobs[j]["due"]
        tard = model.evaluate(tardiness[j]).as_long()
        print(f"  Job {j}: Finish={finish}, Due={due}, Tardiness={tard}")
    
    print(f"\nFeasible: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")