from z3 import *

# ============================================================
# DATA
# ============================================================
N = 12
tasks = ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12']
durations = [2, 3, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2]

# Skills: Welding=0, Assembly=1, Inspection=2, Programming=3
req_skills = [0, 1, 2, 0, 1, 3, 2, 1, 0, 3, 1, 2]

# Machine types: A=0, B=1, C=2
req_machines = [0, 1, 0, 0, 2, 1, 0, 2, 0, 1, 2, 0]

deadlines = [6, 8, 7, 9, 10, 9, 8, 11, 12, 11, 10, 13]

# Worker skill matrix: worker_has_skill[w][s] = True if worker w has skill s
worker_has_skill = [
    [True,  False, True,  False],  # W1: Welding, Inspection
    [False, True,  True,  False],  # W2: Assembly, Inspection
    [False, True,  False, True],   # W3: Programming, Assembly
    [True,  False, False, True],   # W4: Welding, Programming
    [True,  True,  True,  False],  # W5: Assembly, Inspection, Welding
]
worker_costs = [15, 12, 20, 18, 16]

# Machine costs by type index: A->3, B->2, C->4
machine_costs = [3, 2, 4]

# Precedence: (predecessor_index, successor_index)
precedences = [
    (0, 2), (0, 3),   # T1 -> T3, T4
    (1, 4), (1, 5),   # T2 -> T5, T6
    (2, 6),            # T3 -> T7
    (3, 8),            # T4 -> T9
    (4, 7),            # T5 -> T8
    (5, 9),            # T6 -> T10
    (6, 11),           # T7 -> T12
    (7, 10),           # T8 -> T11
]

W = 5       # number of workers
M_cnt = 3   # number of machines
T_max = max(deadlines)  # 13

# ============================================================
# SOLVER
# ============================================================
opt = Optimize()
opt.set(timeout=180000)  # 3 min timeout

# Decision variables
start  = [Int(f'start_{i}')  for i in range(N)]
worker = [Int(f'worker_{i}') for i in range(N)]

# Domain constraints
for i in range(N):
    opt.add(start[i] >= 0)
    opt.add(worker[i] >= 0, worker[i] < W)

# ---- Skill compatibility ----
for i in range(N):
    skill = req_skills[i]
    compatible = [w for w in range(W) if worker_has_skill[w][skill]]
    opt.add(Or([worker[i] == w for w in compatible]))

# ---- Machine type compatibility (deterministic: one machine per type) ----
# M1 -> type A (0), M2 -> type B (1), M3 -> type C (2)
# So machine assignment is fixed by req_machines[i]

# ---- Precedence constraints ----
for (b, a) in precedences:
    opt.add(start[a] >= start[b] + durations[b])

# ---- Deadline constraints ----
for i in range(N):
    opt.add(start[i] + durations[i] <= deadlines[i])

# ---- Worker capacity: at most 3 simultaneous tasks per worker ----
for w in range(W):
    for t in range(T_max + 1):
        active = [If(And(worker[i] == w,
                         start[i] <= t,
                         t < start[i] + durations[i]), 1, 0)
                  for i in range(N)]
        opt.add(Sum(active) <= 3)

# ---- Machine capacity: at most 2 simultaneous tasks per machine ----
tasks_on_machine = [[] for _ in range(M_cnt)]
for i in range(N):
    tasks_on_machine[req_machines[i]].append(i)

for m_idx in range(M_cnt):
    for t in range(T_max + 1):
        active = [If(And(start[i] <= t,
                         t < start[i] + durations[i]), 1, 0)
                  for i in tasks_on_machine[m_idx]]
        if active:
            opt.add(Sum(active) <= 2)

# ---- Budget constraint (total cost <= 470) ----
# Cost per task = (worker_hourly_cost + machine_hourly_cost) * duration
# Machine cost is deterministic; worker cost depends on assignment.
total_cost = Sum([
    (Sum([If(worker[i] == w, worker_costs[w], 0) for w in range(W)])
     + machine_costs[req_machines[i]]) * durations[i]
    for i in range(N)
])
opt.add(total_cost <= 470)

