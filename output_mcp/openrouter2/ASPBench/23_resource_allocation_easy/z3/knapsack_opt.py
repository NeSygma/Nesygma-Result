from z3 import *

# Problem data
values = [50, 40, 60, 35, 70, 45]
resA = [30, 25, 20, 15, 40, 20]
resB = [20, 15, 30, 25, 10, 20]
resC = [10, 15, 20, 10, 25, 15]
capA = 100
capB = 80
capC = 60

opt = Optimize()
# Decision variables: 0-1 selection
selected = [Int(f'sel_{i}') for i in range(6)]
for i in range(6):
    opt.add(selected[i] >= 0, selected[i] <= 1)

# Resource constraints
opt.add(Sum([selected[i] * resA[i] for i in range(6)]) <= capA)
opt.add(Sum([selected[i] * resB[i] for i in range(6)]) <= capB)
opt.add(Sum([selected[i] * resC[i] for i in range(6)]) <= capC)

# Total value
total_value = Int('total_value')
opt.add(total_value == Sum([selected[i] * values[i] for i in range(6)]))

# Objective
opt.maximize(total_value)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract selected tasks
    selected_tasks = [i for i in range(6) if m.evaluate(selected[i]).as_long() == 1]
    # Compute resource usage
    usageA = sum(m.evaluate(selected[i] * resA[i]).as_long() for i in range(6))
    usageB = sum(m.evaluate(selected[i] * resB[i]).as_long() for i in range(6))
    usageC = sum(m.evaluate(selected[i] * resC[i]).as_long() for i in range(6))
    print("STATUS: sat")
    print("selected_tasks =", selected_tasks)
    print("total_value =", m.evaluate(total_value).as_long())
    print("resource_usage = {'resource_a':", usageA, ", 'resource_b':", usageB, ", 'resource_c':", usageC, "}")
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")