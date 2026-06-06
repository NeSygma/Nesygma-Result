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

# Helper: Get task duration, skill, machine type, deadline
def get_task_attr(t, attr):
    return tasks[t][["duration", "required_skill", "required_machine_type", "deadline"].index(attr)]

# Helper: Get worker skills and cost
def get_worker_attr(w, attr):
    if attr == "skills":
        return workers[w][0]
    elif attr == "cost":
        return workers[w][1]

# Helper: Get machine type and cost
def get_machine_attr(m, attr):
    if attr == "type":
        return machines[m][0]
    elif attr == "cost":
        return machines[m][1]

# 1. Task Assignment: Each task assigned to exactly one worker and one machine
for t in tasks.keys():
    opt.add(worker_assignment[t] >= 0, worker_assignment[t] < len(workers))
    opt.add(machine_assignment[t] >= 0, machine_assignment[t] < len(machines))

# 2. Skill Compatibility: Worker must have the required skill
for t in tasks.keys():
    required_skill = get_task_attr(t, "required_skill")
    opt.add(Or([worker_assignment[t] == w for w in workers.keys() if required_skill in get_worker_attr(w, "skills")]))

# 3. Machine Type: Machine must be of the required type
for t in tasks.keys():
    required_machine_type = get_task_attr(t, "required_machine_type")
    opt.add(Or([machine_assignment[t] == m for m in machines.keys() if get_machine_attr(m, "type") == required_machine_type]))

# 4. Capacity Limits
# Worker capacity: At any time s, number of tasks assigned to worker w with start_time[t] <= s < start_time[t] + dur[t] <= WORKER_CAPACITY
for w in workers.keys():
    for s in range(TIME_HORIZON):
        overlapping_tasks = []
        for t in tasks.keys():
            dur = get_task_attr(t, "duration")
            opt.add(Implies(And(worker_assignment[t] == w, start_time[t] <= s, s < start_time[t] + dur), True))
            overlapping_tasks.append(And(worker_assignment[t] == w, start_time[t] <= s, s < start_time[t] + dur))
        opt.add(Sum(overlapping_tasks) <= WORKER_CAPACITY)

# Machine capacity: At any time s, number of tasks assigned to machine m with start_time[t] <= s < start_time[t] + dur[t] <= MACHINE_CAPACITY
for m in machines.keys():
    for s in range(TIME_HORIZON):
        overlapping_tasks = []
        for t in tasks.keys():
            dur = get_task_attr(t, "duration")
            opt.add(Implies(And(machine_assignment[t] == m, start_time[t] <= s, s < start_time[t] + dur), True))
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
    worker_cost = get_worker_attr(worker_assignment[t], "cost")
    machine_cost = get_machine_attr(machine_assignment[t], "cost")
    budget_expr.append((worker_cost + machine_cost) * dur)
opt.add(Sum(budget_expr) <= BUDGET_LIMIT)

# Objective: Minimize makespan = max(start_time[t] + dur[t] for all t)
makespan = Int("makespan")
opt.add(makespan == Max([start_time[t] + get_task_attr(t, "duration") for t in tasks.keys()]))
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
        w = model[worker_assignment[t]]
        m = model[machine_assignment[t]]
        s = model[start_time[t]]
        print(f"{t}: worker={w}, machine={m}, start={s}")
    
    # Calculate total cost
    total_cost = 0
    for t in tasks.keys():
        w = model[worker_assignment[t]]
        m = model[machine_assignment[t]]
        dur = get_task_attr(t, "duration")
        worker_cost = get_worker_attr(w, "cost")
        machine_cost = get_machine_attr(m, "cost")
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