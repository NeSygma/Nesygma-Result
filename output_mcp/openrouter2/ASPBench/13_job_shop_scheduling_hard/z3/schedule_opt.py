from z3 import *

# Define problem data
jobs = {
    1: {
        'due': 20,
        'weight': 3,
        'ops': [
            {'dur': 4, 'machine': 1, 'master': False},
            {'dur': 5, 'machine': 3, 'master': True},
            {'dur': 3, 'machine': 2, 'master': False},
        ]
    },
    2: {
        'due': 25,
        'weight': 1,
        'ops': [
            {'dur': 6, 'machine': 2, 'master': False},
            {'dur': 4, 'machine': 4, 'master': False},
            {'dur': 2, 'machine': 1, 'master': False},
            {'dur': 3, 'machine': 3, 'master': False},
        ]
    },
    3: {
        'due': 22,
        'weight': 2,
        'ops': [
            {'dur': 7, 'machine': 4, 'master': True},
            {'dur': 6, 'machine': 1, 'master': False},
            {'dur': 2, 'machine': 3, 'master': False},
        ]
    },
    4: {
        'due': 30,
        'weight': 1,
        'ops': [
            {'dur': 2, 'machine': 3, 'master': False},
            {'dur': 5, 'machine': 2, 'master': False},
            {'dur': 3, 'machine': 4, 'master': False},
            {'dur': 4, 'machine': 1, 'master': True},
        ]
    }
}

# Horizon
HORIZON = 40

# Create solver
opt = Optimize()

# Variables: start times for each operation
start = {}
for j, data in jobs.items():
    for idx, op in enumerate(data['ops'], start=1):
        var = Int(f'start_{j}_{idx}')
        start[(j, idx)] = var
        # Non-negative and within horizon
        opt.add(var >= 0)
        opt.add(var + op['dur'] <= HORIZON)

# Precedence constraints within each job
for j, data in jobs.items():
    ops = data['ops']
    for idx in range(1, len(ops)):
        opt.add(start[(j, idx+1)] >= start[(j, idx)] + ops[idx-1]['dur'])

# Machine exclusivity
# Build mapping from machine to list of (job, op)
machine_ops = {}
for j, data in jobs.items():
    for idx, op in enumerate(data['ops'], start=1):
        m = op['machine']
        machine_ops.setdefault(m, []).append((j, idx))

for m, ops_list in machine_ops.items():
    for i in range(len(ops_list)):
        for k in range(i+1, len(ops_list)):
            j1, o1 = ops_list[i]
            j2, o2 = ops_list[k]
            dur1 = jobs[j1]['ops'][o1-1]['dur']
            dur2 = jobs[j2]['ops'][o2-1]['dur']
            opt.add(Or(start[(j1, o1)] + dur1 <= start[(j2, o2)],
                       start[(j2, o2)] + dur2 <= start[(j1, o1)]))

# Master operator exclusivity
master_ops = []
for j, data in jobs.items():
    for idx, op in enumerate(data['ops'], start=1):
        if op['master']:
            master_ops.append((j, idx))

for i in range(len(master_ops)):
    for k in range(i+1, len(master_ops)):
        j1, o1 = master_ops[i]
        j2, o2 = master_ops[k]
        dur1 = jobs[j1]['ops'][o1-1]['dur']
        dur2 = jobs[j2]['ops'][o2-1]['dur']
        opt.add(Or(start[(j1, o1)] + dur1 <= start[(j2, o2)],
                   start[(j2, o2)] + dur2 <= start[(j1, o1)]))

# Maintenance windows
# Machine 2: 10-11 inclusive -> no overlap with [10,12)
for j, o in machine_ops.get(2, []):
    dur = jobs[j]['ops'][o-1]['dur']
    opt.add(Or(start[(j, o)] + dur <= 10,
               start[(j, o)] >= 12))
# Machine 4: 15-16 inclusive -> no overlap with [15,17)
for j, o in machine_ops.get(4, []):
    dur = jobs[j]['ops'][o-1]['dur']
    opt.add(Or(start[(j, o)] + dur <= 15,
               start[(j, o)] >= 17))

# Makespan variable
M = Int('makespan')
# Constraint: makespan >= finish of all ops
for (j, o), var in start.items():
    dur = jobs[j]['ops'][o-1]['dur']
    opt.add(M >= var + dur)

# Compute weighted tardiness for each job
job_finish = {}
job_tardiness = {}
job_penalty = {}
for j, data in jobs.items():
    last_op = len(data['ops'])
    dur_last = data['ops'][last_op-1]['dur']
    finish = start[(j, last_op)] + dur_last
    job_finish[j] = finish
    tard = If(finish > data['due'], finish - data['due'], 0)
    job_tardiness[j] = tard
    job_penalty[j] = tard * data['weight']

total_penalty = Sum([job_penalty[j] for j in jobs])

# Total cost
total_cost = M + total_penalty
opt.minimize(total_cost)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    # Extract values
    makespan_val = model[M].as_long()
    total_pen_val = model.evaluate(total_penalty, model_completion=True).as_long()
    total_cost_val = model.evaluate(total_cost, model_completion=True).as_long()
    # Print status
    print("STATUS: sat")
    # Schedule
    print("schedule:")
    for j in sorted(jobs):
        for idx, op in enumerate(jobs[j]['ops'], start=1):
            s = model[start[(j, idx)]].as_long()
            print(f"Job {j} Op {idx} Machine {op['machine']} Start {s} Duration {op['dur']}")
    # Metrics
    print("metrics:")
    print(f"makespan: {makespan_val}")
    print(f"total_penalty: {total_pen_val}")
    print(f"total_cost: {total_cost_val}")
    # Job completion
    print("job_completion:")
    for j in sorted(jobs):
        finish_val = model[job_finish[j]].as_long()
        due = jobs[j]['due']
        tard_val = model[job_tardiness[j]].as_long()
        print(f"Job {j} Finish {finish_val} Due {due} Tardiness {tard_val}")
    # Feasible
    print("feasible: True")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")