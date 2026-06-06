from z3 import *

# Candidates: 0=A, 1=B, 2=C
candidates = [0,1,2]

# Voter true preference ranks (lower is better)
rank = {
    0: {0:0, 1:1, 2:2},  # V1: A>B>C
    1: {0:0, 2:1, 1:2},  # V2: A>C>B
    2: {1:0, 2:1, 0:2},  # V3: B>C>A
    3: {2:0, 1:1, 0:2}   # V4: C>B>A
}

orig_votes = [0,0,1,2]  # V1->A, V2->A, V3->B, V4->C
orig_winner = 0  # A

# Search for minimal coalition size
for k in range(1,5):
    s = Solver()
    # coalition selection booleans
    sel = [Bool(f"sel_{i}") for i in range(4)]
    s.add(PbEq([(sel[i],1) for i in range(4)], k))
    # vote variables (0..2)
    vote = [Int(f"vote_{i}") for i in range(4)]
    for i in range(4):
        s.add(And(vote[i] >= 0, vote[i] <= 2))
        s.add(Implies(Not(sel[i]), vote[i] == orig_votes[i]))
    # count votes per candidate
    count = [Sum([If(vote[i] == c, 1, 0) for i in range(4)]) for c in candidates]
    # winner variable w (candidate index)
    w = Int('w')
    s.add(Or([w == c for c in candidates]))
    # winner must not be original winner (A)
    s.add(w != orig_winner)
    # enforce w is the unique winner (strictly more votes than any other candidate)
    for c in candidates:
        # if w == c then count[c] > count[d] for all d != c
        other_counts = [count[d] for d in candidates if d != c]
        s.add(Implies(w == c, And([count[c] > oc for oc in other_counts])))
    # At least one coalition member prefers w over original winner
    pref_conditions = []
    for i in range(4):
        # construct condition: rank[i][w] < rank[i][orig_winner]
        better_expr = Or([And(w == c, rank[i][c] < rank[i][orig_winner]) for c in candidates])
        pref_conditions.append(And(sel[i], better_expr))
    s.add(Or(pref_conditions))
    # Check satisfiability
    if s.check() == sat:
        m = s.model()
        print("STATUS: sat")
        print(f"minimum_coalition_size = {k}")
        coalition = [i+1 for i in range(4) if is_true(m.eval(sel[i]))]
        print("coalition_members =", coalition)
        new_votes = [m.eval(vote[i]).as_long() for i in range(4)]
        print("new_votes =", new_votes)
        winner = m.eval(w).as_long()
        print("winner =", winner)
        break
else:
    print("STATUS: unsat")