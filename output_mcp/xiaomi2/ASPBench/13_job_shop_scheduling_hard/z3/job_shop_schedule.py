from z3 import *

# ============================================================
# Problem Data
# ============================================================

# Operations: (job, op_index, machine, duration, requires_master)
operations = [
    # Job 1 (Due: 20, Weight: 3)
    (1, 1, 1, 4, False),
    (1, 2, 3, 5, True),
    (1, 3, 2, 3, False),
    # Job 2 (Due: 25, Weight: 1)
    (2, 1, 2, 6, False),
    (2, 2, 4, 4, False),
    (2, 3, 1, 2, False),
    (2, 4, 3, 3, False),
    # Job 3 (Due: 22, Weight: 2)
    (3, 1, 4, 7, True),
    (3, 2, 1, 6, False),
    (3, 3, 3, 2, False),
    # Job 4 (Due: 30, Weight: 1)
    (4, 1, 3, 2, False),
    (4, 2, 2, 5, False),
    (4, 3, 4, 3, False),
    (4, 4, 1, 4, True),
]

# Job info: job -> (due_date, penalty_weight)
job_info = {
    1: (20, 3),
    2: (25, 1),
    3: (22, 2),
    4: (30, 1),
}

# Maintenance windows: machine -> (start, end) inclusive
maintenance = {
    2: (10, 11),
    4: (15, 16),
}

TIME_HORIZON = 40

# ============================================================
# Z3 Model
# ============================================================

opt = Optimize()
opt.set("opt.priority", "lex")  # Lexicographic: first minimize makespan, then penalty

# Decision variables: start time for each operation
starts = {}
for (j, o, m, d, master) in operations:
    starts[(j, o)] = Int(f'start_j{j}_o{o}')

# End times
ends = {}
for (j, o, m, d, master) in operations:
    ends[(j, o)] = starts[(j, o)] + d

# Makespan
makespan = Int('makespan')

# Domain constraints: all starts >= 0, <= TIME_HORIZON
for key in starts:
    opt.add(starts[key] >= 0)
    opt.add(starts[key] <= TIME_HORIZON)

# Makespan >= all end times
for key in ends:
    opt.add(makespan >= ends[key])

# ============================================================
# Constraint 1: Precedence within jobs
# ============================================================
# Group operations by job
from collections import defaultdict
job_ops = defaultdict(list)
for (j, o, m, d, master) in operations:
    job_ops[j].append(o)

for j in job_ops:
    sorted_ops = sorted(job_ops[j])
    for i in range(len(sorted_ops) - 1):
        o_curr = sorted_ops[i]
        o_next = sorted_ops[i + 1]
        # Current operation must finish before next starts
        opt.add(ends[(j, o_curr)] <= starts[(j, o_next)])

# ============================================================
# Constraint 2: Machine Exclusivity
# ============================================================
# Group operations by machine
machine_ops = defaultdict(list)
for (j, o, m, d, master) in operations:
    machine_ops[m].append((j, o, d))

for m in machine_ops:
    ops_list = machine_ops[m]
    for i in range(len(ops_list)):
        for k in range(i + 1, len(ops_list)):
            j1, o1, d1 = ops_list[i]
            j2, o2, d2 = ops_list[k]
            # Either op1 finishes before op2 starts, or op2 finishes before op1 starts
            opt.add(Or(
                ends[(j1, o1)] <= starts[(j2, o2)],
                ends[(j2, o2)] <= starts[(j1, o1)]
            ))

# ============================================================
# Constraint 3: Master Operator Exclusivity
# ============================================================
master_ops = [(j, o, d) for (j, o, m, d, master) in operations if master]
for i in range(len(master_ops)):
    for k in range(i + 1, len(master_ops)):
        j1, o1, d1 = master_ops[i]
        j2, o2, d2 = master_ops[k]
        opt.add(Or(
            ends[(j1, o1)] <= starts[(j2, o2)],
            ends[(j2, o2)] <= starts[(j1, o1)]
        ))

