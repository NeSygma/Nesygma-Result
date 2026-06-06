from z3 import *

# ============================================================
# DATA
# ============================================================
H = 40  # time horizon

# Jobs: (due_date, penalty_weight)
jobs_data = {
    1: {"due": 20, "weight": 3},
    2: {"due": 25, "weight": 1},
    3: {"due": 22, "weight": 2},
    4: {"due": 30, "weight": 1},
}

# Operations: (job, op_idx, duration, machine, requires_master)
# op indices are 0-based within each job
operations = [
    # Job 1: 3 ops
    (1, 0, 4, 1, False),
    (1, 1, 5, 3, True),
    (1, 2, 3, 2, False),
    # Job 2: 4 ops
    (2, 0, 6, 2, False),
    (2, 1, 4, 4, False),
    (2, 2, 2, 1, False),
    (2, 3, 3, 3, False),
    # Job 3: 3 ops
    (3, 0, 7, 4, True),
    (3, 1, 6, 1, False),
    (3, 2, 2, 3, False),
    # Job 4: 4 ops
    (4, 0, 2, 3, False),
    (4, 1, 5, 2, False),
    (4, 2, 3, 4, False),
    (4, 3, 4, 1, True),
]

N_ops = len(operations)

# Maintenance windows: (machine, start, end) inclusive
maintenance = [
    (2, 10, 11),
    (4, 15, 16),
]

# ============================================================
# VARIABLES
# ============================================================
solver = Solver()

# Start times for each operation
start = [Int(f"start_{i}") for i in range(N_ops)]

# For each operation, we know its duration, machine, job, etc.
durations = [op[2] for op in operations]
machines = [op[3] for op in operations]
jobs = [op[0] for op in operations]
op_indices = [op[1] for op in operations]
requires_master = [op[4] for op in operations]

# ============================================================
# DOMAIN CONSTRAINTS
# ============================================================
for i in range(N_ops):
    solver.add(start[i] >= 0)
    solver.add(start[i] + durations[i] <= H)

# ============================================================
# PRECEDENCE: operations within each job must be sequential
# ============================================================
# Group operations by job
from collections import defaultdict
job_ops = defaultdict(list)
for i, op in enumerate(operations):
    job_ops[op[0]].append(i)

for jid, op_list in job_ops.items():
    # Sort by operation index
    op_list_sorted = sorted(op_list, key=lambda i: op_indices[i])
    for k in range(len(op_list_sorted) - 1):
        i_prev = op_list_sorted[k]
        i_next = op_list_sorted[k+1]
        solver.add(start[i_prev] + durations[i_prev] <= start[i_next])

# ============================================================
# MACHINE EXCLUSIVITY: no two ops on same machine overlap
# ============================================================
for i in range(N_ops):
    for j in range(i+1, N_ops):
        if machines[i] == machines[j]:
            # Non-overlap: i before j OR j before i
            solver.add(Or(
                start[i] + durations[i] <= start[j],
                start[j] + durations[j] <= start[i]
            ))

# ============================================================
# MASTER OPERATOR EXCLUSIVITY
# ============================================================
master_ops = [i for i in range(N_ops) if requires_master[i]]
for idx_a in range(len(master_ops)):
    for idx_b in range(idx_a+1, len(master_ops)):
        i = master_ops[idx_a]
        j = master_ops[idx_b]
        solver.add(Or(
            start[i] + durations[i] <= start[j],
            start[j] + durations[j] <= start[i]
        ))

# ============================================================
# MAINTENANCE WINDOWS
# ============================================================
# For each operation on a machine with a maintenance window,
# the operation must not overlap with the window.
# i.e., operation finishes before window starts OR starts after window ends
for (m, win_start, win_end) in maintenance:
    for i in range(N_ops):
        if machines[i] == m:
            # Operation must be entirely outside the maintenance window
            solver.add(Or(
                start[i] + durations[i] <= win_start,
                start[i] >= win_end + 1  # win_end is inclusive, so next time unit is win_end+1
            ))

# ============================================================
# OBJECTIVE: Minimize Makespan + Total Weighted Tardiness
# ============================================================

# Makespan: completion time of last operation
makespan = Int('makespan')
for i in range(N_ops):
    solver.add(makespan >= start[i] + durations[i])

# Job completion times = start of last op + duration of last op
job_completion = {}
for jid in [1, 2, 3, 4]:
    last_op_idx = max(job_ops[jid], key=lambda i: op_indices[i])
    job_completion[jid] = Int(f"completion_{jid}")
    solver.add(job_completion[jid] == start[last_op_idx] + durations[last_op_idx])

# Tardiness and penalty
total_penalty = Int('total_penalty')
penalty_terms = []
for jid in [1, 2, 3, 4]:
    due = jobs_data[jid]["due"]
    weight = jobs_data[jid]["weight"]
    tardiness = Int(f"tardiness_{jid}")
    solver.add(tardiness == If(job_completion[jid] > due, job_completion[jid] - due, 0))
    penalty_terms.append(tardiness * weight)

solver.add(total_penalty == Sum(penalty_terms))

# Total cost
total_cost = Int('total_cost')
solver.add(total_cost == makespan + total_penalty)

# ============================================================
# OPTIMIZATION
# ============================================================
opt = Optimize()
# Add all constraints from solver to opt
for c in solver.assertions():
    opt.add(c)

# Minimize total cost
opt.minimize(total_cost)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Makespan = {m[makespan]}")
    print(f"Total Penalty = {m[total_penalty]}")
    print(f"Total Cost = {m[total_cost]}")
    print()
    print("Schedule (job, op, machine, start, duration, end):")
    for i in range(N_ops):
        s = m[start[i]].as_long()
        d = durations[i]
        print(f"  Job {jobs[i]} Op {op_indices[i]+1}: Machine {machines[i]}, Start={s}, Duration={d}, End={s+d}")
    print()
    print("Job Completion:")
    for jid in [1, 2, 3, 4]:
        c = m[job_completion[jid]].as_long()
        due = jobs_data[jid]["due"]
        w = jobs_data[jid]["weight"]
        tard = max(0, c - due)
        print(f"  Job {jid}: Finish={c}, Due={due}, Tardiness={tard}, Penalty={tard * w}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")