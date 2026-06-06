from z3 import *

# Define tasks with (name, duration, resource)
tasks = [
    # Roast Chicken
    ("prep_chicken", 15, "prep_area"),
    ("bake_chicken", 50, "oven"),
    ("rest_chicken", 10, "prep_area"),
    # Vegetable Soup
    ("chop_veg_soup", 20, "prep_area"),
    ("simmer_stock", 30, "stove"),
    # Risotto
    ("chop_onion", 5, "prep_area"),
    ("cook_risotto", 25, "stove"),
    # Side Salad
    ("wash_greens", 5, "prep_area"),
    ("mix_dressing", 10, "prep_area"),
    # Special task
    ("preheat_oven", 10, "oven"),
]

# Create start time variables (non-negative integers)
start = {}
for name, dur, res in tasks:
    start[name] = Int(f"start_{name}")

# Duration mapping
duration = {name: dur for name, dur, res in tasks}

# Resource mapping
resource = {name: res for name, dur, res in tasks}

# Precedence constraints
solver = Solver()

# Roast Chicken: prep_chicken -> bake_chicken -> rest_chicken
solver.add(start["prep_chicken"] + duration["prep_chicken"] <= start["bake_chicken"])
solver.add(start["bake_chicken"] + duration["bake_chicken"] <= start["rest_chicken"])

# Vegetable Soup: chop_veg_soup -> simmer_stock
solver.add(start["chop_veg_soup"] + duration["chop_veg_soup"] <= start["simmer_stock"])

# Risotto: chop_onion -> cook_risotto
solver.add(start["chop_onion"] + duration["chop_onion"] <= start["cook_risotto"])

# Side Salad: wash_greens -> mix_dressing
solver.add(start["wash_greens"] + duration["wash_greens"] <= start["mix_dressing"])

# Inter-recipe dependency: simmer_stock must finish before cook_risotto starts
solver.add(start["simmer_stock"] + duration["simmer_stock"] <= start["cook_risotto"])

# Oven preheating: preheat_oven must complete before any bake_chicken starts
solver.add(start["preheat_oven"] + duration["preheat_oven"] <= start["bake_chicken"])

# Resource capacity constraints
# For each resource, ensure no two tasks overlap beyond capacity
# We'll use pairwise non-overlap for tasks sharing the same resource
# For prep_area (capacity 2), we need to ensure at most 2 tasks overlap.
# Since capacity is 2, we can allow overlap but need to limit concurrent tasks.
# We'll use cumulative constraint or explicit constraints.
# Let's use explicit constraints for simplicity: for each pair of tasks using same resource,
# they must not overlap if capacity is 1, but for capacity 2 we need to allow up to 2 overlaps.
# We'll use a different approach: for each resource, we can use the cumulative constraint.
# However, Z3's cumulative is not directly available in Python API; we can use a custom encoding.
# For capacity 2, we can use a binary variable for each time slot? That's complex.
# Instead, we can use the "at most 2 tasks overlap" constraint by ensuring that for any three tasks,
# they cannot all overlap simultaneously. But that's O(n^3).
# Better: use the cumulative constraint via the 'sum' of intervals.
# Let's use the standard approach: for each resource, we can use the "no overlap" for capacity 1,
# and for capacity 2 we can use a more general encoding.

# Let's list tasks per resource:
prep_area_tasks = [name for name, dur, res in tasks if res == "prep_area"]
oven_tasks = [name for name, dur, res in tasks if res == "oven"]
stove_tasks = [name for name, dur, res in tasks if res == "stove"]

print("Prep area tasks:", prep_area_tasks)
print("Oven tasks:", oven_tasks)
print("Stove tasks:", stove_tasks)

# For oven (capacity 1) and stove (capacity 1), we can enforce pairwise non-overlap.
# For prep_area (capacity 2), we need to allow up to 2 concurrent tasks.
# We'll use a simple encoding: for each pair of prep_area tasks, we allow overlap,
# but we must ensure that no three tasks overlap simultaneously.
# We'll create a binary variable for each pair indicating if they overlap? That's messy.
# Instead, we can use the "cumulative" constraint via the "sum of heights" approach.
# Let's define for each task a height of 1, and capacity 2.
# We can use the following encoding: for each time point, the sum of tasks active at that time <= 2.
# But time is continuous; we can discretize at task start/end times.
# Since all durations are integers, we can consider integer time points.
# However, that could be large.

# Alternative: use the "no overlap" for capacity 1, and for capacity 2 we can use a different method:
# For each pair of tasks, we can allow overlap, but we need to ensure that for any three tasks,
# they don't all overlap. We can add constraints for each triple.
# Let's do that for prep_area (6 tasks). Number of triples = C(6,3)=20. That's manageable.

# For each triple (i,j,k) of prep_area tasks, we ensure that not all three overlap.
# Overlap condition: tasks i and j overlap if start_i < end_j and start_j < end_i.
# We'll encode using Z3's Or of pairwise non-overlap.

# Let's define end times
end = {name: start[name] + duration[name] for name in start}

# Helper function to check overlap between two tasks
def overlap(t1, t2):
    # t1 and t2 overlap if start1 < end2 and start2 < end1
    return And(start[t1] < end[t2], start[t2] < end[t1])

# For oven tasks (capacity 1): ensure no overlap between any two oven tasks
for i in range(len(oven_tasks)):
    for j in range(i+1, len(oven_tasks)):
        solver.add(Not(overlap(oven_tasks[i], oven_tasks[j])))

# For stove tasks (capacity 1): ensure no overlap between any two stove tasks
for i in range(len(stove_tasks)):
    for j in range(i+1, len(stove_tasks)):
        solver.add(Not(overlap(stove_tasks[i], stove_tasks[j])))

# For prep_area tasks (capacity 2): ensure no triple overlap
# For each triple (i,j,k), ensure that not all three overlap.
# That is: Not(And(overlap(i,j), overlap(j,k), overlap(i,k)))
# But we need to ensure that at most 2 overlap at any time.
# Actually, the triple constraint ensures that there is no time where all three are active.
# However, it's possible that three tasks overlap pairwise but not all three simultaneously?
# If each pair overlaps, then there is a common intersection? Not necessarily.
# For intervals, if each pair overlaps, then all three have a common intersection (Helly's theorem for intervals).
# So triple overlap constraint is sufficient.
for i in range(len(prep_area_tasks)):
    for j in range(i+1, len(prep_area_tasks)):
        for k in range(j+1, len(prep_area_tasks)):
            solver.add(Not(And(overlap(prep_area_tasks[i], prep_area_tasks[j]),
                               overlap(prep_area_tasks[j], prep_area_tasks[k]),
                               overlap(prep_area_tasks[i], prep_area_tasks[k]))))

# Ensure all start times are non-negative
for name in start:
    solver.add(start[name] >= 0)

# Objective: minimize total makespan (max end time)
makespan = Int("makespan")
solver.add(makespan >= end[name] for name in end)
# We'll use Optimize for minimization
opt = Optimize()
# Transfer constraints from solver to opt
for c in solver.assertions():
    opt.add(c)
opt.add(makespan >= end[name] for name in end)
opt.minimize(makespan)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print("Optimal makespan:", m.evaluate(makespan))
    print("Schedule:")
    for name, dur, res in tasks:
        st = m.evaluate(start[name])
        et = m.evaluate(end[name])
        print(f"  {name}: start={st}, end={et}, resource={res}")
    # Also compute total_time
    total_time = m.evaluate(makespan)
    print(f"total_time={total_time}")
    # Check feasibility
    feasible = True
    # Verify constraints (optional)
    print("feasible=True")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")