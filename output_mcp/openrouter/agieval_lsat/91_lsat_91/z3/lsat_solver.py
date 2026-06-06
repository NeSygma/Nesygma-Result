from z3 import *

# Variables
p = [Int(f'p{i}') for i in range(1,6)]  # pianist: 0=Wayne,1=Zara
t = [Int(f't{i}') for i in range(1,6)]  # piece type: 0=modern,1=traditional

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(Or(p[i]==0, p[i]==1))
    solver.add(Or(t[i]==0, t[i]==1))

# 1. third solo is traditional
solver.add(t[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively.
# There is at least one adjacent pair of traditional pieces, and no other adjacent pair.
adjacent = []
for i in range(4):
    adjacent.append(And(t[i]==1, t[i+1]==1))
# At least one adjacent pair
solver.add(Or(adjacent))
# No two distinct adjacent pairs (i.e., at most one)
for i in range(4):
    for j in range(i+1,4):
        solver.add(Not(And(adjacent[i], adjacent[j])))
# Also prevent three in a row (which would create two overlapping pairs). The above already prevents overlapping because overlapping pairs share an index, they'd be two distinct pairs -> disallowed.

# 3. Fourth solo condition
cond3 = Or(And(p[3]==0, t[3]==1), And(p[3]==1, t[3]==0))
solver.add(cond3)

# 4. Pianist of second solo != pianist of fifth solo
solver.add(p[1] != p[4])

# 5. No traditional piece until Wayne performs at least one modern piece.
# For each traditional piece at position i, there exists j < i with p[j]==0 and t[j]==0.
for i in range(5):
    # if t[i]==1 then exists earlier Wayne modern
    earlier_conditions = []
    for j in range(i):
        earlier_conditions.append(And(p[j]==0, t[j]==0))
    if earlier_conditions:
        solver.add(Implies(t[i]==1, Or(earlier_conditions)))
    else:
        # i==0, no earlier, so cannot be traditional
        solver.add(t[i]==0)

# Additional given condition: fifth solo is traditional
solver.add(t[4]==1)

# Enumerate all models to find possible pianist values per position
possible_p = [set() for _ in range(5)]
models = []
while solver.check() == sat:
    m = solver.model()
    # record pianist values
    for i in range(5):
        val = m.evaluate(p[i]).as_long()
        possible_p[i].add(val)
    # block this model
    block = []
    for i in range(5):
        block.append(p[i] == m.evaluate(p[i]))
    for i in range(5):
        block.append(t[i] == m.evaluate(t[i]))
    solver.add(Not(And(block)))

forced_count = sum(1 for s in possible_p if len(s)==1)
# Prepare option constraints as BoolVals
opt_a_constr = BoolVal(forced_count == 1)
opt_b_constr = BoolVal(forced_count == 2)
opt_c_constr = BoolVal(forced_count == 3)
opt_d_constr = BoolVal(forced_count == 4)
opt_e_constr = BoolVal(forced_count == 5)

# LSAT Multiple Choice Skeleton
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