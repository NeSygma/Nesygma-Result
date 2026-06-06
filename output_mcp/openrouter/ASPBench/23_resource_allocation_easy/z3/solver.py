from z3 import *

# Define data
values = [50, 40, 60, 35, 70, 45]
res_a = [30, 25, 20, 15, 40, 20]
res_b = [20, 15, 30, 25, 10, 20]
res_c = [10, 15, 20, 10, 25, 15]

# Decision variables: Bool for each task
select = [Bool(f'select_{i}') for i in range(6)]

opt = Optimize()

# Resource capacity constraints
opt.add(Sum([If(select[i], res_a[i], 0) for i in range(6)]) <= 100)
opt.add(Sum([If(select[i], res_b[i], 0) for i in range(6)]) <= 80)
opt.add(Sum([If(select[i], res_c[i], 0) for i in range(6)]) <= 60)

# Objective: maximize total value
total_val = Sum([If(select[i], values[i], 0) for i in range(6)])
opt.maximize(total_val)

result = opt.check()
if result == sat:
    m = opt.model()
    selected = [i for i in range(6) if is_true(m.eval(select[i]))]
    total_value = sum(values[i] for i in selected)
    used_a = sum(res_a[i] for i in selected)
    used_b = sum(res_b[i] for i in selected)
    used_c = sum(res_c[i] for i in selected)
    print("STATUS: sat")
    print(f"selected_tasks = {selected}")
    print(f"total_value = {total_value}")
    print(f"resource_a = {used_a}")
    print(f"resource_b = {used_b}")
    print(f"resource_c = {used_c}")
else:
    print("STATUS: unsat")