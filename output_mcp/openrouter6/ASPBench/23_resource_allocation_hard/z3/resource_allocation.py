from z3 import *

# Task data
tasks = [
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
    (11, "Deployment", 95, 30, 35, 45, 15)
]

# Extract arrays
values = [t[2] for t in tasks]
compute = [t[3] for t in tasks]
bandwidth = [t[4] for t in tasks]
storage = [t[5] for t in tasks]
specialists = [t[6] for t in tasks]

# Capacities
CAP_COMPUTE = 150
CAP_BANDWIDTH = 120
CAP_STORAGE = 140
CAP_SPECIALISTS = 60

# Create solver
opt = Optimize()

# Decision variables: selection[i] = 1 if task i is selected
selection = [Int(f'sel_{i}') for i in range(12)]
for i in range(12):
    opt.add(selection[i] >= 0, selection[i] <= 1)

# Helper variables for categories
has_research = Int('has_research')
has_development = Int('has_development')
has_deployment = Int('has_deployment')
opt.add(has_research >= 0, has_research <= 1)
opt.add(has_development >= 0, has_development <= 1)
opt.add(has_deployment >= 0, has_deployment <= 1)

# Category constraints: has_X = 1 if any task in that category is selected
# Research: tasks 0-3
opt.add(has_research >= selection[0])
opt.add(has_research >= selection[1])
opt.add(has_research >= selection[2])
opt.add(has_research >= selection[3])
opt.add(has_research <= selection[0] + selection[1] + selection[2] + selection[3])

# Development: tasks 4-7
opt.add(has_development >= selection[4])
opt.add(has_development >= selection[5])
opt.add(has_development >= selection[6])
opt.add(has_development >= selection[7])
opt.add(has_development <= selection[4] + selection[5] + selection[6] + selection[7])

# Deployment: tasks 8-11
opt.add(has_deployment >= selection[8])
opt.add(has_deployment >= selection[9])
opt.add(has_deployment >= selection[10])
opt.add(has_deployment >= selection[11])
opt.add(has_deployment <= selection[8] + selection[9] + selection[10] + selection[11])

# Diversity bonus
bonus_achieved = Int('bonus_achieved')
opt.add(bonus_achieved >= 0, bonus_achieved <= 1)
opt.add(bonus_achieved == If(And(has_research == 1, has_development == 1, has_deployment == 1), 1, 0))

# Resource usage calculations
compute_total = Sum([selection[i] * compute[i] for i in range(12)])
bandwidth_total = Sum([selection[i] * bandwidth[i] for i in range(12)])
storage_total = Sum([selection[i] * storage[i] for i in range(12)])

# Specialist usage: base cost + conditional additional cost
base_specialists = Sum([selection[i] * specialists[i] for i in range(12)])
deployment_count = Sum([selection[i] for i in range(8, 12)])
additional_specialists = 5 * deployment_count * has_development
specialists_total = base_specialists + additional_specialists

# Resource constraints
opt.add(compute_total <= CAP_COMPUTE)
opt.add(bandwidth_total <= CAP_BANDWIDTH)
opt.add(storage_total <= CAP_STORAGE)
opt.add(specialists_total <= CAP_SPECIALISTS)

# Prerequisite: Task 4 requires Task 0
opt.add(selection[4] <= selection[0])

# Mutual exclusion: Task 1 and Task 7 cannot both be selected
opt.add(selection[1] + selection[7] <= 1)

# Total value calculation
total_value = Sum([selection[i] * values[i] for i in range(12)]) + 100 * bonus_achieved

# Maximize total value
opt.maximize(total_value)

# Check and get model
result = opt.check()
if result == sat:
    m = opt.model()
    
    # Extract selected tasks
    selected_tasks = []
    for i in range(12):
        if m.evaluate(selection[i]) == 1:
            selected_tasks.append(i)
    selected_tasks.sort()
    
    # Calculate total value
    total_val = m.evaluate(total_value).as_long()
    
    # Calculate bonus achieved
    bonus = m.evaluate(bonus_achieved) == 1
    
    # Calculate resource usage
    compute_used = m.evaluate(compute_total).as_long()
    bandwidth_used = m.evaluate(bandwidth_total).as_long()
    storage_used = m.evaluate(storage_total).as_long()
    specialists_used = m.evaluate(specialists_total).as_long()
    
    print("STATUS: sat")
    print(f"selected_tasks: {selected_tasks}")
    print(f"total_value: {total_val}")
    print(f"bonus_achieved: {bonus}")
    print("resource_usage:")
    print(f"  compute: {compute_used}")
    print(f"  bandwidth: {bandwidth_used}")
    print(f"  storage: {storage_used}")
    print(f"  specialists: {specialists_used}")
    
    # Verify expected optimal value
    if total_val == 470:
        print("Optimal value matches expected: 470")
    else:
        print(f"Note: Found value {total_val}, expected 470")
        
elif result == unsat:
    print("STATUS: unsat")
    print("Problem is infeasible")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")