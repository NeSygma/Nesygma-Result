from z3 import *

# ============================================================
# Problem: Schedule 4 recipes with shared resources, minimize makespan
# ============================================================

# ---------- Tasks and Durations ----------
tasks_info = [
    ("prep_chicken",   "roast_chicken", "prep_chicken",   15, "prep_area"),
    ("bake_chicken",   "roast_chicken", "bake_chicken",   50, "oven"),
    ("rest_chicken",   "roast_chicken", "rest_chicken",   10, "prep_area"),
    ("chop_veg_soup",  "vegetable_soup","chop_veg_soup",  20, "prep_area"),
    ("simmer_stock",   "vegetable_soup","simmer_stock",   30, "stove"),
    ("chop_onion",     "risotto",       "chop_onion",      5, "prep_area"),
    ("cook_risotto",   "risotto",       "cook_risotto",   25, "stove"),
    ("wash_greens",    "side_salad",    "wash_greens",     5, "prep_area"),
    ("mix_dressing",   "side_salad",    "mix_dressing",   10, "prep_area"),
    ("preheat_oven",   None,            None,             10, "oven"),
]

task_ids = [t[0] for t in tasks_info]
durations = {t[0]: t[3] for t in tasks_info}
resources = {t[0]: t[4] for t in tasks_info}
N = len(task_ids)

# ---------- Decision Variables ----------
start_times = {tid: Int(f"start_{tid}") for tid in task_ids}
end_times = {tid: Int(f"end_{tid}") for tid in task_ids}
makespan = Int("makespan")

# ---------- Use Optimize directly ----------
opt = Optimize()

# ---------- Domain bounds ----------
for tid in task_ids:
    d = durations[tid]
    opt.add(start_times[tid] >= 0)
    opt.add(end_times[tid] == start_times[tid] + d)
    opt.add(end_times[tid] <= makespan)

# ---------- Step Precedences (within each recipe) ----------
opt.add(end_times["prep_chicken"] <= start_times["bake_chicken"])
opt.add(end_times["bake_chicken"] <= start_times["rest_chicken"])
opt.add(end_times["chop_veg_soup"] <= start_times["simmer_stock"])
opt.add(end_times["chop_onion"] <= start_times["cook_risotto"])
opt.add(end_times["wash_greens"] <= start_times["mix_dressing"])

# ---------- Inter-recipe Dependency ----------
opt.add(end_times["simmer_stock"] <= start_times["cook_risotto"])

# ---------- Oven Preheating ----------
opt.add(end_times["preheat_oven"] <= start_times["bake_chicken"])

# ---------- Resource Capacity Constraints ----------
# Use pairwise non-overlap constraints for capacity-1 resources (oven, stove)
# For capacity-2 resource (prep_area), we need at most 2 overlapping.

# Helper: for two tasks a,b on same resource, they can overlap if capacity > 1
# For capacity 1: they must NOT overlap
# For capacity 2: we need a more complex constraint

# Let's use a simpler approach: for each resource, use cumulative constraints
# via pairwise constraints with a "no more than capacity overlap" pattern.

# For oven (capacity 1): pairwise non-overlap
oven_tasks = [tid for tid in task_ids if resources[tid] == "oven"]
for i in range(len(oven_tasks)):
    for j in range(i+1, len(oven_tasks)):
        a = oven_tasks[i]
        b = oven_tasks[j]
        opt.add(Or(end_times[a] <= start_times[b], end_times[b] <= start_times[a]))

# For stove (capacity 1): pairwise non-overlap
stove_tasks = [tid for tid in task_ids if resources[tid] == "stove"]
for i in range(len(stove_tasks)):
    for j in range(i+1, len(stove_tasks)):
        a = stove_tasks[i]
        b = stove_tasks[j]
        opt.add(Or(end_times[a] <= start_times[b], end_times[b] <= start_times[a]))

# For prep_area (capacity 2): at most 2 can overlap at any time
# Use a time-indexed approach but with a smaller horizon
prep_tasks = [tid for tid in task_ids if resources[tid] == "prep_area"]
# We'll use a bounded horizon of 200
H = 200
opt.add(makespan <= H)

# For each time point, count active prep_area tasks
for t in range(H):
    active = Sum([If(And(start_times[tid] <= t, t < end_times[tid]), 1, 0) for tid in prep_tasks])
    opt.add(active <= 2)

# ---------- Minimize makespan ----------
opt.minimize(makespan)

result = opt.check()

if result == sat:
    m = opt.model()
    total_time = m.eval(makespan)
    print("STATUS: sat")
    print(f"total_time={total_time}")
    print("schedule:")
    for tid in task_ids:
        s = m.eval(start_times[tid])
        e = m.eval(end_times[tid])
        r = resources[tid]
        info = [t for t in tasks_info if t[0] == tid][0]
        if info[1] is not None:
            print(f"  recipe={info[1]}, step={info[2]}, start_time={s}, end_time={e}, resource={r}")
        else:
            print(f"  task={info[0]}, start_time={s}, end_time={e}, resource={r}")
    print("feasible=True")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (no feasible schedule found)")
else:
    print("STATUS: unknown")