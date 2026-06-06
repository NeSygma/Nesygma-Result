from z3 import *

# Data definition
jobs = {
    1: {
        'due': 20,
        'weight': 3,
        'ops': [
            {'dur': 4, 'mach': 1, 'master': False},
            {'dur': 5, 'mach': 3, 'master': True},
            {'dur': 3, 'mach': 2, 'master': False},
        ]
    },
    2: {
        'due': 25,
        'weight': 1,
        'ops': [
            {'dur': 6, 'mach': 2, 'master': False},
            {'dur': 4, 'mach': 4, 'master': False},
            {'dur': 2, 'mach': 1, 'master': False},
            {'dur': 3, 'mach': 3, 'master': False},
        ]
    },
    3: {
        'due': 22,
        'weight': 2,
        'ops': [
            {'dur': 7, 'mach': 4, 'master': True},
            {'dur': 6, 'mach': 1, 'master': False},
            {'dur': 2, 'mach': 3, 'master': False},
        ]
    },
    4: {
        'due': 30,
        'weight': 1,
        'ops': [
            {'dur': 2, 'mach': 3, 'master': False},
            {'dur': 5, 'mach': 2, 'master': False},
            {'dur': 3, 'mach': 4, 'master': False},
            {'dur': 4, 'mach': 1, 'master': True},
        ]
    },
}

# Maintenance windows: machine -> (start, end) inclusive
maintenance = {
    2: (10, 11),
    4: (15, 16),
}

# Create variables for each operation
op_vars = []  # list of dicts with start var and other info
for j_id, j_data in jobs.items():
    for o_idx, op in enumerate(j_data['ops']):
        var = Int(f'start_j{j_id}_o{o_idx+1}')
        op_vars.append({
            'job': j_id,
            'op_idx': o_idx+1,
            'start': var,
            'dur': op['dur'],
            'mach': op['mach'],
            'master': op['master']
        })

opt = Optimize()

# Horizon constraints
HORIZON = 40
for ov in op_vars:
    opt.add(ov['start'] >= 0)
    opt.add(ov['start'] + ov['dur'] <= HORIZON)

# Precedence within each job
for j_id, j_data in jobs.items():
    ops = [ov for ov in op_vars if ov['job'] == j_id]
    ops_sorted = sorted(ops, key=lambda x: x['op_idx'])
    for i in range(len(ops_sorted)-1):
        cur = ops_sorted[i]
        nxt = ops_sorted[i+1]
        opt.add(nxt['start'] >= cur['start'] + cur['dur'])

# Machine exclusivity
for m in [1,2,3,4]:
    ops_on_m = [ov for ov in op_vars if ov['mach'] == m]
    for i in range(len(ops_on_m)):
        for j in range(i+1, len(ops_on_m)):
            a = ops_on_m[i]
            b = ops_on_m[j]
            opt.add(Or(a['start'] + a['dur'] <= b['start'], b['start'] + b['dur'] <= a['start']))

# Master operator exclusivity
master_ops = [ov for ov in op_vars if ov['master']]
for i in range(len(master_ops)):
    for j in range(i+1, len(master_ops)):
        a = master_ops[i]
        b = master_ops[j]
        opt.add(Or(a['start'] + a['dur'] <= b['start'], b['start'] + b['dur'] <= a['start']))

# Maintenance windows constraints
for ov in op_vars:
    m = ov['mach']
    if m in maintenance:
        ws, we = maintenance[m]  # inclusive
        # operation interval [s, s+dur) must not intersect [ws, we+1)
        opt.add(Or(ov['start'] + ov['dur'] <= ws, ov['start'] >= we + 1))

# Makespan variable
makespan = Int('makespan')
# makespan >= each operation end
for ov in op_vars:
    opt.add(makespan >= ov['start'] + ov['dur'])
opt.add(makespan <= HORIZON)

# Job finish times and tardiness penalties
total_penalty = Int('total_penalty')
penalties = []
for j_id, j_data in jobs.items():
    # last operation of job
    ops = [ov for ov in op_vars if ov['job'] == j_id]
    last_op = max(ops, key=lambda x: x['op_idx'])
    finish = last_op['start'] + last_op['dur']
    due = j_data['due']
    weight = j_data['weight']
    tard = Int(f'tard_j{j_id}')
    opt.add(tard == If(finish > due, finish - due, 0))
    penalties.append(tard * weight)

opt.add(total_penalty == Sum(penalties))

# Total cost
total_cost = Int('total_cost')
opt.add(total_cost == makespan + total_penalty)

# Objective: minimize total_cost
opt.minimize(total_cost)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    print('STATUS: sat')
    print('makespan =', m[makespan].as_long())
    print('total_penalty =', m[total_penalty].as_long())
    print('total_cost =', m[total_cost].as_long())
    # Print start times for each operation
    for ov in sorted(op_vars, key=lambda x: (x['job'], x['op_idx'])):
        s = m[ov['start']].as_long()
        print(f"Job {ov['job']} Op {ov['op_idx']}: start={s}, dur={ov['dur']}, mach={ov['mach']}, master={ov['master']}")
else:
    print('STATUS: unsat')