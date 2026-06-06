from z3 import *

# Data
tasks = {
    'T1': {'dur': 2, 'skill': 'Welding', 'm_type': 'A', 'deadline': 6},
    'T2': {'dur': 3, 'skill': 'Assembly', 'm_type': 'B', 'deadline': 8},
    'T3': {'dur': 1, 'skill': 'Inspection', 'm_type': 'A', 'deadline': 7},
    'T4': {'dur': 2, 'skill': 'Welding', 'm_type': 'A', 'deadline': 9},
    'T5': {'dur': 3, 'skill': 'Assembly', 'm_type': 'C', 'deadline': 10},
    'T6': {'dur': 2, 'skill': 'Programming', 'm_type': 'B', 'deadline': 9},
    'T7': {'dur': 1, 'skill': 'Inspection', 'm_type': 'A', 'deadline': 8},
    'T8': {'dur': 2, 'skill': 'Assembly', 'm_type': 'C', 'deadline': 11},
    'T9': {'dur': 3, 'skill': 'Welding', 'm_type': 'A', 'deadline': 12},
    'T10': {'dur': 2, 'skill': 'Programming', 'm_type': 'B', 'deadline': 11},
    'T11': {'dur': 1, 'skill': 'Assembly', 'm_type': 'C', 'deadline': 10},
    'T12': {'dur': 2, 'skill': 'Inspection', 'm_type': 'A', 'deadline': 13},
}

workers = {
    'W1': {'skills': ['Welding', 'Inspection'], 'cost': 15},
    'W2': {'skills': ['Assembly', 'Inspection'], 'cost': 12},
    'W3': {'skills': ['Programming', 'Assembly'], 'cost': 20},
    'W4': {'skills': ['Welding', 'Programming'], 'cost': 18},
    'W5': {'skills': ['Assembly', 'Inspection', 'Welding'], 'cost': 16},
}

machines = {
    'M1': {'type': 'A', 'cost': 3},
    'M2': {'type': 'B', 'cost': 2},
    'M3': {'type': 'C', 'cost': 4},
}

precedence = [
    ('T1', 'T3'), ('T1', 'T4'),
    ('T2', 'T5'), ('T2', 'T6'),
    ('T3', 'T7'),
    ('T4', 'T9'),
    ('T5', 'T8'),
    ('T6', 'T10'),
    ('T7', 'T12'),
    ('T8', 'T11')
]

task_ids = list(tasks.keys())
worker_ids = list(workers.keys())
machine_ids = list(machines.keys())

# Optimization
opt = Optimize()

# Variables
start = {tid: Int(f'start_{tid}') for tid in task_ids}
worker_assign = {tid: Int(f'worker_{tid}') for tid in task_ids} # 0-4
machine_assign = {tid: Int(f'machine_{tid}') for tid in task_ids} # 0-2

# Domain constraints
for tid in task_ids:
    opt.add(start[tid] >= 0)
    opt.add(start[tid] + tasks[tid]['dur'] <= tasks[tid]['deadline'])
    opt.add(worker_assign[tid] >= 0, worker_assign[tid] < len(worker_ids))
    opt.add(machine_assign[tid] >= 0, machine_assign[tid] < len(machine_ids))

# Skill and Machine compatibility
for tid in task_ids:
    # Skill
    skill_req = tasks[tid]['skill']
    opt.add(Or([worker_assign[tid] == i for i, wid in enumerate(worker_ids) if skill_req in workers[wid]['skills']]))
    # Machine
    m_type_req = tasks[tid]['m_type']
    opt.add(Or([machine_assign[tid] == i for i, mid in enumerate(machine_ids) if machines[mid]['type'] == m_type_req]))

# Precedence
for t1, t2 in precedence:
    opt.add(start[t1] + tasks[t1]['dur'] <= start[t2])

# Makespan
makespan = Int('makespan')
for tid in task_ids:
    opt.add(makespan >= start[tid] + tasks[tid]['dur'])

# Time horizon
T_MAX = 15
for t in range(T_MAX):
    # Worker capacity (max 3)
    for i in range(len(worker_ids)):
        opt.add(Sum([If(And(start[tid] <= t, t < start[tid] + tasks[tid]['dur'], worker_assign[tid] == i), 1, 0) for tid in task_ids]) <= 3)
    # Machine capacity (max 2)
    for i in range(len(machine_ids)):
        opt.add(Sum([If(And(start[tid] <= t, t < start[tid] + tasks[tid]['dur'], machine_assign[tid] == i), 1, 0) for tid in task_ids]) <= 2)

# Budget
# Use If-Else to map symbolic worker/machine index to cost
def get_worker_cost(idx):
    return Sum([If(idx == i, workers[wid]['cost'], 0) for i, wid in enumerate(worker_ids)])

def get_machine_cost(idx):
    return Sum([If(idx == i, machines[mid]['cost'], 0) for i, mid in enumerate(machine_ids)])

total_cost = Sum([
    (get_worker_cost(worker_assign[tid]) + get_machine_cost(machine_assign[tid])) * tasks[tid]['dur']
    for tid in task_ids
])
opt.add(total_cost <= 470)

opt.minimize(makespan)

if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"makespan: {m[makespan]}")
    print(f"total_cost: {m.eval(total_cost)}")
    for tid in task_ids:
        w_idx = m[worker_assign[tid]].as_long()
        m_idx = m[machine_assign[tid]].as_long()
        print(f"{tid}: start={m[start[tid]]}, worker={worker_ids[w_idx]}, machine={machine_ids[m_idx]}")
else:
    print("STATUS: unsat")