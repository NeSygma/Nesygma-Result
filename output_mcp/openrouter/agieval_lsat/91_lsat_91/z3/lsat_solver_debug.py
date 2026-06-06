from z3 import *

p = [Int(f'p{i}') for i in range(1,6)]
t = [Int(f't{i}') for i in range(1,6)]
solver = Solver()
for i in range(5):
    solver.add(Or(p[i]==0, p[i]==1))
    solver.add(Or(t[i]==0, t[i]==1))
# constraints
solver.add(t[2]==1)
# exactly one adjacent pair of trad
adjacent = [And(t[i]==1, t[i+1]==1) for i in range(4)]
solver.add(Or(adjacent))
for i in range(4):
    for j in range(i+1,4):
        solver.add(Not(And(adjacent[i], adjacent[j])))
# fourth solo condition
solver.add(Or(And(p[3]==0, t[3]==1), And(p[3]==1, t[3]==0)))
# second vs fifth pianist diff
solver.add(p[1] != p[4])
# no trad until Wayne does a modern earlier
for i in range(5):
    earlier = []
    for j in range(i):
        earlier.append(And(p[j]==0, t[j]==0))
    if earlier:
        solver.add(Implies(t[i]==1, Or(earlier)))
    else:
        solver.add(t[i]==0)
# fifth is trad
solver.add(t[4]==1)

possible_p = [set() for _ in range(5)]
model_count=0
while solver.check() == sat:
    m = solver.model()
    model_count+=1
    for i in range(5):
        possible_p[i].add(m[p[i]].as_long())
    # block
    block = []
    for i in range(5):
        block.append(p[i] == m[p[i]])
        block.append(t[i] == m[t[i]])
    solver.add(Not(And(block)))

forced_count = sum(1 for s in possible_p if len(s)==1)
print('model_count', model_count)
print('possible_p sets:', possible_p)
print('forced_count', forced_count)