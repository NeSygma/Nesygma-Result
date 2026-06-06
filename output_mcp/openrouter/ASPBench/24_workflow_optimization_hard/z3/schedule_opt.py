from z3 import *

# Data
num_tasks = 10
tasks = list(range(num_tasks))
# durations
duration = [4,3,5,2,6,3,4,5,2,3]
# eligible machines per task (IDs)
eligible = {
    0: [1],
    1: [2],
    2: [3],
    3: [1],
    4: [2],
    5: [1],
    6: [3],
    7: [2],
    8: [1],
    9: [2,3]
}
# prerequisites per task
prereq = {
    0: [],
    1: [],
    2: [],
    3: [0],
    4: [1],
    5: [3],
    6: [2,4],
    7: [4],
    8: [5],
    9: [7,8]
}

opt = Optimize()
# decision variables
start = [Int(f'start_{i}') for i in tasks]
end = [Int(f'end_{i}') for i in tasks]
machine = [Int(f'machine_{i}') for i in tasks]

# constraints
for i in tasks:
    # start >= 0
    opt.add(start[i] >= 0)
    # end = start + duration
    opt.add(end[i] == start[i] + duration[i])
    # machine eligibility
    opt.add(Or([machine[i] == m for m in eligible[i]]))
    # machine domain (optional) ensure within 1..3
    opt.add(machine[i] >= 1, machine[i] <= 3)
    # precedence
    for p in prereq[i]:
        opt.add(start[i] >= end[p])

# non-overlap on same machine
for i in tasks:
    for j in tasks:
        if i < j:
            # if same machine, enforce ordering
            opt.add(Implies(machine[i] == machine[j], Or(end[i] <= start[j], end[j] <= start[i])))

# makespan variable
makespan = Int('makespan')
for i in tasks:
    opt.add(makespan >= end[i])
opt.minimize(makespan)

# check
res = opt.check()
if res == sat:
    m = opt.model()
    print('STATUS: sat')
    print('makespan =', m[makespan].as_long())
    for i in tasks:
        mi = m[machine[i]].as_long()
        si = m[start[i]].as_long()
        ei = m[end[i]].as_long()
        print(f'task {i}: machine = {mi}, start = {si}, end = {ei}')
else:
    print('STATUS: unsat')