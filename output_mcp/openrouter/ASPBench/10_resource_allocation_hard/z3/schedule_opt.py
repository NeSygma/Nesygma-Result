from z3 import *

# Data definitions
tasks = ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12"]
num_tasks = len(tasks)
# durations
duration = [2,3,1,2,3,2,1,2,3,2,1,2]
# required skill per task
skill_req = ["Welding","Assembly","Inspection","Welding","Assembly","Programming","Inspection","Assembly","Welding","Programming","Assembly","Inspection"]
# required machine type per task
machine_type_req = ["A","B","A","A","C","B","A","C","A","B","C","A"]
# deadlines
deadline = [6,8,7,9,10,9,8,11,12,11,10,13]

# Workers
workers = ["W1","W2","W3","W4","W5"]
worker_cost = [15,12,20,18,16]
worker_skills = [
    {"Welding","Inspection"},          # W1
    {"Assembly","Inspection"},          # W2
    {"Programming","Assembly"},         # W3
    {"Welding","Programming"},          # W4
    {"Assembly","Inspection","Welding"} # W5
]

# Machines
machines = ["M1","M2","M3"]
machine_type = ["A","B","C"]
machine_cost = [3,2,4]

# Precedence list (indices)
precedence = [
    (0,2), # T1 -> T3
    (0,3), # T1 -> T4
    (1,4), # T2 -> T5
    (1,5), # T2 -> T6
    (2,6), # T3 -> T7
    (3,8), # T4 -> T9
    (4,7), # T5 -> T8
    (5,9), # T6 -> T10
    (6,11),# T7 -> T12
    (7,10) # T8 -> T11
]

opt = Optimize()

# Decision variables
start = [Int(f"start_{i}") for i in range(num_tasks)]
worker = [Int(f"worker_{i}") for i in range(num_tasks)]
machine = [Int(f"machine_{i}") for i in range(num_tasks)]

makespan = Int("makespan")

# Basic constraints
for i in range(num_tasks):
    opt.add(start[i] >= 0)
    opt.add(start[i] + duration[i] <= deadline[i])
    opt.add(worker[i] >= 0, worker[i] < len(workers))
    opt.add(machine[i] >= 0, machine[i] < len(machines))
    # skill compatibility
    allowed_workers = [w for w in range(len(workers)) if skill_req[i] in worker_skills[w]]
    opt.add(Or([worker[i] == w for w in allowed_workers]))
    # machine type compatibility
    allowed_machines = [m for m in range(len(machines)) if machine_type[m] == machine_type_req[i]]
    opt.add(Or([machine[i] == m for m in allowed_machines]))

# Precedence constraints
for a,b in precedence:
    opt.add(start[b] >= start[a] + duration[a])

# Makespan constraints
for i in range(num_tasks):
    opt.add(makespan >= start[i] + duration[i])
opt.add(makespan <= max(deadline))

# Budget constraint using piecewise cost
cost_terms = []
for i in range(num_tasks):
    # worker cost component
    wc = Sum([If(worker[i] == w, worker_cost[w], 0) for w in range(len(workers))])
    # machine cost component
    mc = Sum([If(machine[i] == m, machine_cost[m], 0) for m in range(len(machines))])
    cost_terms.append((wc + mc) * duration[i])

total_cost = Sum(cost_terms)
opt.add(total_cost <= 470)

# Capacity constraints for each time point up to max deadline
max_time = max(deadline)
for t in range(max_time+1):
    for w in range(len(workers)):
        overlapping = [If(And(start[i] <= t, t < start[i] + duration[i], worker[i] == w), 1, 0) for i in range(num_tasks)]
        opt.add(Sum(overlapping) <= 3)
    for m in range(len(machines)):
        overlapping_m = [If(And(start[i] <= t, t < start[i] + duration[i], machine[i] == m), 1, 0) for i in range(num_tasks)]
        opt.add(Sum(overlapping_m) <= 2)

# Objective: minimize makespan
opt.minimize(makespan)

# Solve
if opt.check() == sat:
    model = opt.model()
    print("STATUS: sat")
    for i in range(num_tasks):
        s = model.eval(start[i]).as_long()
        w = model.eval(worker[i]).as_long()
        m = model.eval(machine[i]).as_long()
        print(f"{tasks[i]} start={s} worker={workers[w]} machine={machines[m]}")
    mk = model.eval(makespan).as_long()
    tc = model.eval(total_cost).as_long()
    print(f"makespan = {mk}")
    print(f"total_cost = {tc}")
else:
    print("STATUS: unsat")