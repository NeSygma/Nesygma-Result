from z3 import *

# Problem data

# Tasks: (duration, required_skill, required_machine_type, deadline)
tasks = {
    "T1": (2, "Welding", "A", 6),
    "T2": (3, "Assembly", "B", 8),
    "T3": (1, "Inspection", "A", 7),
    "T4": (2, "Welding", "A", 9),
    "T5": (3, "Assembly", "C", 10),
    "T6": (2, "Programming", "B", 9),
    "T7": (1, "Inspection", "A", 8),
    "T8": (2, "Assembly", "C", 11),
    "T9": (3, "Welding", "A", 12),
    "T10": (2, "Programming", "B", 11),
    "T11": (1, "Assembly", "C", 10),
    "T12": (2, "Inspection", "A", 13),
}

# Workers: (skills, hourly_cost)
workers = {
    "W1": (["Welding", "Inspection"], 15),
    "W2": (["Assembly", "Inspection"], 12),
    "W3": (["Programming", "Assembly"], 20),
    "W4": (["Welding", "Programming"], 18),
    "W5": (["Assembly", "Inspection", "Welding"], 16),
}

# Machines: (type, hourly_cost)
machines = {
    "M1": ("A", 3),
    "M2": ("B", 2),
    "M3": ("C", 4),
}

# Precedence dependencies: (before, after)
precedence = [
    ("T1", "T3"),
    ("T1", "T4"),
    ("T2", "T5"),
    ("T2", "T6"),
    ("T3", "T7"),
    ("T4", "T9"),
    ("T5", "T8"),
    ("T6", "T10"),
    ("T7", "T12"),
    ("T8", "T11"),
]

# Global constraints
BUDGET_LIMIT = 470
WORKER_CAPACITY = 3
MACHINE_CAPACITY = 2

# Time horizon (bounded for optimization)
TIME_HORIZON = 15

# Initialize solver
opt = Optimize()

# Declare variables
start_time = {t: Int(f"start_{t}") for t in tasks.keys()}
worker_assignment = {t: Int(f"worker_{t}") for t in tasks.keys()}
machine_assignment = {t: Int(f"machine_{t}") for t in tasks.keys()}

# Map worker and machine names to integer indices
worker_list = list(workers.keys())
machine_list = list(machines.keys())

# Helper: Get task duration, skill, machine type, deadline
def get_task_attr(t, attr):
    return tasks[t][["duration", "required_skill", "required_machine_type", "deadline"].index(attr)]

# Helper: Get worker skills and cost (using Or-Loop pattern for symbolic indexing)
def get_worker_skill(w, skill):
    # w is a Z3 Int variable representing worker index
    # Return a Z3 expression: True if worker w has the skill
    return Or([And(w == i, skill in workers[worker_list[i]][0]) for i in range(len(worker_list))])

def get_worker_cost(w):
    # w is a Z3 Int variable representing worker index
    # Return a Z3 expression for the cost of worker w
    return If(w == 0, 15, If(w == 1, 12, If(w == 2, 20, If(w == 3, 18, 16))))

# Helper: Get machine type and cost (using Or-Loop pattern for symbolic indexing)
def get_machine_type(m, req_type):
    # m is a Z3 Int variable representing machine index
    # Return a Z3 expression: True if machine m is of type req_type
    return Or([And(m == i, machines[machine_list[i]][0] == req_type) for i in range(len(machine_list))])

def get_machine_cost(m):
    # m is a Z3 Int variable representing machine index
    # Return a Z3 expression for the cost of machine m
    return If(m == 0, 3, If(m == 1, 2, 4))

# 1. Task Assignment: Each task assigned to exactly one worker and one machine
for t in tasks.keys():
    opt.add(worker_assignment[t] >= 0, worker_assignment[t] < len(workers))
    opt.add(machine_assignment[t] >= 0, machine_assignment[t] < len(machines))

# 2. Skill Compatibility: Worker must have the required skill
for t in tasks.keys():
    required_skill = get_task_attr(t, "required_skill")
    opt.add(get_worker_skill(worker_assignment[t], required_skill))

# 3. Machine Type: Machine must be of the required type
for t in tasks.keys():
    required_machine_type = get_task_attr(t, "required_machine_type")
    opt.add(get_machine_type(machine_assignment[t], required_machine_type))

# 4. Capacity Limits
# Worker capacity: At any time s, number of tasks assigned to worker w with start_time[t] <= s < start_time[t] + dur[t] <= WORKER_CAPACITY
for w in range(len(worker_list)):
    for s in range(TIME_HORIZON):
        overlapping_tasks = []
        for t in tasks.keys():
            dur = get_task_attr(t, "duration")
            overlapping_tasks.append(And(worker_assignment[t] == w, start_time[t] <= s, s < start_time[t] + dur))
        opt.add(Sum(overlapping_tasks) <= WORKER_CAPACITY)

# Machine capacity: At any time s, number of tasks assigned to machine m with start_time[t] <= s < start_time[t] + dur[t] <= MACHINE_CAPACITY
for m in range(len(machine_list)):
    for s in range(TIME_HORIZON):
        overlapping_tasks = []
        for t in tasks.keys():
            dur = get_task_attr(t, "duration")
            overlapping_tasks.append(And(machine_assignment[t] == m, start_time[t] <= s, s < start_time[t] + dur))
        opt.add(Sum(overlapping_tasks) <= MACHINE_CAPACITY)

# 5. Precedence: If t1 must precede t2, then start_time[t2] >= start_time[t1] + dur[t1]
for (t1, t2) in precedence:
    dur1 = get_task_attr(t1, "duration")
    opt.add(start_time[t2] >= start_time[t1] + dur1)

# 6. Deadlines: start_time[t] + dur[t] <= deadline[t]
for t in tasks.keys():
    deadline = get_task_attr(t, "deadline")
    dur = get_task_attr(t, "duration")
    opt.add(start_time[t] + dur <= deadline)

# 7. Budget: Sum over all tasks of (worker_cost + machine_cost) * dur[t] <= BUDGET_LIMIT
budget_expr = []
for t in tasks.keys():
    w = worker_assignment[t]
    m = machine_assignment[t]
    dur = get_task_attr(t, "duration")
    worker_cost = get_worker_cost(w)
    machine_cost = get_machine_cost(m)
    budget_expr.append((worker_cost + machine_cost) * dur)
opt.add(Sum(budget_expr) <= BUDGET_LIMIT)

# Objective: Minimize makespan = max(start_time[t] + dur[t] for all t)
makespan = Int("makespan")
finish_times = [start_time[t] + get_task_attr(t, "duration") for t in tasks.keys()]
opt.add(makespan >= f for f in finish_times)
opt.minimize(makespan)

# Check and print result
BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal makespan:", model[makespan])
    print("Task assignments:")
    for t in tasks.keys():
        w_idx = model[worker_assignment[t]].as_long()
        m_idx = model[machine_assignment[t]].as_long()
        s = model[start_time[t]]
        print(f"{t}: worker={worker_list[w_idx]}, machine={machine_list[m_idx]}, start={s}")
    
    # Calculate total cost
    total_cost = 0
    for t in tasks.keys():
        w_idx = model[worker_assignment[t]].as_long()
        m_idx = model[machine_assignment[t]].as_long()
        dur = get_task_attr(t, "duration")
        worker_cost = workers[worker_list[w_idx]][1]
        machine_cost = machines[machine_list[m_idx]][1]
        task_cost = (worker_cost + machine_cost) * dur
        total_cost += task_cost
    print("Total cost:", total_cost)
    print("Feasible: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")