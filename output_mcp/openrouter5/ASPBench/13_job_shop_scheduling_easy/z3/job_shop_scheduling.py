from z3 import *

# Instance data
# Jobs: each job has operations (op_index, duration, machine)
jobs_data = [
    [(0, 3, 1), (1, 2, 2), (2, 4, 3)],  # Job 1: j1o1->j1o2->j1o3
    [(0, 2, 2), (1, 5, 1), (2, 1, 3)],  # Job 2: j2o1->j2o2->j2o3
    [(0, 4, 3), (1, 1, 1), (2, 3, 2)],  # Job 3: j3o1->j3o2->j3o3
]

num_jobs = len(jobs_data)
num_ops_per_job = len(jobs_data[0])  # 3
num_machines = 3

# Decision variables: start times for each operation
# start[j][k] = start time of operation k of job j
start = [[Int(f"start_j{j+1}_o{k+1}") for k in range(num_ops_per_job)] for j in range(num_jobs)]

# Makespan variable
makespan = Int('makespan')

opt = Optimize()

# Domain constraints: start times are non-negative
for j in range(num_jobs):
    for k in range(num_ops_per_job):
        opt.add(start[j][k] >= 0)

# Precedence constraints: operations within each job must be sequential
for j in range(num_jobs):
    for k in range(num_ops_per_job - 1):
        dur = jobs_data[j][k][1]
        opt.add(start[j][k] + dur <= start[j][k+1])

# Resource constraints: operations on the same machine cannot overlap
# For each pair of operations on the same machine, one must finish before the other starts
# Collect operations by machine
machine_ops = [[] for _ in range(num_machines + 1)]  # 1-indexed machines
for j in range(num_jobs):
    for k in range(num_ops_per_job):
        op_dur = jobs_data[j][k][1]
        op_machine = jobs_data[j][k][2]
        machine_ops[op_machine].append((j, k, op_dur))

# For each machine, add non-overlap constraints between every pair of operations
for m in range(1, num_machines + 1):
    ops = machine_ops[m]
    for i in range(len(ops)):
        for ii in range(i + 1, len(ops)):
            j1, k1, d1 = ops[i]
            j2, k2, d2 = ops[ii]
            # Either op1 before op2, or op2 before op1
            opt.add(Or(
                start[j1][k1] + d1 <= start[j2][k2],
                start[j2][k2] + d2 <= start[j1][k1]
            ))

# Makespan definition: makespan >= completion time of every operation
for j in range(num_jobs):
    for k in range(num_ops_per_job):
        dur = jobs_data[j][k][1]
        opt.add(makespan >= start[j][k] + dur)

# Objective: minimize makespan
opt.minimize(makespan)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"makespan = {m[makespan]}")
    print()
    print("Schedule:")
    print("Job | Op | Machine | Start | Duration | End")
    print("-" * 50)
    for j in range(num_jobs):
        for k in range(num_ops_per_job):
            s = m[start[j][k]].as_long()
            d = jobs_data[j][k][1]
            mach = jobs_data[j][k][2]
            print(f"  {j+1}  | {k+1}  |   m{mach}   |  {s:2d}   |    {d}    | {s+d:2d}")
    print()
    print(f"feasible = True")
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule exists.")
else:
    print("STATUS: unknown")