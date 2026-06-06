from z3 import *

# Problem data
jobs = [
    {"id": 1, "due": 20, "weight": 3, "operations": [
        {"dur": 4, "machine": 1, "master": False},
        {"dur": 5, "machine": 3, "master": True},
        {"dur": 3, "machine": 2, "master": False}
    ]},
    {"id": 2, "due": 25, "weight": 1, "operations": [
        {"dur": 6, "machine": 2, "master": False},
        {"dur": 4, "machine": 4, "master": False},
        {"dur": 2, "machine": 1, "master": False},
        {"dur": 3, "machine": 3, "master": False}
    ]},
    {"id": 3, "due": 22, "weight": 2, "operations": [
        {"dur": 7, "machine": 4, "master": True},
        {"dur": 6, "machine": 1, "master": False},
        {"dur": 2, "machine": 3, "master": False}
    ]},
    {"id": 4, "due": 30, "weight": 1, "operations": [
        {"dur": 2, "machine": 3, "master": False},
        {"dur": 5, "machine": 2, "master": False},
        {"dur": 3, "machine": 4, "master": False},
        {"dur": 4, "machine": 1, "master": True}
    ]}
]

# Create solver
solver = Optimize()

# Time horizon
TIME_HORIZON = 40

# Create variables for each operation
# We'll use a flat list of operations for easier indexing
operations = []  # list of (job_id, op_index, duration, machine, master)
for job in jobs:
    for op_idx, op in enumerate(job["operations"]):
        operations.append({
            "job": job["id"],
            "op": op_idx,
            "dur": op["dur"],
            "machine": op["machine"],
            "master": op["master"],
            "due": job["due"],
            "weight": job["weight"]
        })

# Create start time variables for each operation
start_vars = []
end_vars = []
for i, op in enumerate(operations):
    start = Int(f"start_{i}")
    end = Int(f"end_{i}")
    # Bound start times
    solver.add(start >= 0)
    solver.add(start <= TIME_HORIZON - op["dur"])
    # End time = start + duration
    solver.add(end == start + op["dur"])
    # End time within horizon
    solver.add(end <= TIME_HORIZON)
    start_vars.append(start)
    end_vars.append(end)

# Precedence constraints within each job
for job in jobs:
    job_ops = [i for i, op in enumerate(operations) if op["job"] == job["id"]]
    for i in range(len(job_ops) - 1):
        prev_idx = job_ops[i]
        next_idx = job_ops[i + 1]
        # Previous operation must finish before next starts
        solver.add(end_vars[prev_idx] <= start_vars[next_idx])

# Machine exclusivity constraints
machines = [1, 2, 3, 4]
for machine in machines:
    machine_ops = [i for i, op in enumerate(operations) if op["machine"] == machine]
    for i in range(len(machine_ops)):
        for j in range(i + 1, len(machine_ops)):
            idx1 = machine_ops[i]
            idx2 = machine_ops[j]
            # Disjunctive constraint: either op1 finishes before op2 starts, or vice versa
            solver.add(Or(
                end_vars[idx1] <= start_vars[idx2],
                end_vars[idx2] <= start_vars[idx1]
            ))

# Master operator exclusivity constraints
master_ops = [i for i, op in enumerate(operations) if op["master"]]
for i in range(len(master_ops)):
    for j in range(i + 1, len(master_ops)):
        idx1 = master_ops[i]
        idx2 = master_ops[j]
        # Disjunctive constraint for master operator
        solver.add(Or(
            end_vars[idx1] <= start_vars[idx2],
            end_vars[idx2] <= start_vars[idx1]
        ))

# Maintenance window constraints
# Machine 2: unavailable from time 10 to 11 (inclusive)
machine2_ops = [i for i, op in enumerate(operations) if op["machine"] == 2]
for idx in machine2_ops:
    # Operation cannot overlap with [10, 11]
    # Either finishes before 10, or starts after 11
    solver.add(Or(
        end_vars[idx] <= 10,
        start_vars[idx] >= 11
    ))

