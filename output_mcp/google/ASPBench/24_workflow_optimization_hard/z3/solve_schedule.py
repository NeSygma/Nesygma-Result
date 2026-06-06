from z3 import *

# Task data
durations = {0: 4, 1: 3, 2: 5, 3: 2, 4: 6, 5: 3, 6: 4, 7: 5, 8: 2, 9: 3}
eligible_machines = {
    0: [1], 1: [2], 2: [3], 3: [1], 4: [2],
    5: [1], 6: [3], 7: [2], 8: [1], 9: [2, 3]
}
prerequisites = {
    0: [], 1: [], 2: [], 3: [0], 4: [1],
    5: [3], 6: [2, 4], 7: [4], 8: [5], 9: [7, 8]
}
tasks = list(range(10))
machines = [1, 2, 3]

# Optimization
opt = Optimize()

# Variables
start_times = {t: Int(f'start_{t}') for t in tasks}
end_times = {t: Int(f'end_{t}') for t in tasks}
machine_assignments = {t: Int(f'machine_{t}') for t in tasks}
makespan = Int('makespan')

# Constraints
for t in tasks:
    # Duration
    opt.add(end_times[t] == start_times[t] + durations[t])
    opt.add(start_times[t] >= 0)
    
    # Machine eligibility
    opt.add(Or([machine_assignments[t] == m for m in eligible_machines[t]]))
    
    # Prerequisites
    for pre in prerequisites[t]:
        opt.add(start_times[t] >= end_times[pre])

# Machine non-overlap
for m in machines:
    for t1 in tasks:
        for t2 in tasks:
            if t1 < t2:
                # If both assigned to same machine, they cannot overlap
                opt.add(Implies(
                    And(machine_assignments[t1] == m, machine_assignments[t2] == m),
                    Or(end_times[t1] <= start_times[t2], end_times[t2] <= start_times[t1])
                ))

# Makespan
for t in tasks:
    opt.add(makespan >= end_times[t])
opt.minimize(makespan)

# Solve
if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"makespan = {m[makespan]}")
    for t in tasks:
        print(f"Task {t}: machine={m[machine_assignments[t]]}, start={m[start_times[t]]}, end={m[end_times[t]]}")
else:
    print("STATUS: unsat")