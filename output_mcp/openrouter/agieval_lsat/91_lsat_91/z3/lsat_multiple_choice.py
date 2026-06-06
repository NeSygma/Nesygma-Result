from z3 import *

def base_solver():
    # 0 = Wayne, 1 = Zara
    p = [Int(f'p{i}') for i in range(1,6)]
    t = [Int(f't{i}') for i in range(1,6)]
    s = Solver()
    for i in range(5):
        s.add(Or(p[i]==0, p[i]==1))
        s.add(Or(t[i]==0, t[i]==1))
    # third solo is traditional (t=1)
    s.add(t[2]==1)
    # exactly one adjacent pair of traditional pieces
    adj = [And(t[i]==1, t[i+1]==1) for i in range(4)]
    s.add(Or(adj))
    for i in range(4):
        for j in range(i+1,4):
            s.add(Not(And(adj[i], adj[j])))
    # fourth solo condition: either Wayne traditional or Zara modern
    # Wayne =0, Zara=1 ; traditional=1, modern=0
    s.add(Or(And(p[3]==0, t[3]==1), And(p[3]==1, t[3]==0)))
    # pianist of second != pianist of fifth
    s.add(p[1] != p[4])
    # No traditional until Wayne performs a modern earlier
    for i in range(5):
        earlier = []
        for j in range(i):
            earlier.append(And(p[j]==0, t[j]==0))  # Wayne (0) modern (0)
        if earlier:
            s.add(Implies(t[i]==1, Or(earlier)))
        else:
            s.add(t[i]==0)  # first solo cannot be traditional
    # fifth is traditional
    s.add(t[4]==1)
    return s, p, t

# First, compute forced_count by enumerating all models
s0, p_vars, t_vars = base_solver()
possible = [set() for _ in range(5)]
model_cnt = 0
while s0.check() == sat:
    m = s0.model()
    model_cnt += 1
    for i in range(5):
        possible[i].add(m[p_vars[i]].as_long())
    # block this model
    block = []
    for i in range(5):
        block.append(p_vars[i] == m[p_vars[i]])
        block.append(t_vars[i] == m[t_vars[i]])
    s0.add(Not(And(block)))
forced_count = sum(1 for s in possible if len(s)==1)
# Now test each answer option
options = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
}
found = []
for letter, val in options.items():
    s_opt, _, _ = base_solver()
    # add a constraint that forced_count equals val (as a Boolean constant)
    if forced_count == val:
        s_opt.add(BoolVal(True))
    else:
        s_opt.add(BoolVal(False))
    if s_opt.check() == sat:
        found.append(letter)

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")