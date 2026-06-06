from z3 import *

# ============================================================
# DATA
# ============================================================

tasks = {
    'T1':  {'dur': 2, 'skill': 'Welding',     'machine_type': 'A', 'deadline': 6},
    'T2':  {'dur': 3, 'skill': 'Assembly',    'machine_type': 'B', 'deadline': 8},
    'T3':  {'dur': 1, 'skill': 'Inspection',  'machine_type': 'A', 'deadline': 7},
    'T4':  {'dur': 2, 'skill': 'Welding',     'machine_type': 'A', 'deadline': 9},
    'T5':  {'dur': 3, 'skill': 'Assembly',    'machine_type': 'C', 'deadline': 10},
    'T6':  {'dur': 2, 'skill': 'Programming', 'machine_type': 'B', 'deadline': 9},
    'T7':  {'dur': 1, 'skill': 'Inspection',  'machine_type': 'A', 'deadline': 8},
    'T8':  {'dur': 2, 'skill': 'Assembly',    'machine_type': 'C', 'deadline': 11},
    'T9':  {'dur': 3, 'skill': 'Welding',     'machine_type': 'A', 'deadline': 12},
    'T10': {'dur': 2, 'skill': 'Programming', 'machine_type': 'B', 'deadline': 11},
    'T11': {'dur': 1, 'skill': 'Assembly',    'machine_type': 'C', 'deadline': 10},
    'T12': {'dur': 2, 'skill': 'Inspection',  'machine_type': 'A', 'deadline': 13},
}

workers = {
    'W1': {'skills': ['Welding', 'Inspection'],              'cost': 15},
    'W2': {'skills': ['Assembly', 'Inspection'],             'cost': 12},
    'W3': {'skills': ['Programming', 'Assembly'],            'cost': 20},
    'W4': {'skills': ['Welding', 'Programming'],             'cost': 18},
    'W5': {'skills': ['Assembly', 'Inspection', 'Welding'],  'cost': 16},
}

machines = {
    'M1': {'type': 'A', 'cost': 3},
    'M2': {'type': 'B', 'cost': 2},
    'M3': {'type': 'C', 'cost': 4},
}

# Precedence: (predecessor, successor)
precedences = [
    ('T1', 'T3'), ('T1', 'T4'),
    ('T2', 'T5'), ('T2', 'T6'),
    ('T3', 'T7'),
    ('T4', 'T9'),
    ('T5', 'T8'),
    ('T6', 'T10'),
    ('T7', 'T12'),
    ('T8', 'T11'),
]

task_ids = list(tasks.keys())
worker_ids = list(workers.keys())
machine_ids = list(machines.keys())

# ============================================================
# SOLVER
# ============================================================

opt = Optimize()
opt.set("timeout", 120000)  # 2 minutes

# --- Decision Variables ---
# Start time for each task
start = {t: Int(f'start_{t}') for t in task_ids}

# Worker assignment for each task (index into worker_ids)
worker_assign = {t: Int(f'worker_{t}') for t in task_ids}

# Machine assignment for each task (index into machine_ids)
machine_assign = {t: Int(f'machine_{t}') for t in task_ids}

# Makespan variable
makespan = Int('makespan')

# --- Domain constraints ---
for t in task_ids:
    opt.add(start[t] >= 0)
    opt.add(worker_assign[t] >= 0, worker_assign[t] < len(worker_ids))
    opt.add(machine_assign[t] >= 0, machine_assign[t] < len(machine_ids))

# --- Skill compatibility ---
for t in task_ids:
    required_skill = tasks[t]['skill']
    compatible_workers = [i for i, w in enumerate(worker_ids) if required_skill in workers[w]['skills']]
    opt.add(Or([worker_assign[t] == i for i in compatible_workers]))

# --- Machine type compatibility ---
for t in task_ids:
    required_type = tasks[t]['machine_type']
    compatible_machines = [i for i, m in enumerate(machine_ids) if machines[m]['type'] == required_type]
    opt.add(Or([machine_assign[t] == i for i in compatible_machines]))

