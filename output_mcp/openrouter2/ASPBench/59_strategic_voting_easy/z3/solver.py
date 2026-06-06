from z3 import *

# Define constants
candidates = ['A','B','C']
# Preference ranks: lower is better
pref = [
    [1,2,3],  # V1: A > B > C
    [1,3,2],  # V2: A > C > B
    [3,1,2],  # V3: B > C > A
    [3,2,1]   # V4: C > B > A
]
true_top = [0,0,1,2]  # indices of top preference for each voter

# Variables
v = [Int(f'v{i}') for i in range(4)]  # votes of each voter
c = [Bool(f'c{i}') for i in range(4)]  # coalition membership
w = Int('w')  # winner candidate index

solver = Solver()
# Domain constraints
for vi in v:
    solver.add(vi >= 0, vi <= 2)
solver.add(w >= 0, w <= 2)

# Vote constraints based on coalition membership
for i in range(4):
    # if in coalition, vote for winner
    solver.add(Implies(c[i], v[i] == w))
    # if not in coalition, vote truthfully
    solver.add(Implies(Not(c[i]), v[i] == true_top[i]))

# Count votes
count = [Sum([If(v[i] == j, 1, 0) for i in range(4)]) for j in range(3)]
# Winner constraints: w is one of the candidates with maximum votes
for j in range(3):
    solver.add(count[w] >= count[j])

# Coalition preference improvement: each coalition member prefers winner over A (index 0)
for i in range(4):
    solver.add(Implies(c[i], pref[i][w] < pref[i][0]))

# Search for minimal coalition size
min_k = None
for k in range(1,5):
    solver.push()
    solver.add(Sum([If(ci,1,0) for ci in c]) == k)
    if solver.check() == sat:
        min_k = k
        solver.pop()
        break
    solver.pop()

if min_k is not None:
    print("STATUS: sat")
    print(f"minimum_coalition_size = {min_k}")
else:
    print("STATUS: unsat")