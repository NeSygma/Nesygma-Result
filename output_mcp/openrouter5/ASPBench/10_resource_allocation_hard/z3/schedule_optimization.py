from z3 import *

# ============================================================
# DATA
# ============================================================
tasks = list(range(12))  # 0..11 for T1..T12
task_names = ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12"]
duration = [2, 3, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2]

# Required skill: 0=Welding, 1=Assembly, 2=Inspection, 3=Programming
required_skill = [0, 1, 2, 0, 1, 3, 2, 1, 0, 3, 1, 2]

# Machine type: 0=A, 1=B, 2=C
machine_type_needed = [0, 1, 0, 0, 2, 1, 0, 2, 0, 1, 2, 0]

deadline = [6, 8, 7, 9, 10, 9, 8, 11, 12, 11, 10, 13]

# Workers: 5 workers
workers = list(range(5))
worker_names = ["W1","W2","W3","W4","W5"]
# worker skills: [Welding, Assembly, Inspection, Programming]
worker_skills = [
    [True, False, True, False],   # W1
    [False, True, True, False],   # W2
    [False, True, False, True],   # W3
    [True, False, False, True],   # W4
    [True, True, True, False]     # W5
]
worker_cost = [15, 12, 20, 18, 16]

# Machines: 3 machines
machines = list(range(3))
machine_names = ["M1","M2","M3"]
machine_type = [0, 1, 2]  # A, B, C
machine_cost = [3, 2, 4]

# Precedence: (predecessor, successor) using 0-indexed task IDs
precedence = [
    (0, 2),  # T1 -> T3
    (0, 3),  # T1 -> T4
    (1, 4),  # T2 -> T5
    (1, 5),  # T2 -> T6
    (2, 6),  # T3 -> T7
    (3, 8),  # T4 -> T9
    (4, 7),  # T5 -> T8
    (5, 9),  # T6 -> T10
    (6, 11), # T7 -> T12
    (7, 10)  # T8 -> T11
]

# ============================================================
# MODEL
# ============================================================
opt = Optimize()

# Decision variables
start = [Int(f"start_{i}") for i in tasks]
worker_assign = [Int(f"worker_{i}") for i in tasks]
machine_assign = [Int(f"machine_{i}") for i in tasks]

# Makespan variable
makespan = Int("makespan")

# Domain constraints
for i in tasks:
    opt.add(start[i] >= 0)
    opt.add(worker_assign[i] >= 0, worker_assign[i] <= 4)
    opt.add(machine_assign[i] >= 0, machine_assign[i] <= 2)

# 1. Skill compatibility
for i in tasks:
    # worker must have the required skill
    skill = required_skill[i]
    # Or constraint over workers that have this skill
    allowed_workers = [w for w in workers if worker_skills[w][skill]]
    opt.add(Or([worker_assign[i] == w for w in allowed_workers]))

# 2. Machine type compatibility
for i in tasks:
    mtype = machine_type_needed[i]
    allowed_machines = [m for m in machines if machine_type[m] == mtype]
    opt.add(Or([machine_assign[i] == m for m in allowed_machines]))

# 3. Precedence constraints
for pred, succ in precedence:
    opt.add(start[pred] + duration[pred] <= start[succ])

# 4. Deadlines
for i in tasks:
    opt.add(start[i] + duration[i] <= deadline[i])

# 5. Capacity constraints: at any time point, no worker > 3 tasks, no machine > 2 tasks
# We use a discrete time model. The max possible time is max(deadline) = 13
max_time = 13

# For each time point t (0..max_time-1), for each worker w, count tasks active at t
for t in range(max_time):
    for w in workers:
        # Tasks active at time t: start[i] <= t < start[i] + duration[i]
        active_exprs = []
        for i in tasks:
            active = And(start[i] <= t, t < start[i] + duration[i], worker_assign[i] == w)
            active_exprs.append(active)
        # Count using If
        opt.add(Sum([If(active, 1, 0) for active in active_exprs]) <= 3)
    
    for m in machines:
        active_exprs = []
        for i in tasks:
            active = And(start[i] <= t, t < start[i] + duration[i], machine_assign[i] == m)
            active_exprs.append(active)
        opt.add(Sum([If(active, 1, 0) for active in active_exprs]) <= 2)

# 6. Budget constraint
# Total cost = sum over tasks of (worker_cost[worker_assign[i]] + machine_cost[machine_assign[i]]) * duration[i]
# We need to express this symbolically using If-then-else
total_cost_exprs = []
for i in tasks:
    w_cost_expr = Sum([If(worker_assign[i] == w, worker_cost[w], 0) for w in workers])
    m_cost_expr = Sum([If(machine_assign[i] == m, machine_cost[m], 0) for m in machines])
    task_cost = (w_cost_expr + m_cost_expr) * duration[i]
    total_cost_exprs.append(task_cost)

total_cost = Sum(total_cost_exprs)
opt.add(total_cost <= 470)

# 7. Makespan definition
for i in tasks:
    opt.add(makespan >= start[i] + duration[i])

# Objective: minimize makespan
opt.minimize(makespan)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"makespan = {m[makespan]}")
    print(f"total_cost = {m.eval(total_cost)}")
    print()
    print("Schedule:")
    for i in tasks:
        s = m[start[i]].as_long()
        w = m[worker_assign[i]].as_long()
        mac = m[machine_assign[i]].as_long()
        print(f"{task_names[i]}: start={s}, end={s+duration[i]}, worker={worker_names[w]}, machine={machine_names[mac]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")