# ---- Objective: minimize makespan ----
makespan = Int('makespan')
opt.add(makespan >= 0)
for i in range(N):
    opt.add(makespan >= start[i] + durations[i])
opt.minimize(makespan)

# ============================================================
# SOLVE & OUTPUT
# ============================================================
result = opt.check()

if result == sat:
    m = opt.model()
    ms_val  = m.evaluate(makespan,  model_completion=True)
    tc_val  = m.evaluate(total_cost, model_completion=True)

    print("STATUS: sat")
    print(f"makespan = {ms_val}")
    print(f"total_cost = {tc_val}")
    print(f"feasible = True")
    print()
    print("Schedule:")
    for i in range(N):
        s_val = m.evaluate(start[i], model_completion=True)
        w_val = m.evaluate(worker[i], model_completion=True)
        w_int = w_val.as_long()
        mach_int = req_machines[i]
        finish = int(str(s_val)) + durations[i]
        print(f"  {tasks[i]}: start={s_val}, finish={finish}, worker=W{w_int+1}, machine=M{mach_int+1}, "
              f"cost={(worker_costs[w_int] + machine_costs[mach_int]) * durations[i]}")

    # Verify all constraints explicitly
    print()
    print("=== Verification ===")
    # Check deadlines
    all_deadlines_ok = True
    for i in range(N):
        s_val = int(str(m.evaluate(start[i], model_completion=True)))
        if s_val + durations[i] > deadlines[i]:
            print(f"  VIOLATION: {tasks[i]} finishes at {s_val+durations[i]} > deadline {deadlines[i]}")
            all_deadlines_ok = False
    if all_deadlines_ok:
        print("  All deadlines satisfied.")

    # Check precedences
    all_prec_ok = True
    for (b, a) in precedences:
        sb = int(str(m.evaluate(start[b], model_completion=True)))
        sa = int(str(m.evaluate(start[a], model_completion=True)))
        if sa < sb + durations[b]:
            print(f"  VIOLATION: {tasks[a]} starts at {sa} < {tasks[b]} finishes at {sb+durations[b]}")
            all_prec_ok = False
    if all_prec_ok:
        print("  All precedence constraints satisfied.")

    # Check budget
    computed_cost = 0
    for i in range(N):
        w_val = int(str(m.evaluate(worker[i], model_completion=True)))
        mc = req_machines[i]
        computed_cost += (worker_costs[w_val] + machine_costs[mc]) * durations[i]
    print(f"  Computed total cost: {computed_cost} (limit 470)")
    if computed_cost <= 470:
        print("  Budget constraint satisfied.")
    else:
        print("  VIOLATION: Budget exceeded!")

    # Check worker capacity
    print("  Worker capacity check (max 3 simultaneous):")
    for w in range(W):
        max_sim = 0
        for t in range(T_max + 1):
            count = 0
            for i in range(N):
                wi = int(str(m.evaluate(worker[i], model_completion=True)))
                si = int(str(m.evaluate(start[i], model_completion=True)))
                if wi == w and si <= t < si + durations[i]:
                    count += 1
            if count > max_sim:
                max_sim = count
        status = "OK" if max_sim <= 3 else "VIOLATION"
        print(f"    W{w+1}: max simultaneous = {max_sim} [{status}]")

    # Check machine capacity
    print("  Machine capacity check (max 2 simultaneous):")
    for m_idx in range(M_cnt):
        max_sim = 0
        for t in range(T_max + 1):
            count = 0
            for i in tasks_on_machine[m_idx]:
                si = int(str(m.evaluate(start[i], model_completion=True)))
                if si <= t < si + durations[i]:
                    count += 1
            if count > max_sim:
                max_sim = count
        status = "OK" if max_sim <= 2 else "VIOLATION"
        print(f"    M{m_idx+1}: max simultaneous = {max_sim} [{status}]")

elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found.")
else:
    print("STATUS: unknown")
    print("Solver returned unknown (timeout or incomplete).")