# ============================================================
# Constraint 4: Maintenance Windows
# ============================================================
for (j, o, m, d, master) in operations:
    if m in maintenance:
        maint_start, maint_end = maintenance[m]
        # Operation must either finish before maintenance starts
        # or start after maintenance ends (inclusive window)
        # Maintenance [maint_start, maint_end] inclusive means
        # machine unavailable at times maint_start..maint_end
        # Operation occupies [start, start+d) so must avoid overlap
        opt.add(Or(
            ends[(j, o)] <= maint_start,
            starts[(j, o)] >= maint_end + 1
        ))

# ============================================================
# Objective: Minimize Makespan + Total Weighted Tardiness
# ============================================================

# Tardiness per job
tardiness = {}
for j in job_info:
    due, weight = job_info[j]
    # Job completion time = max end time of all operations in that job
    job_end = Int(f'job_end_{j}')
    # job_end >= all operation ends for this job
    opt.add(job_end >= 0)
    for o in job_ops[j]:
        opt.add(job_end >= ends[(j, o)])
    # job_end is exactly the max (we minimize, so it will be tight)
    tardiness[j] = Int(f'tardiness_{j}')
    opt.add(tardiness[j] == If(job_end - due > 0, job_end - due, 0))

# Total weighted tardiness penalty
total_penalty = Int('total_penalty')
opt.add(total_penalty == Sum([tardiness[j] * job_info[j][1] for j in job_info]))

# Total cost
total_cost = Int('total_cost')
opt.add(total_cost == makespan + total_penalty)

# Minimize total cost
opt.minimize(total_cost)

# ============================================================
# Solve
# ============================================================
result = opt.check()

if result == sat:
    model = opt.model()
    
    makespan_val = model.eval(makespan).as_long()
    total_penalty_val = model.eval(total_penalty).as_long()
    total_cost_val = model.eval(total_cost).as_long()
    
    print("STATUS: sat")
    print(f"\n=== OPTIMAL SCHEDULE ===")
    print(f"Makespan: {makespan_val}")
    print(f"Total Weighted Tardiness Penalty: {total_penalty_val}")
    print(f"Total Cost: {total_cost_val}")
    
    print(f"\n=== OPERATION SCHEDULE ===")
    # Collect schedule entries for sorting
    schedule_entries = []
    for (j, o, m, d, master) in operations:
        s = model.eval(starts[(j, o)]).as_long()
        e = s + d
        master_str = " [MASTER]" if master else ""
        schedule_entries.append((s, j, o, m, d, e, master_str))
    
    schedule_entries.sort()
    print(f"{'Start':>6} {'Job':>4} {'Op':>3} {'Machine':>8} {'Dur':>4} {'End':>5} {'Note':>10}")
    print("-" * 50)
    for s, j, o, m, d, e, note in schedule_entries:
        print(f"{s:>6} {j:>4} {o:>3} {m:>8} {d:>4} {e:>5} {note:>10}")
    
    print(f"\n=== JOB COMPLETION ===")
    for j in sorted(job_info.keys()):
        due, weight = job_info[j]
        job_end_val = max(model.eval(ends[(j, o)]).as_long() for o in job_ops[j])
        tard_val = max(0, job_end_val - due)
        penalty = tard_val * weight
        print(f"Job {j}: Finish={job_end_val}, Due={due}, Tardiness={tard_val}, Weight={weight}, Penalty={penalty}")
    
    print(f"\n=== MACHINE UTILIZATION ===")
    for m in sorted(machine_ops.keys()):
        ops_on_m = []
        for (j, o, d) in machine_ops[m]:
            s = model.eval(starts[(j, o)]).as_long()
            ops_on_m.append((s, s + d, j, o))
        ops_on_m.sort()
        print(f"Machine {m}: {[(s, e, f'J{j}O{o}') for s, e, j, o in ops_on_m]}")
        if m in maintenance:
            ms, me = maintenance[m]
            print(f"  Maintenance window: [{ms}, {me}]")
    
    print(f"\n=== MASTER OPERATOR SCHEDULE ===")
    for (j, o, d) in master_ops:
        s = model.eval(starts[(j, o)]).as_long()
        print(f"  Job {j} Op {o}: [{s}, {s+d})")
    
    # Verify expected optimal makespan
    if makespan_val == 24:
        print(f"\n✓ Makespan matches expected optimal: 24")
    else:
        print(f"\n⚠ Makespan {makespan_val} differs from expected 24")

elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found.")
else:
    print("STATUS: unknown")
    print("Solver returned unknown.")