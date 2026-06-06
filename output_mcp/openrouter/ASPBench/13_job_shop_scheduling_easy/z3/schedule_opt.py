from z3 import *

# Define data
jobs = {
    (1,1): {'machine':1, 'duration':3},
    (1,2): {'machine':2, 'duration':2},
    (1,3): {'machine':3, 'duration':4},
    (2,1): {'machine':2, 'duration':2},
    (2,2): {'machine':1, 'duration':5},
    (2,3): {'machine':3, 'duration':1},
    (3,1): {'machine':3, 'duration':4},
    (3,2): {'machine':1, 'duration':1},
    (3,3): {'machine':2, 'duration':3},
}

# Create start time variables
starts = {op: Int(f's_{op[0]}_{op[1]}') for op in jobs}

opt = Optimize()

# Add non-negative start constraints
for var in starts.values():
    opt.add(var >= 0)

# Precedence constraints within each job
for job in [1,2,3]:
    for op in [1,2]:
        cur = (job, op)
        nxt = (job, op+1)
        opt.add(starts[cur] + jobs[cur]['duration'] <= starts[nxt])

# Resource constraints: no overlap on same machine
# Gather ops per machine
ops_by_machine = {1: [], 2: [], 3: []}
for op, info in jobs.items():
    ops_by_machine[info['machine']].append(op)

for m, ops in ops_by_machine.items():
    for i in range(len(ops)):
        for j in range(i+1, len(ops)):
            op_i = ops[i]
            op_j = ops[j]
            dur_i = jobs[op_i]['duration']
            dur_j = jobs[op_j]['duration']
            si = starts[op_i]
            sj = starts[op_j]
            # either i finishes before j starts or vice versa
            opt.add(Or(si + dur_i <= sj, sj + dur_j <= si))

# Makespan variable
makespan = Int('makespan')
opt.add(makespan >= 0)
for op, info in jobs.items():
    opt.add(makespan >= starts[op] + info['duration'])

# Objective: minimize makespan
opt.minimize(makespan)

res = opt.check()
if res == sat:
    m = opt.model()
    ms_val = m.eval(makespan).as_long()
    print("STATUS: sat")
    print(f"makespan = {ms_val}")
    print(f"feasible = True")
    # Print schedule entries sorted by job then operation
    for job in [1,2,3]:
        for op in [1,2,3]:
            key = (job, op)
            start_val = m.eval(starts[key]).as_long()
            machine = jobs[key]['machine']
            duration = jobs[key]['duration']
            print(f"job = {job}, operation = {op}, machine = {machine}, start = {start_val}, duration = {duration}")
else:
    print("STATUS: unsat")
    print("feasible = False")