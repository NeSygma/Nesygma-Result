from z3 import *
import itertools, collections

# Buildings and classes
buildings = ['G','F','L','K','M','O','Y','Z']
cls = {'G':1,'F':1,'L':2,'K':2,'M':2,'O':2,'Y':3,'Z':3}
# owners: 0=RealProp,1=Southco,2=Trustcorp
init = {'G':0,'Y':0,'Z':0,'F':1,'L':1,'K':2,'M':2,'O':2}

# Generate trades from a state, also indicate if trade involves owners 1 and 2
def trades_from(state):
    res = []
    # type1: swap two buildings of same class, different owners
    for b1,b2 in itertools.combinations(buildings,2):
        o1,o2 = state[b1], state[b2]
        if o1==o2: continue
        if cls[b1]==cls[b2]:
            new = state.copy()
            new[b1], new[b2] = o2, o1
            involves = ( (o1==1 and o2==2) or (o1==2 and o2==1) )
            res.append((new,involves))
    # type2: one class1 for two class2
    for b1 in buildings:
        if cls[b1]!=1: continue
        o1 = state[b1]
        # choose two distinct class2 buildings owned by a different owner o2
        class2 = [b for b in buildings if cls[b]==2 and state[b]!=o1]
        for b2,b3 in itertools.combinations(class2,2):
            o2 = state[b2]
            if state[b3]!=o2: continue
            new = state.copy()
            new[b1] = o2
            new[b2] = o1
            new[b3] = o1
            involves = ( (o1==1 and o2==2) or (o1==2 and o2==1) )
            res.append((new,involves))
    # type3: one class2 for two class3
    for b1 in buildings:
        if cls[b1]!=2: continue
        o1 = state[b1]
        class3 = [b for b in buildings if cls[b]==3 and state[b]!=o1]
        for b2,b3 in itertools.combinations(class3,2):
            o2 = state[b2]
            if state[b3]!=o2: continue
            new = state.copy()
            new[b1] = o2
            new[b2] = o1
            new[b3] = o1
            involves = ( (o1==1 and o2==2) or (o1==2 and o2==1) )
            res.append((new,involves))
    return res

# BFS over (state, flag) where flag indicates if a 1-2 trade occurred
visited = set()
queue = collections.deque()
queue.append( (init, False) )
visited.add( (tuple(sorted(init.items())), False) )
reachable = []  # list of (state, flag)
while queue:
    cur_state, cur_flag = queue.popleft()
    reachable.append( (cur_state, cur_flag) )
    for nxt_state, involves in trades_from(cur_state):
        nxt_flag = cur_flag or involves
        key = (tuple(sorted(nxt_state.items())), nxt_flag)
        if key not in visited:
            visited.add(key)
            queue.append( (nxt_state, nxt_flag) )

print(f"Total reachable (state,flag) combos: {len(reachable)}")

# Filter states where Trustcorp (2) owns no class2 buildings
valid_states = []
for st, flag in reachable:
    ok = True
    for b in buildings:
        if cls[b]==2 and st[b]==2:
            ok = False
            break
    if ok:
        valid_states.append( (st, flag) )
print(f"States satisfying premise: {len(valid_states)}")

# Build Z3 model for final owners (any of the valid states)
owner_vars = {b: Int(f'owner_{b}') for b in buildings}
solver = Solver()
for b in buildings:
    solver.add(owner_vars[b] >= 0, owner_vars[b] <= 2)
# Or of all valid states
or_clauses = []
for st,_ in valid_states:
    clause = And([owner_vars[b] == st[b] for b in buildings])
    or_clauses.append(clause)
solver.add(Or(or_clauses))

# Option definitions
optA = Or(owner_vars['G']==0, owner_vars['F']==0)  # RealProp owns a class1 building
optB = And(owner_vars['G']!=1, owner_vars['F']!=1, owner_vars['Y']!=1, owner_vars['Z']!=1)  # Southco only class2
# For C, we need to check if there exists a valid state with flag=False (i.e., no 1-2 trade). If none, then C is forced true.
# We'll handle C separately.
optD = owner_vars['G']==2
optE = owner_vars['Z']==2

# Determine which options are forced true across all valid_states
forced = []
# A,B,D,E via Z3 unsat of Not(option)
for letter, opt in [("A",optA),("B",optB),("D",optD),("E",optE)]:
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(opt))
    if s.check() == unsat:
        forced.append(letter)
# C: check if any valid state has flag=False
any_no_trade = any(flag==False for _,flag in valid_states)
if not any_no_trade:
    forced.append('C')

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
elif len(forced) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options forced {forced}")
else:
    print("STATUS: unsat")
    print("Refine: No options forced")