from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver for optimization
opt = Optimize()

# --- Decision Variables ---
# selected[i] = 1 if task i is selected, else 0
selected = [Int(f"selected_{i}") for i in range(12)]

# --- Resource Usage Variables ---
# Compute, Bandwidth, Storage, Specialists
resource_usage = {
    "compute": Int("compute"),
    "bandwidth": Int("bandwidth"),
    "storage": Int("storage"),
    "specialists": Int("specialists"),
}

# --- Total Value and Bonus ---
total_value = Int("total_value")
bonus_achieved = Bool("bonus_achieved")

# --- Task Data ---
task_data = [
    # ID, Category, Value, Compute, Bandwidth, Storage, Specialists
    (0, "Research", 40, 20, 10, 30, 5),
    (1, "Research", 60, 30, 25, 20, 10),
    (2, "Research", 70, 25, 20, 15, 5),
    (3, "Research", 55, 20, 15, 25, 10),
    (4, "Development", 80, 40, 30, 20, 20),
    (5, "Development", 90, 35, 25, 30, 15),
    (6, "Development", 75, 30, 40, 25, 18),
    (7, "Development", 85, 45, 35, 15, 22),
    (8, "Deployment", 65, 15, 20, 40, 8),
    (9, "Deployment", 80, 20, 30, 35, 12),
    (10, "Deployment", 70, 25, 25, 30, 10),
    (11, "Deployment", 95, 30, 35, 45, 15),
]

# --- Resource Capacities ---
resource_capacities = {
    "compute": 150,
    "bandwidth": 120,
    "storage": 140,
    "specialists": 60,
}

# --- Helper: Category Mapping ---
category_map = {i: cat for i, cat, *_ in task_data}

# --- Constraints ---

# 1. Task Selection: Each task can be selected at most once (0-1)
for i in range(12):
    opt.add(selected[i] >= 0, selected[i] <= 1)

# 2. Resource Usage: Sum over selected tasks
opt.add(resource_usage["compute"] == Sum([
    If(selected[i] == 1, task_data[i][3], 0) for i in range(12)
]))
opt.add(resource_usage["bandwidth"] == Sum([
    If(selected[i] == 1, task_data[i][4], 0) for i in range(12)
]))
opt.add(resource_usage["storage"] == Sum([
    If(selected[i] == 1, task_data[i][5], 0) for i in range(12)
]))

# Special handling for specialists due to conditional cost
opt.add(resource_usage["specialists"] == Sum([
    If(selected[i] == 1, task_data[i][6], 0) for i in range(12)
]) + 
    If(Or(selected[4] == 1, selected[5] == 1, selected[6] == 1, selected[7] == 1), 
       Sum([If(selected[i] == 1, 5, 0) for i in range(8, 12)]), 
       0
    )
)

# 3. Resource Limits
opt.add(resource_usage["compute"] <= resource_capacities["compute"])
opt.add(resource_usage["bandwidth"] <= resource_capacities["bandwidth"])
opt.add(resource_usage["storage"] <= resource_capacities["storage"])
opt.add(resource_usage["specialists"] <= resource_capacities["specialists"])

# 4. Prerequisite: Task 4 requires Task 0
opt.add(Implies(selected[4] == 1, selected[0] == 1))

# 5. Mutual Exclusion: Task 1 and Task 7 cannot both be selected
opt.add(Not(And(selected[1] == 1, selected[7] == 1)))

# 6. Diversity Bonus: At least one task from each category
# Research: 0-3, Development: 4-7, Deployment: 8-11
research_selected = Or([selected[i] == 1 for i in range(4)])
development_selected = Or([selected[i] == 1 for i in range(4, 8)])
deployment_selected = Or([selected[i] == 1 for i in range(8, 12)])
opt.add(bonus_achieved == And(research_selected, development_selected, deployment_selected))

# 7. Total Value: Sum of selected task values + bonus if achieved
base_value = Sum([
    If(selected[i] == 1, task_data[i][2], 0) for i in range(12)
])
opt.add(total_value == base_value + If(bonus_achieved, 100, 0))

# --- Objective: Maximize total_value ---
opt.maximize(total_value)

# --- Check and Output ---
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Total value:", model[total_value])
    print("Bonus achieved:", model[bonus_achieved])
    print("Resource usage:")
    print("  Compute:", model[resource_usage["compute"]])
    print("  Bandwidth:", model[resource_usage["bandwidth"]])
    print("  Storage:", model[resource_usage["storage"]])
    print("  Specialists:", model[resource_usage["specialists"]])
    print("Selected tasks:", sorted([i for i in range(12) if model[selected[i]] == 1]))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")