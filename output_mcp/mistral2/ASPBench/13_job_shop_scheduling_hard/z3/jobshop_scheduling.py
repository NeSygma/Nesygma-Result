from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# --- Data ---
num_jobs = 4
num_machines = 4
max_time = 40

# Job data: (due_date, penalty_weight, list of (duration, machine, requires_master))
job_data = [
    (20, 3, [(4, 1, False), (5, 3, True), (3, 2, False)]),  # Job 1
    (25, 1, [(6, 2, False), (4, 4, False), (2, 1, False), (3, 3, False)]),  # Job 2
    (22, 2, [(7, 4, True), (6, 1, False), (2, 3, False)]),  # Job 3
    (30, 1, [(2, 3, False), (5, 2, False), (3, 4, False), (4, 1, True)]),  # Job 4
]

# Maintenance windows: (machine, start, end)
maintenance = [(2, 10, 11), (4, 15, 16)]

# --- Z3 Model ---
opt = Optimize()

# --- Decision Variables ---
# Start times for each operation
start = [[Int(f"start_{i}_{j}") for j in range(len(job_data[i][2]))] for i in range(num_jobs)]

# Machine assignments for each operation
machine = [[Int(f"machine_{i}_{j}") for j in range(len(job_data[i][2]))] for i in range(num_jobs)]

# Completion times for each operation
end = [[Int(f"end_{i}_{j}") for j in range(len(job_data[i][2]))] for i in range(num_jobs)]

# Completion times for each job
job_end = [Int(f"job_end_{i}") for i in range(num_jobs)]

# Tardiness for each job
tardiness = [Int(f"tardiness_{i}") for i in range(num_jobs)]

# Total weighted tardiness penalty
total_penalty = Int("total_penalty")

# Makespan
makespan = Int("makespan")

# Total cost
total_cost = Int("total_cost")

# --- Constraints ---

# 1. Precedence constraints: operations in a job must be sequential
for i in range(num_jobs):
    for j in range(1, len(job_data[i][2])):
        opt.add(start[i][j] >= end[i][j-1])

# 2. Machine assignments must match the specified machine for each operation
for i in range(num_jobs):
    for j in range(len(job_data[i][2])):
        opt.add(machine[i][j] == job_data[i][2][j][1])

# 3. Completion times
for i in range(num_jobs):
    for j in range(len(job_data[i][2])):
        opt.add(end[i][j] == start[i][j] + job_data[i][2][j][0])

# 4. Job completion times
for i in range(num_jobs):
    opt.add(job_end[i] == end[i][-1])

# 5. Tardiness
for i in range(num_jobs):
    opt.add(tardiness[i] == If(job_end[i] > job_data[i][0],
                              (job_end[i] - job_data[i][0]) * job_data[i][1],
                              0))

# 6. Total weighted tardiness penalty
opt.add(total_penalty == Sum(tardiness))

# 7. Makespan
opt.add(makespan == job_end[0])
for i in range(1, num_jobs):
    opt.add(makespan >= job_end[i])

# 8. Total cost
opt.add(total_cost == makespan + total_penalty)

# 9. Machine exclusivity: no two operations can overlap on the same machine
# Collect operations per machine
ops_per_machine = [[] for _ in range(num_machines)]
for i in range(num_jobs):
    for j in range(len(job_data[i][2])):
        m = machine[i][j]
        ops_per_machine[m].append((i, j))

# Encode no overlap for each machine
for m in range(num_machines):
    ops = ops_per_machine[m]
    for idx1 in range(len(ops)):
        for idx2 in range(idx1 + 1, len(ops)):
            i1, j1 = ops[idx1]
            i2, j2 = ops[idx2]
            # No overlap: either op1 finishes before op2 starts, or op2 finishes before op1 starts
            opt.add(Or(end[i1][j1] <= start[i2][j2], end[i2][j2] <= start[i1][j1]))

# 10. Master Operator exclusivity: at most one operation requiring the Master Operator can be active at any time
master_ops = []
for i in range(num_jobs):
    for j in range(len(job_data[i][2])):
        if job_data[i][2][j][2]:  # requires_master
            master_ops.append((i, j))

for idx1 in range(len(master_ops)):
    for idx2 in range(idx1 + 1, len(master_ops)):
        i1, j1 = master_ops[idx1]
        i2, j2 = master_ops[idx2]
        # No overlap
        opt.add(Or(end[i1][j1] <= start[i2][j2], end[i2][j2] <= start[i1][j1]))

# 11. Maintenance windows: no operation can run during maintenance on its machine
for (m, start_maint, end_maint) in maintenance:
    for i in range(num_jobs):
        for j in range(len(job_data[i][2])):
            if machine[i][j] == m:
                # Operation cannot overlap with maintenance window
                opt.add(Or(end[i][j] <= start_maint, start[i][j] >= end_maint))

# 12. Time horizon: all operations must finish by max_time
for i in range(num_jobs):
    for j in range(len(job_data[i][2])):
        opt.add(start[i][j] >= 0)
        opt.add(end[i][j] <= max_time)

# --- Objective ---
opt.minimize(total_cost)

# --- Check and Print Results ---
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Total Cost:", model[total_cost])
    print("Makespan:", model[makespan])
    print("Total Penalty:", model[total_penalty])
    print("--- Schedule ---")
    for i in range(num_jobs):
        for j in range(len(job_data[i][2])):
            print(f"Job {i+1}, Operation {j+1}: Machine {model[machine[i][j]]}, Start Time {model[start[i][j]]}, Duration {job_data[i][2][j][0]}, End Time {model[end[i][j]]}")
    print("--- Job Completion ---")
    for i in range(num_jobs):
        print(f"Job {i+1}: Finish Time {model[job_end[i]]}, Due Date {job_data[i][0]}, Tardiness {model[tardiness[i]]}")
    print("feasible: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")