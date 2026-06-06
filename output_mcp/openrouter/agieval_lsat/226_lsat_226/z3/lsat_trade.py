from z3 import *

# Companies: 0=RealProp (R), 1=Southco (S), 2=Trustcorp (T)
R, S, T = 0, 1, 2

# Buildings and classes
buildings = ['G','Y','Z','F','L','K','M','O']
cls = {
    'G': 1,
    'Y': 3,
    'Z': 3,
    'F': 1,
    'L': 2,
    'K': 2,
    'M': 2,
    'O': 2,
}
# Initial owners
init_owner = {
    'G': R,
    'Y': R,
    'Z': R,
    'F': S,
    'L': S,
    'K': T,
    'M': T,
    'O': T,
}

# Generate all possible final ownerships after exactly one trade
possible_finals = []

# Helper to copy dict
import copy

# Type 1: exchange one building for one building of same class between different companies
for b1 in buildings:
    for b2 in buildings:
        if b1 >= b2:  # avoid duplicates and self
            continue
        if cls[b1] != cls[b2]:
            continue
        if init_owner[b1] == init_owner[b2]:
            continue
        # swap owners
        new = init_owner.copy()
        o1 = init_owner[b1]
        o2 = init_owner[b2]
        new[b1] = o2
        new[b2] = o1
        possible_finals.append(new)

# Type 2: one class1 building for two class2 buildings
class1_buildings = [b for b in buildings if cls[b]==1]
class2_buildings = [b for b in buildings if cls[b]==2]
for b1 in class1_buildings:
    for b2 in class2_buildings:
        for b3 in class2_buildings:
            if b2 >= b3:  # ensure distinct unordered pair
                continue
            # owners must be different companies
            o1 = init_owner[b1]
            o2 = init_owner[b2]
            o3 = init_owner[b3]
            if o1 == o2 or o1 == o3:
                continue
            # also b2 and b3 must be owned by same company (the other party)
            if o2 != o3:
                continue
            new = init_owner.copy()
            # transfer
            new[b1] = o2  # class1 goes to class2 owner
            new[b2] = o1
            new[b3] = o1
            possible_finals.append(new)

# Type 3: one class2 building for two class3 buildings
class3_buildings = [b for b in buildings if cls[b]==3]
for b1 in class2_buildings:
    for b2 in class3_buildings:
        for b3 in class3_buildings:
            if b2 >= b3:
                continue
            o1 = init_owner[b1]
            o2 = init_owner[b2]
            o3 = init_owner[b3]
            if o1 == o2 or o1 == o3:
                continue
            if o2 != o3:
                continue
            new = init_owner.copy()
            new[b1] = o2
            new[b2] = o1
            new[b3] = o1
            possible_finals.append(new)

# Remove duplicates (dicts) by converting to tuple of owners in fixed order
unique = []
seen = set()
for d in possible_finals:
    tup = tuple(d[b] for b in buildings)
    if tup not in seen:
        seen.add(tup)
        unique.append(d)
possible_finals = unique

# Now set up Z3 variables for final owners
final = {b: Int(f'final_{b}') for b in buildings}
solver = Solver()
for b in buildings:
    solver.add(Or(final[b] == R, final[b] == S, final[b] == T))

# Constrain final owners to be one of the possible finals
or_clauses = []
for d in possible_finals:
    clause = And([final[b] == d[b] for b in buildings])
    or_clauses.append(clause)
solver.add(Or(or_clauses))

# Define option constraints
# Option A
opt_a = []
# RealProp: Flores Tower and Garza Tower -> R owns F and G
opt_a.append(final['F'] == R)
opt_a.append(final['G'] == R)
# Southco: Lynch, Yates, Zimmer -> S owns L, Y, Z
opt_a.append(final['L'] == S)
opt_a.append(final['Y'] == S)
opt_a.append(final['Z'] == S)
# Trustcorp unchanged: K,M,O owned by T
opt_a.append(final['K'] == T)
opt_a.append(final['M'] == T)
opt_a.append(final['O'] == T)
opt_a_constr = And(opt_a)

# Option B
opt_b = []
opt_b.append(final['G'] == R)
opt_b.append(final['K'] == R)
opt_b.append(final['O'] == R)
opt_b.append(final['F'] == S)
opt_b.append(final['L'] == S)
opt_b.append(final['M'] == T)
opt_b.append(final['Y'] == T)
opt_b.append(final['Z'] == T)
opt_b_constr = And(opt_b)

# Option C
opt_c = []
opt_c.append(final['G'] == R)
opt_c.append(final['L'] == R)
opt_c.append(final['F'] == S)
opt_c.append(final['Y'] == S)
opt_c.append(final['Z'] == S)
opt_c.append(final['K'] == T)
opt_c.append(final['M'] == T)
opt_c.append(final['O'] == T)
opt_c_constr = And(opt_c)

# Option D
opt_d = []
opt_d.append(final['G'] == R)
opt_d.append(final['M'] == R)
opt_d.append(final['Y'] == R)
opt_d.append(final['F'] == S)
opt_d.append(final['L'] == S)
opt_d.append(final['K'] == T)
opt_d.append(final['O'] == T)
opt_d.append(final['Z'] == T)
opt_d_constr = And(opt_d)

# Option E
opt_e = []
opt_e.append(final['G'] == R)
opt_e.append(final['Y'] == R)
opt_e.append(final['Z'] == R)
opt_e.append(final['L'] == S)
opt_e.append(final['O'] == S)
opt_e.append(final['F'] == T)
opt_e.append(final['K'] == T)
opt_e.append(final['M'] == T)
opt_e_constr = And(opt_e)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")