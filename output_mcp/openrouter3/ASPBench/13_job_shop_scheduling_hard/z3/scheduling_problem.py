from z3 import *

# Problem data
jobs = {
    1: {"due": 20, "weight": 3, "ops": [
        {"duration": 4, "machine": 1, "master": False},
        {"duration": 5, "machine": 3, "master": True},
        {"duration": 3, "machine": 2, "master": False}
    ]},
    2: {"due": 25, "weight": 1, "ops": [
        {"duration": 6, "machine": 2, "master": False},
        {"duration": 4, "machine": 4, "master": False},
        {"duration": 2, "machine": 1, "master": False},
        {"duration": 3, "machine": 3, "master": False}
    ]},
    3: {"due": 22, "weight": 2, "ops": [
        {"duration": 7, "machine": 4, "master": True},
        {"duration": 6, "machine": 1, "master": False},
        {"duration": 2, "machine": 3, "master": False}
    ]},
    4: {"due": 30, "weight": 1, "ops": [
        {"duration": 2, "machine": 3, "master": False},
        {"duration": 5, "machine": 2, "master": False},
        {"duration": 3, "machine": 4, "master": False},
        {"duration": 4, "machine": 1, "master": True}
    ]}
}

# Maintenance windows: machine -> (start, end)
maintenance = {
    2: (10, 11),
    4: (15, 16)
}

TIME_HORIZON = 40

# Create solver
opt = Optimize()

# Operation variables: start[job][op], end[job][op]
start = {}
end = {}
master_ops = []  # List of (job, op) that require master operator

for job_id, job_data in jobs.items():
    start[job_id] = []
    end[job_id] = []
    for op_idx, op_data in enumerate(job_data["ops"]):
        op_name = f"J{job_id}_O{op_idx+1}"
        s = Int(f"start_{op_name}")
        e = Int(f"end_{op_name}")
        start[job_id].append(s)
        end[job_id].append(e)
        
        # Duration constraint
        opt.add(e == s + op_data["duration"])
        
        # Non-negativity and horizon
        opt.add(s >= 0)
        opt.add(e <= TIME_HORIZON)
        
        # Track master operations
        if op_data["master"]:
            master_ops.append((job_id, op_idx))

# 1. Precedence constraints within jobs
for job_id in jobs:
    for i in range(len(jobs[job_id]["ops"]) - 1):
        opt.add(end[job_id][i] <= start[job_id][i+1])

# 2. Machine exclusivity constraints
# Group operations by machine
machine_ops = {1: [], 2: [], 3: [], 4: []}
for job_id in jobs:
    for op_idx, op_data in enumerate(jobs[job_id]["ops"]):
        machine = op_data["machine"]
        machine_ops[machine].append((job_id, op_idx))

# For each machine, ensure no overlapping operations
for machine, ops in machine_ops.items():
    for i in range(len(ops)):
        for j in range(i+1, len(ops)):
            job1, op1 = ops[i]
            job2, op2 = ops[j]
            # Either op1 finishes before op2 starts, or op2 finishes before op1 starts
            opt.add(Or(
                end[job1][op1] <= start[job2][op2],
                end[job2][op2] <= start[job1][op1]
            ))

# 3. Master operator exclusivity
# At most one master operation at any time
for i in range(len(master_ops)):
    for j in range(i+1, len(master_ops)):
        job1, op1 = master_ops[i]
        job2, op2 = master_ops[j]
        opt.add(Or(
            end[job1][op1] <= start[job2][op2],
            end[job2][op2] <= start[job1][op1]
        ))

# 4. Maintenance constraints
# For each operation on a machine with maintenance, ensure it doesn't overlap
for machine, (maint_start, maint_end) in maintenance.items():
    for job_id, op_idx in machine_ops[machine]:
        # Operation cannot be running during maintenance window
        # Either it finishes before maintenance starts, or starts after maintenance ends
        opt.add(Or(
            end[job_id][op_idx] <= maint_start,
            start[job_id][op_idx] >= maint_end + 1  # +1 because maintenance is inclusive
        ))

# 5. Calculate makespan (completion of last operation)
all_ends = []
for job_id in jobs:
    all_ends.extend(end[job_id])

# Create makespan variable and constrain it to be the maximum of all ends
makespan = Int("makespan")
for e in all_ends:
    opt.add(makespan >= e)

# 6. Calculate tardiness for each job
tardiness = {}
for job_id in jobs:
    job_finish = end[job_id][-1]  # Last operation completion
    due = jobs[job_id]["due"]
    weight = jobs[job_id]["weight"]
    
    # Tardiness = max(0, finish - due) * weight
    tard = Int(f"tardiness_{job_id}")
    opt.add(tard >= 0)
    opt.add(tard == If(job_finish > due, (job_finish - due) * weight, 0))
    tardiness[job_id] = tard

# 7. Total cost = makespan + sum of tardiness
total_tardiness = Int("total_tardiness")
opt.add(total_tardiness == Sum([tardiness[job_id] for job_id in jobs]))

total_cost = Int("total_cost")
opt.add(total_cost == makespan + total_tardiness)

# Objective: minimize total cost
opt.minimize(total_cost)

# Check for solution
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract schedule
    schedule = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]["ops"]):
            schedule.append({
                "job": job_id,
                "operation": op_idx + 1,
                "machine": op_data["machine"],
                "start": model[start[job_id][op_idx]].as_long(),
                "duration": op_data["duration"]
            })
    
    # Calculate metrics
    makespan_val = model[makespan].as_long()
    total_penalty_val = model[total_tardiness].as_long()
    total_cost_val = model[total_cost].as_long()
    
    # Job completion info
    job_completion = []
    for job_id in jobs:
        finish = model[end[job_id][-1]].as_long()
        due = jobs[job_id]["due"]
        tard = model[tardiness[job_id]].as_long()
        job_completion.append({
            "job": job_id,
            "finish_time": finish,
            "due_date": due,
            "tardiness": tard
        })
    
    print(f"makespan: {makespan_val}")
    print(f"total_penalty: {total_penalty_val}")
    print(f"total_cost: {total_cost_val}")
    print(f"feasible: True")
    
    print("\nSchedule:")
    for s in schedule:
        print(f"  Job {s['job']}, Op {s['operation']}: Machine {s['machine']}, Start {s['start']}, Duration {s['duration']}")
    
    print("\nJob Completion:")
    for jc in job_completion:
        print(f"  Job {jc['job']}: Finish {jc['finish_time']}, Due {jc['due_date']}, Tardiness {jc['tardiness']}")
    
    # Check if makespan matches expected
    if makespan_val == 24:
        print(f"\n✓ Makespan matches expected value: {makespan_val}")
    else:
        print(f"\n⚠ Makespan is {makespan_val}, expected 24")

elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule exists with the given constraints")
else:
    print("STATUS: unknown")
    print("Solver could not determine feasibility")