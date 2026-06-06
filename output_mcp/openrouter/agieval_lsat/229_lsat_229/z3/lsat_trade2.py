from z3 import *
import itertools, collections

# Owners: 0=RealProp,1=Southco,2=Trustcorp
owners_list = ['G','F','L','K','M','O','Y','Z']
# class mapping
cls = {'G':1,'F':1,'L':2,'K':2,'M':2,'O':2,'Y':3,'Z':3}
# initial ownership dict
init = {'G':0,'Y':0,'Z':0,'F':1,'L':1,'K':2,'M':2,'O':2}

# Generate all possible trades from a state
def trades_from(state):
    res = []
    # list of owners for each building
    for b1,b2 in itertools.combinations(owners_list,2):
        o1, o2 = state[b1], state[b2]
        if o1==o2:
            continue
        c1, c2 = cls[b1], cls[b2]
        # type1: same class swap
        if c1==c2:
            new = state.copy()
            new[b1], new[b2] = o2, o1
            res.append(new)
        # type2: class1 for two class2
        # need one building class1 and another class2, and the trade is between two owners, but gives two class2 to owner of class1 and gives class1 to owner of class2? Actually trade is one class1 building for two class2 buildings. So one owner gives class1 and receives two class2; the other gives two class2 and receives class1.
        # We'll consider triples: need a class1 building and two class2 buildings owned by the other owner.
    # handle type2 and type3 separately using combos of three buildings
    # type2: pick class1 building b1 owned by o1, and two class2 buildings b2,b3 owned by o2
    for b1 in owners_list:
        if cls[b1]!=1: continue
        o1 = state[b1]
        # choose two distinct class2 buildings owned by a different owner o2
        class2_buildings = [b for b in owners_list if cls[b]==2 and state[b]!=o1]
        for b2,b3 in itertools.combinations(class2_buildings,2):
            o2 = state[b2]
            if state[b3]!=o2: continue
            # perform trade: o1 gives b1, receives b2,b3; o2 gives b2,b3, receives b1
            new = state.copy()
            new[b1] = o2
            new[b2] = o1
            new[b3] = o1
            res.append(new)
    # type3: one class2 for two class3
    for b1 in owners_list:
        if cls[b1]!=2: continue
        o1 = state[b1]
        class3_buildings = [b for b in owners_list if cls[b]==3 and state[b]!=o1]
        for b2,b3 in itertools.combinations(class3_buildings,2):
            o2 = state[b2]
            if state[b3]!=o2: continue
            new = state.copy()
            new[b1] = o2
            new[b2] = o1
            new[b3] = o1
            res.append(new)
    return res

# BFS to collect reachable states (limit depth to avoid infinite loops)
reachable = set()
queue = collections.deque()
queue.append(init)
reachable.add(tuple(sorted(init.items())))
while queue:
    cur = queue.popleft()
    for nxt in trades_from(cur):
        key = tuple(sorted(nxt.items()))
        if key not in reachable:
            reachable.add(key)
            queue.append(nxt)
# Convert reachable to list of dicts
reachable_states = [dict(state) for state in (dict(t) for t in reachable)]
print(f"Total reachable states: {len(reachable_states)}")

# Build Z3 variables for final owners
owner_vars = {b: Int(f'owner_{b}') for b in owners_list}
solver = Solver()
# domain constraints
for b in owners_list:
    solver.add(owner_vars[b] >= 0, owner_vars[b] <= 2)
# Constrain to be one of reachable states
or_clauses = []
for st in reachable_states:
    clause = And([owner_vars[b] == st[b] for b in owners_list])
    or_clauses.append(clause)
solver.add(Or(or_clauses))
# Add premise: Trustcorp (2) owns no class2 buildings after trades
for b in owners_list:
    if cls[b]==2:
        solver.add(owner_vars[b] != 2)

# Define option constraints
optA = Or(owner_vars['G']==0, owner_vars['F']==0)  # RealProp owns a class1 building
optB = And(owner_vars['G']!=1, owner_vars['F']!=1, owner_vars['Y']!=1, owner_vars['Z']!=1)  # Southco only class2
optC = Or([owner_vars[b]==1 for b in owners_list])  # Southco owns at least one building (i.e., made a trade?)
optD = owner_vars['G']==2
optE = owner_vars['Z']==2
options = [("A", optA), ("B", optB), ("C", optC), ("D", optD), ("E", optE)]

found_options = []
for letter, opt in options:
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(opt))
    if s.check() == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")