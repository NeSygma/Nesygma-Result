from z3 import *
import itertools, collections

# Define data
buildings = [
    ('Garza', 1),   # 0
    ('Flores', 1),  # 1
    ('Yates', 3),   # 2
    ('Zimmer', 3),  # 3
    ('Lynch', 2),   # 4
    ('King', 2),    # 5
    ('Meyer', 2),   # 6
    ('Ortiz', 2)    # 7
]
num = len(buildings)
# Companies: 0=RealProp,1=Southco,2=Trustcorp
initial = [0,1,0,0,1,2,2,2]  # owner index per building

# Precompute class list
cls = [b[1] for b in buildings]

# Generate all possible trades from a state
def trades_from(state):
    res = []
    # For each ordered pair of companies i!=j
    for i in range(3):
        for j in range(3):
            if i==j: continue
            # Buildings owned by i and j
            owned_i = [idx for idx in range(num) if state[idx]==i]
            owned_j = [idx for idx in range(num) if state[idx]==j]
            # 1) same class swap
            for a in owned_i:
                for b in owned_j:
                    if cls[a]==cls[b]:
                        new = list(state)
                        new[a], new[b] = j, i
                        res.append(tuple(new))
            # 2) class1 for two class2
            # i gives class1 a, receives two class2 b,c from j
            class1_i = [a for a in owned_i if cls[a]==1]
            class2_j = [b for b in owned_j if cls[b]==2]
            if class1_i and len(class2_j)>=2:
                for a in class1_i:
                    for b,c in itertools.combinations(class2_j,2):
                        new = list(state)
                        new[a]=j
                        new[b]=i
                        new[c]=i
                        res.append(tuple(new))
            # 3) class2 for two class3
            class2_i = [a for a in owned_i if cls[a]==2]
            class3_j = [b for b in owned_j if cls[b]==3]
            if class2_i and len(class3_j)>=2:
                for a in class2_i:
                    for b,c in itertools.combinations(class3_j,2):
                        new = list(state)
                        new[a]=j
                        new[b]=i
                        new[c]=i
                        res.append(tuple(new))
    return res

# BFS to find all reachable states
reachable = set()
queue = collections.deque()
start = tuple(initial)
reachable.add(start)
queue.append(start)
while queue:
    s = queue.popleft()
    for ns in trades_from(s):
        if ns not in reachable:
            reachable.add(ns)
            queue.append(ns)

# Now encode reachable states into Z3 as Or of equalities
owner = [Int(f'owner_{i}') for i in range(num)]
solver = Solver()
for o in owner:
    solver.add(o>=0, o<=2)
# Add constraint that the tuple is one of reachable
or_clauses = []
for state in reachable:
    clause = And([owner[i]==state[i] for i in range(num)])
    or_clauses.append(clause)
solver.add(Or(or_clauses))

# Define option constraints
opt_a = And(owner[0]==0, owner[1]==0)  # RealProp owns Garza and Flores
opt_b = And(owner[1]==1, owner[6]==1)  # Southco owns Flores and Meyer
opt_c = And(owner[0]==1, owner[4]==1)  # Southco owns Garza and Lynch
opt_d = And(owner[1]==2, owner[7]==2)  # Trustcorp owns Flores and Ortiz
opt_e = And(owner[0]==2, owner[6]==2)  # Trustcorp owns Garza and Meyer
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found)==1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found)>1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")