# Machine 4: unavailable from time 15 to 16 (inclusive)
machine4_ops = [i for i, op in enumerate(operations) if op["machine"] == 4]
for idx in machine4_ops:
    # Operation cannot overlap with [15, 16]
    solver.add(Or(
        end_vars[idx] <= 15,
        start_vars[idx] >= 16
    ))

# Calculate makespan (maximum end time)
makespan = Int("makespan")
solver.add(makespan >= 0)
for end in end_vars:
    solver.add(makespan >= end)

# Calculate job completion times and tardiness
job_completion = {}
job_tardiness = {}
job_penalty = {}
total_penalty = Int("total_penalty")
penalty_terms = []

for job in jobs:
    job_id = job["id"]
    # Find last operation of this job
    job_ops = [i for i, op in enumerate(operations) if op["job"] == job_id]
    last_op_idx = job_ops[-1]
    completion = end_vars[last_op_idx]
    
    # Tardiness = max(0, completion - due)
    tardiness = Int(f"tardiness_{job_id}")
    solver.add(tardiness >= 0)
    solver.add(tardiness >= completion - job["due"])
    
    # Weighted penalty
    penalty = Int(f"penalty_{job_id}")
    solver.add(penalty == tardiness * job["weight"])
    
    job_completion[job_id] = completion
    job_tardiness[job_id] = tardiness
    job_penalty[job_id] = penalty
    penalty_terms.append(penalty)

# Total weighted tardiness penalty
solver.add(total_penalty == Sum(penalty_terms))

# Total cost = makespan + total_penalty
total_cost = Int("total_cost")
solver.add(total_cost == makespan + total_penalty)

# Objective: minimize total cost
solver.minimize(total_cost)

# Check and print results
print("Solving scheduling problem...")
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    
    # Extract schedule
    schedule = []
    for i, op in enumerate(operations):
        start_val = model[start_vars[i]].as_long()
        end_val = model[end_vars[i]].as_long()
        schedule.append({
            "job": op["job"],
            "operation": op["op"] + 1,  # 1-indexed for output
            "machine": op["machine"],
            "start": start_val,
            "duration": op["dur"],
            "end": end_val,
            "master": op["master"]
        })
    
    # Extract metrics
    makespan_val = model[makespan].as_long()
    total_penalty_val = model[total_penalty].as_long()
    total_cost_val = model[total_cost].as_long()
    
    # Job completion info
    job_info = []
    for job in jobs:
        job_id = job["id"]
        completion_val = model[job_completion[job_id]].as_long()
        tardiness_val = model[job_tardiness[job_id]].as_long()
        job_info.append({
            "job": job_id,
            "finish_time": completion_val,
            "due_date": job["due"],
            "tardiness": tardiness_val,
            "weight": job["weight"],
            "penalty": tardiness_val * job["weight"]
        })
    
    # Print results
    print("\n=== SCHEDULE ===")
    for s in schedule:
        print(f"Job {s['job']}, Op {s['operation']}: Machine {s['machine']}, "
              f"Start {s['start']}, Duration {s['duration']}, End {s['end']}, "
              f"Master: {s['master']}")
    
    print("\n=== METRICS ===")
    print(f"Makespan: {makespan_val}")
    print(f"Total Weighted Tardiness Penalty: {total_penalty_val}")
    print(f"Total Cost (Makespan + Penalty): {total_cost_val}")
    
    print("\n=== JOB COMPLETION INFO ===")
    for info in job_info:
        print(f"Job {info['job']}: Finish={info['finish_time']}, Due={info['due_date']}, "
              f"Tardiness={info['tardiness']}, Weight={info['weight']}, Penalty={info['penalty']}")
    
    print(f"\nFeasible: True")
    
    # Expected optimal makespan check
    if makespan_val == 24:
        print(f"\n✓ Makespan matches expected optimal value of 24")
    else:
        print(f"\n⚠ Makespan is {makespan_val}, expected 24")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible schedule found with given constraints")
elif result == unknown:
    print("STATUS: unknown")
    print("Solver could not determine satisfiability")
else:
    print("STATUS: unknown")
    print("Unexpected solver result")