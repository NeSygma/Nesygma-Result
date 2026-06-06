from z3 import *

# Define data
sets = [
    {"elements": [1,2,3,4,5], "cost": 1},  #0
    {"elements": [1,6,11,16], "cost": 1}, #1
    {"elements": [2,7,12,17], "cost": 1}, #2
    {"elements": [3,8,13,18], "cost": 1}, #3
    {"elements": [4,9,14,19], "cost": 1}, #4
    {"elements": [5,10,15,20], "cost": 1}, #5
    {"elements": [6,7,8,9,10], "cost": 1}, #6
    {"elements": [1,3,5,7,9], "cost": 1}, #7
    {"elements": [2,4,6,8,10], "cost": 1}, #8
    {"elements": [1,2,3,4,5,6,7], "cost": 4}, #9 specialized
    {"elements": [11,12,13,14,15], "cost": 4}, #10 specialized
    {"elements": [8,9,10], "cost": 4}, #11 specialized
    {"elements": [1,5,10,15], "cost": 4}, #12 specialized
    {"elements": [16,17,18,19,20], "cost": 4}, #13 specialized
]

num_sets = len(sets)
universe = list(range(1,21))

# Decision variables
sel = [Bool(f"sel_{i}") for i in range(num_sets)]

solver = Optimize()

# 1. Full coverage
for e in universe:
    covering = [If(sel[i], 1, 0) for i, s in enumerate(sets) if e in s["elements"]]
    solver.add(Sum(covering) >= 1)

# 2. Prerequisites
solver.add(Implies(sel[9], sel[0]))  # Set 9 requires Set 0
solver.add(Implies(sel[11], sel[6])) # Set 11 requires Set 6

# 3. Mutual exclusion
solver.add(Not(And(sel[12], sel[13])))

# 4. Category balancing if any specialized selected
specialized_idxs = [9,10,11,12,13]
any_specialized = Or([sel[i] for i in specialized_idxs])
# categories standard sets
catA = [0,1,2]
catB = [3,4,5]
catC = [6,7,8]
solver.add(Implies(any_specialized, Sum([If(sel[i],1,0) for i in catA]) >= 1))
solver.add(Implies(any_specialized, Sum([If(sel[i],1,0) for i in catB]) >= 1))
solver.add(Implies(any_specialized, Sum([If(sel[i],1,0) for i in catC]) >= 1))

# 5. Redundancy penalty expression
penalty_terms = []
for e in universe:
    coverage = Sum([If(sel[i], 1, 0) for i, s in enumerate(sets) if e in s["elements"]])
    penalty_terms.append(If(coverage > 3, 2, 0))
redundancy_penalty = Sum(penalty_terms)

# Base cost
base_cost = Sum([If(sel[i], sets[i]["cost"], 0) for i in range(num_sets)])

total_cost = base_cost + redundancy_penalty

# Objective: minimize total cost
solver.minimize(total_cost)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    selected = [i for i in range(num_sets) if m.eval(sel[i])]
    base_val = m.eval(base_cost).as_long()
    penalty_val = m.eval(redundancy_penalty).as_long()
    total_val = m.eval(total_cost).as_long()
    print("STATUS: sat")
    print("selected_sets =", selected)
    print("base_cost =", base_val)
    print("redundancy_penalty =", penalty_val)
    print("total_cost =", total_val)
else:
    print("STATUS: unsat")