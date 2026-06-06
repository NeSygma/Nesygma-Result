from z3 import *

opt = Optimize()

# binary variables for each task
x = [Bool(f'x{i}') for i in range(6)]

# resource consumption per task
A_usage = [30, 25, 20, 15, 40, 20]
B_usage = [20, 15, 30, 25, 10, 20]
C_usage = [10, 15, 20, 10, 25, 15]
values = [50, 40, 60, 35, 70, 45]

# capacity constraints
opt.add(Sum([A_usage[i] * x[i] for i in range(6)]) <= 100)
opt.add(Sum([B_usage[i] * x[i] for i in range(6)]) <= 80)
opt.add(Sum([C_usage[i] * x[i] for i in range(6)]) <= 60)

# objective: maximize total value
opt.maximize(Sum([values[i] * x[i] for i in range(6)]))

# solve
result = opt.check()
if result == sat:
    m = opt.model()
    selected_tasks = [i for i in range(6) if m[x[i]] == True]
    total_value = sum(values[i] for i in range(6) if m[x[i]] == True)
    resource_a = sum(A_usage[i] for i in range(6) if m[x[i]] == True)
    resource_b = sum(B_usage[i] for i in range(6) if m[x[i]] == True)
    resource_c = sum(C_usage[i] for i in range(6) if m[x[i]] == True)
    print("STATUS: sat")
    print("selected_tasks =", selected_tasks)
    print("total_value =", total_value)
    print("resource_usage = {")
    print("  resource_a =", resource_a)
    print("  resource_b =", resource_b)
    print("  resource_c =", resource_c)
    print("}")
else:
    print("STATUS: unsat")