# --- Deadline constraints ---
for t in task_ids:
    opt.add(start[t] + tasks[t]['dur'] <= tasks[t]['deadline'])

# --- Precedence constraints ---
for (pred, succ) in precedences:
    opt.add(start[pred] + tasks[pred]['dur'] <= start[succ])

# --- Makespan definition ---
for t in task_ids:
    opt.add(makespan >= start[t] + tasks[t]['dur'])
opt.add(makespan >= 0)

# --- Capacity constraints (pairwise overlap detection) ---
# Two tasks overlap if: start[a] < start[b] + dur[b] AND start[b] < start[a] + dur[a]
# Worker capacity: at most 3 tasks can overlap for any worker
# Machine capacity: at most 2 tasks can overlap for any machine

# For worker capacity: for any set of 4 tasks assigned to the same worker,
# at least one pair must not overlap.
# We enumerate all 4-element subsets of tasks for each worker.
# But that's expensive. Instead, we use a pairwise approach:
# For each pair of tasks, if they share a worker and overlap, that's fine as long as
# no 3+ tasks overlap at any point. 

# A cleaner approach: for each worker, for each pair of tasks assigned to that worker,
# we need to ensure that at most 3 overlap at any time.
# We use the "no 4 tasks overlap" formulation:
# For any 4 tasks all assigned to the same worker, at least one pair doesn't overlap.

# Similarly for machines: for any 3 tasks all on the same machine, at least one pair doesn't overlap.

def overlaps(a, b):
    """Returns Z3 Bool: tasks a and b overlap in time."""
    return And(start[a] < start[b] + tasks[b]['dur'],
               start[b] < start[a] + tasks[a]['dur'])

# Worker capacity: no 4 tasks assigned to same worker can all pairwise overlap
from itertools import combinations
for w_idx in range(len(worker_ids)):
    # For every combination of 4 tasks
    for combo in combinations(task_ids, 4):
        a, b, c, d = combo
        # If all 4 are assigned to this worker, they can't all pairwise overlap
        all_same_worker = And(worker_assign[a] == w_idx,
                              worker_assign[b] == w_idx,
                              worker_assign[c] == w_idx,
                              worker_assign[d] == w_idx)
        # At least one pair must not overlap
        not_all_overlap = Or(Not(overlaps(a, b)), Not(overlaps(a, c)), Not(overlaps(a, d)),
                             Not(overlaps(b, c)), Not(overlaps(b, d)), Not(overlaps(c, d)))
        opt.add(Implies(all_same_worker, not_all_overlap))

# Machine capacity: no 3 tasks assigned to same machine can all pairwise overlap
for m_idx in range(len(machine_ids)):
    for combo in combinations(task_ids, 3):
        a, b, c = combo
        all_same_machine = And(machine_assign[a] == m_idx,
                               machine_assign[b] == m_idx,
                               machine_assign[c] == m_idx)
        not_all_overlap = Or(Not(overlaps(a, b)), Not(overlaps(a, c)), Not(overlaps(b, c)))
        opt.add(Implies(all_same_machine, not_all_overlap))

# --- Budget constraint ---
# Total cost = sum over tasks of (worker_cost + machine_cost) * duration
total_cost = Sum([
    (If(worker_assign[t] == 0, workers['W1']['cost'],
     If(worker_assign[t] == 1, workers['W2']['cost'],
     If(worker_assign[t] == 2, workers['W3']['cost'],
     If(worker_assign[t] == 3, workers['W4']['cost'],
        workers['W5']['cost'])))) +
    If(machine_assign[t] == 0, machines['M1']['cost'],
     If(machine_assign[t] == 1, machines['M2']['cost'],
        machines['M3']['cost']))) * tasks[t]['dur']
    for t in task_ids
])
opt.add(total_cost <= 470)

