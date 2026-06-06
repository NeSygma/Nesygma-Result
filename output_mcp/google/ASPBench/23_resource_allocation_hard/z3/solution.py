from z3 import *

# Task data
tasks = [
    {"id": 0, "cat": "Research", "val": 40, "comp": 20, "band": 10, "stor": 30, "spec": 5},
    {"id": 1, "cat": "Research", "val": 60, "comp": 30, "band": 25, "stor": 20, "spec": 10},
    {"id": 2, "cat": "Research", "val": 70, "comp": 25, "band": 20, "stor": 15, "spec": 5},
    {"id": 3, "cat": "Research", "val": 55, "comp": 20, "band": 15, "stor": 25, "spec": 10},
    {"id": 4, "cat": "Development", "val": 80, "comp": 40, "band": 30, "stor": 20, "spec": 20},
    {"id": 5, "cat": "Development", "val": 90, "comp": 35, "band": 25, "stor": 30, "spec": 15},
    {"id": 6, "cat": "Development", "val": 75, "comp": 30, "band": 40, "stor": 25, "spec": 18},
    {"id": 7, "cat": "Development", "val": 85, "comp": 45, "band": 35, "stor": 15, "spec": 22},
    {"id": 8, "cat": "Deployment", "val": 65, "comp": 15, "band": 20, "stor": 40, "spec": 8},
    {"id": 9, "cat": "Deployment", "val": 80, "comp": 20, "band": 30, "stor": 35, "spec": 12},
    {"id": 10, "cat": "Deployment", "val": 70, "comp": 25, "band": 25, "stor": 30, "spec": 10},
    {"id": 11, "cat": "Deployment", "val": 95, "comp": 30, "band": 35, "stor": 45, "spec": 15},
]

opt = Optimize()

# Decision variables
x = [Bool(f"x_{i}") for i in range(12)]

# Helper variables
res_selected = Or([x[i] for i in range(0, 4)])
dev_selected = Or([x[i] for i in range(4, 8)])
dep_selected = Or([x[i] for i in range(8, 12)])
bonus_achieved = And(res_selected, dev_selected, dep_selected)

# Resource usage
compute_usage = Sum([If(x[i], tasks[i]["comp"], 0) for i in range(12)])
bandwidth_usage = Sum([If(x[i], tasks[i]["band"], 0) for i in range(12)])
storage_usage = Sum([If(x[i], tasks[i]["stor"], 0) for i in range(12)])
# Specialist usage: base + conditional
base_spec_usage = Sum([If(x[i], tasks[i]["spec"], 0) for i in range(12)])
conditional_spec_usage = If(dev_selected, Sum([If(x[i], 5, 0) for i in range(8, 12)]), 0)
specialist_usage = base_spec_usage + conditional_spec_usage

# Constraints
opt.add(compute_usage <= 150)
opt.add(bandwidth_usage <= 120)
opt.add(storage_usage <= 140)
opt.add(specialist_usage <= 60)

# Prerequisite: Task 4 requires Task 0
opt.add(Implies(x[4], x[0]))

# Mutual Exclusion: Task 1 and Task 7 cannot both be selected
opt.add(Not(And(x[1], x[7])))

# Objective
total_value = Sum([If(x[i], tasks[i]["val"], 0) for i in range(12)]) + If(bonus_achieved, 100, 0)
opt.maximize(total_value)

if opt.check() == sat:
    m = opt.model()
    selected = [i for i in range(12) if is_true(m.evaluate(x[i]))]
    print("STATUS: sat")
    print(f"selected_tasks: {selected}")
    print(f"total_value: {m.evaluate(total_value)}")
    print(f"bonus_achieved: {is_true(m.evaluate(bonus_achieved))}")
    print(f"resource_usage: {{'compute': {m.evaluate(compute_usage)}, 'bandwidth': {m.evaluate(bandwidth_usage)}, 'storage': {m.evaluate(storage_usage)}, 'specialists': {m.evaluate(specialist_usage)}}}")
else:
    print("STATUS: unsat")