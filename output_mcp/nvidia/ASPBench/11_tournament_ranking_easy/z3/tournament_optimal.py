from z3 import *

teams = ['A','B','C','D','E']
rank = {t: Int(f'rank_{t}') for t in teams}

solver = Optimize()
# domain constraints
for t in teams:
    solver.add(rank[t] >= 0, rank[t] <= 4)
# all-different
solver.add(Distinct(list(rank.values())))

# match results
matches = [
    ('A','B'),('B','C'),('C','A'),('A','D'),('D','E'),
    ('E','C'),('B','E'),('D','C'),('A','E'),('B','D')
]

# violation sum
violation_sum = Sum([If(rank[w] > rank[l], 1, 0) for w,l in matches])
# objective
solver.minimize(violation_sum)

# solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("ranking:")
    for t in teams:
        print(f"{t} = {m[rank[t]].as_long() + 1}")
    print(f"violations = {m.eval(violation_sum)}")
else:
    print("STATUS: unsat")