# --- Objective: minimize makespan ---
opt.minimize(makespan)

# ============================================================
# SOLVE
# ============================================================

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    schedule = []
    for t in task_ids:
        s = m.evaluate(start[t]).as_long()
        w_idx = m.evaluate(worker_assign[t]).as_long()
        m_idx = m.evaluate(machine_assign[t]).as_long()
        w_name = worker_ids[w_idx]
        m_name = machine_ids[m_idx]
        schedule.append((t, w_name, m_name, s))
    
    ms = m.evaluate(makespan).as_long()
    
    # Compute total cost
    tc = 0
    for t in task_ids:
        s = m.evaluate(start[t]).as_long()
        w_idx = m.evaluate(worker_assign[t]).as_long()
        m_idx = m.evaluate(machine_assign[t]).as_long()
        w_cost = workers[worker_ids[w_idx]]['cost']
        m_cost = machines[machine_ids[m_idx]]['cost']
        tc += (w_cost + m_cost) * tasks[t]['dur']
    
    print(f"makespan: {ms}")
    print(f"total_cost: {tc}")
    print(f"feasible: True")
    print()
    print("Schedule:")
    print(f"{'Task':<6} {'Worker':<8} {'Machine':<9} {'Start':<6} {'Finish':<7}")
    print("-" * 40)
    for t, w, mc, s in sorted(schedule, key=lambda x: x[3]):
        f = s + tasks[t]['dur']
        print(f"{t:<6} {w:<8} {mc:<9} {s:<6} {f:<7}")
    
    # Verify constraints
    print()
    print("=== Constraint Verification ===")
    
    # Check deadlines
    deadline_ok = True
    for t in task_ids:
        s = m.evaluate(start[t]).as_long()
        if s + tasks[t]['dur'] > tasks[t]['deadline']:
            print(f"  VIOLATION: {t} finishes at {s + tasks[t]['dur']} > deadline {tasks[t]['deadline']}")
            deadline_ok = False
    if deadline_ok:
        print("  Deadlines: OK")
    
    # Check precedences
    prec_ok = True
    for (pred, succ) in precedences:
        sp = m.evaluate(start[pred]).as_long()
        ss = m.evaluate(start[succ]).as_long()
        if sp + tasks[pred]['dur'] > ss:
            print(f"  VIOLATION: {pred} finishes at {sp + tasks[pred]['dur']} > {succ} starts at {ss}")
            prec_ok = False
    if prec_ok:
        print("  Precedences: OK")
    
    # Check budget
    print(f"  Budget: {tc} <= 470 {'OK' if tc <= 470 else 'VIOLATION'}")
    
    # Check worker capacity (at most 3 simultaneous)
    # Check machine capacity (at most 2 simultaneous)
    # We check at each integer time point
    max_worker_sim = 0
    max_machine_sim = 0
    for t_pt in range(ms + 1):
        for w_idx in range(len(worker_ids)):
            count = sum(1 for t in task_ids 
                       if m.evaluate(worker_assign[t]).as_long() == w_idx
                       and m.evaluate(start[t]).as_long() <= t_pt < m.evaluate(start[t]).as_long() + tasks[t]['dur'])
            if count > max_worker_sim:
                max_worker_sim = count
        for m_idx in range(len(machine_ids)):
            count = sum(1 for t in task_ids
                       if m.evaluate(machine_assign[t]).as_long() == m_idx
                       and m.evaluate(start[t]).as_long() <= t_pt < m.evaluate(start[t]).as_long() + tasks[t]['dur'])
            if count > max_machine_sim:
                max_machine_sim = count
    
    print(f"  Max worker simultaneous: {max_worker_sim} {'OK' if max_worker_sim <= 3 else 'VIOLATION'}")
    print(f"  Max machine simultaneous: {max_machine_sim} {'OK' if max_machine_sim <= 2 else 'VIOLATION'}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")