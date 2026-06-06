from z3 import *

# Data
# Tasks
tasks = [
    {'id':'T1','duration':2,'skill':'Welding','machine_type':'A','deadline':6},
    {'id':'T2','duration':3,'skill':'Assembly','machine_type':'B','deadline':8},
    {'id':'T3','duration':1,'skill':'Inspection','machine_type':'A','deadline':7},
    {'id':'T4','duration':2,'skill':'Welding','machine_type':'A','deadline':9},
    {'id':'T5','duration':3,'skill':'Assembly','machine_type':'C','deadline':10},
    {'id':'T6','duration':2,'skill':'Programming','machine_type':'B','deadline':9},
    {'id':'T7','duration':1,'skill':'Inspection','machine_type':'A','deadline':8},
    {'id':'T8','duration':2,'skill':'Assembly','machine_type':'C','deadline':11},
    {'id':'T9','duration':3,'skill':'Welding','machine_type':'A','deadline':12},
    {'id':'T10','duration':2,'skill':'Programming','machine_type':'B','deadline':11},
    {'id':'T11','duration':1,'skill':'Assembly','machine_type':'C','deadline':10},
    {'id':'T12','duration':2,'skill':'Inspection','machine_type':'A','deadline':13},
]

# Workers
workers = [
    {'id':'W1','skills':['Welding','Inspection'],'cost':15},
    {'id':'W2','skills':['Assembly','Inspection'],'cost':12},
    {'id':'W3','skills':['Programming','Assembly'],'cost':20},
    {'id':'W4','skills':['Welding','Programming'],'cost':18},
    {'id':'W5','skills':['Assembly','Inspection','Welding'],'cost':16},
]

# Machines
machines = [
    {'id':'M1','type':'A','cost':3},
    {'id':'M2','type':'B','cost':2},
    {'id':'M3','type':'C','cost':4},
]

# Precedence dependencies (indices of tasks)
precedences = [
    (0,2),(0,3),   # T1 before T3,T4
    (1,4),(1,5),   # T2 before T5,T6
    (2,6),         # T3 before T7
    (3,8),         # T4 before T9
    (4,7),         # T5 before T8
    (5,9),         # T6 before T10
    (6,11),        # T7 before T12
    (7,10),        # T8 before T11
]

# Solver
opt = Optimize()

num_tasks = len(tasks)
num_workers = len(workers)
num_machines = len(machines)

# Variables
starts = [Int(f'start_{i}') for i in range(num_tasks)]
workers_assign = [Int(f'worker_{i}') for i in range(num_tasks)]
machines_assign = [Int(f'machine_{i}') for i in range(num_tasks)]
makespan = Int('makespan')

# Domain constraints
for i in range(num_tasks):
    opt.add(starts[i] >= 0)
    opt.add(starts[i] <= tasks[i]['deadline'] - tasks[i]['duration'])
    opt.add(workers_assign[i] >= 0, workers_assign[i] < num_workers)
    opt.add(machines_assign[i] >= 0, machines_assign[i] < num_machines)

# Skill and machine type compatibility
for i, task in enumerate(tasks):
    # Allowed workers
    allowed_workers = [idx for idx,w in enumerate(workers) if task['skill'] in w['skills']]
    opt.add(Or([workers_assign[i] == w for w in allowed_workers]))
    # Allowed machines
    allowed_machines = [idx for idx,m in enumerate(machines) if task['machine_type'] == m['type']]
    opt.add(Or([machines_assign[i] == m for m in allowed_machines]))

# Deadline constraints
for i, task in enumerate(tasks):
    opt.add(starts[i] + task['duration'] <= task['deadline'])

# Precedence constraints
for a,b in precedences:
    opt.add(starts[b] >= starts[a] + tasks[a]['duration'])

# Capacity constraints
max_deadline = max(task['deadline'] for task in tasks)
for t in range(max_deadline):
    # Worker capacity
    for w in range(num_workers):
        active = [If(And(starts[i] <= t, t < starts[i] + tasks[i]['duration']), 1, 0) for i in range(num_tasks) if workers_assign[i] == w]
        # Note: workers_assign[i] == w is a Bool, but we need to use If with that condition
        # Instead, we use a sum over all tasks with a condition on worker assignment
        active = [If(And(workers_assign[i] == w, starts[i] <= t, t < starts[i] + tasks[i]['duration']), 1, 0) for i in range(num_tasks)]
        opt.add(Sum(active) <= 3)
    # Machine capacity
    for m in range(num_machines):
        active = [If(And(machines_assign[i] == m, starts[i] <= t, t < starts[i] + tasks[i]['duration']), 1, 0) for i in range(num_tasks)]
        opt.add(Sum(active) <= 2)

# Budget constraint
budget_expr = Sum([ (workers[w]['cost'] + machines[m]['cost']) * tasks[i]['duration']
                    for i in range(num_tasks)
                    for w in range(num_workers)
                    for m in range(num_machines)
                    if workers_assign[i] == w and machines_assign[i] == m])
opt.add(budget_expr <= 470)

# Makespan constraints
for i, task in enumerate(tasks):
    opt.add(makespan >= starts[i] + task['duration'])

# Objective
opt.minimize(makespan)

# Check
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Extract schedule
    schedule = []
    total_cost = 0
    for i, task in enumerate(tasks):
        s = model[starts[i]].as_long()
        w = model[workers_assign[i]].as_long()
        m = model[machines_assign[i]].as_long()
        finish = s + task['duration']
        cost = (workers[w]['cost'] + machines[m]['cost']) * task['duration']
        total_cost += cost
        schedule.append((task['id'], workers[w]['id'], machines[m]['id'], s, finish))
    # Print schedule
    for t_id, w_id, m_id, s, f in schedule:
        print(f"Task {t_id}: Worker {w_id}, Machine {m_id}, Start {s}, Finish {f}")
    # Print makespan
    makespan_val = model[makespan].as_long()
    print(f"makespan: {makespan_val}")
    print(f"total_cost: {total_cost}")
    print("feasible: True")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")