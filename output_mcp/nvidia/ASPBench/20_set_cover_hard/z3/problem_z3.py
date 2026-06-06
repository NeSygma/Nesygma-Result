from z3 import *

# Problem data
sets = [
    {1,2,3,4,5},
    {1,6,11,16},
    {2,7,12,17},
    {3,8,13,18},
    {4,9,14,19},
    {5,10,15,20},
    {6,7,8,9,10},
    {1,3,5,7,9},
    {2,4,6,8,10},
    {1,2,3,4,5,6,7},
    {11,12,13,14,15},
    {8,9,10},
    {1,5,10,15},
    {16,17,18,19,20}
]
costs = [1,1,1,1,1,1,1,1,1,4,4,4,4,4]

# Category indices
A = [0,1,2]
B = [3,4,5]
C = [6,7,8]
specialized = [9,10,11,12,13]

# Create optimizer
solver = Optimize()

# Selection booleans
sel = [Bool(f'sel_{i}') for i in range(len(sets))]

# Base cost variable
base_cost = Int('base_cost')
solver.add(base_cost == Sum([If(sel[i], costs[i], 0) for i in range(len(sets))]))

# Map elements to covering sets
element_to_sets = {e: [] for e in range(1,21)}
for i, s in enumerate(sets):
    for e in s:
        element_to_sets[e].append(sel[i])

# Cover count per element (1..20)
cover_count = [Int(f'c{i}') for i in range(1,21)]
for e in range(1,21):
    # at least one set covers each element
    solver.add(cover_count[e-1] >= 1)
    # exact count for penalty calculation
    solver.add(cover_count[e-1] == Sum([If(s, 1, 0) for s in element_to_sets[e]]))

# Redundancy penalty
overcover = [Int(f'o{i}') for i in range(1,21)]
for i in range(20):
    solver.add(overcover[i] == If(cover_count[i] > 3, 1, 0))
penalty = 2 * Sum(overcover)

# Total cost
total_cost = base_cost + penalty
solver.minimize(total_cost)

# Prerequisite constraints
solver.add(Implies(sel[9], sel[0]))  # Set 9 requires Set 0
solver.add(Implies(sel[11], sel[6])) # Set 11 requires Set 6

# Mutual exclusion of specialized sets 12 and 13
solver.add(Or(sel[12] == 0, sel[13] == 0))

# Category balancing: if any specialized set is chosen, must pick at least one from A, B, C
solver.add(Implies(Or([sel[i] for i in specialized]),
                 And(Or([sel[i] for i in A]),
                     Or([sel[i] for i in B]),
                     Or([sel[i] for i in C]))))

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    # Selected sets
    selected = [i for i in range(len(sel)) if m[sel[i]]]
    print("selected_sets =", selected)
    print("total_sets =", len(selected))
    # Covered elements
    covered = [e for e in range(1,21) if m[cover_count[e-1]] > 0]
    print("covered_elements =", covered)
    # Cost components
    print("base_cost =", m[base_cost])
    print("redundancy_penalty =", m[penalty])
    print("total_cost =", m[total_cost])
else:
    print("STATUS: unsat")