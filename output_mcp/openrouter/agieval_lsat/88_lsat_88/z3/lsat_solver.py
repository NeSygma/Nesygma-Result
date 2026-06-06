from z3 import *

solver = Solver()

# Number of solos
N = 5
# Pianist: True = Wayne, False = Zara
p = [Bool(f'p_{i}') for i in range(N)]
# Type: True = Traditional, False = Modern
t = [Bool(f't_{i}') for i in range(N)]

# Base constraints
# 1. third solo (index 2) is traditional
solver.add(t[2] == True)
# 2. Exactly two traditional pieces total and they are consecutive
# Sum of traditional pieces == 2
solver.add(Sum([If(t[i], 1, 0) for i in range(N)]) == 2)
# There exists a consecutive pair of traditional pieces
consec = []
for i in range(N-1):
    consec.append(And(t[i], t[i+1]))
solver.add(Or(consec))
# 3. Fourth solo (index 3): either Wayne performs a traditional piece or Zara performs a modern piece
cond4 = Or(And(p[3] == True, t[3] == True), And(p[3] == False, t[3] == False))
solver.add(cond4)
# 4. Pianist of second solo (index1) != pianist of fifth solo (index4)
solver.add(p[1] != p[4])
# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# For each position i where t[i] is True, there must exist j < i with p[j]==True and t[j]==False.
for i in range(N):
    # if t[i] then exists earlier Wayne modern
    earlier = []
    for j in range(i):
        earlier.append(And(p[j] == True, t[j] == False))
    # If there is no earlier position, then cannot be traditional
    if earlier:
        solver.add(Implies(t[i], Or(earlier)))
    else:
        solver.add(t[i] == False)

# Define option constraints mapping
options = {}
# A: first, third, fourth are traditional (positions 0,2,3)
opt_a = []
for i in range(N):
    if i in [0,2,3]:
        opt_a.append(t[i] == True)
    else:
        opt_a.append(t[i] == False)
options['A'] = And(opt_a)
# B: second, third, fourth (1,2,3)
opt_b = []
for i in range(N):
    if i in [1,2,3]:
        opt_b.append(t[i] == True)
    else:
        opt_b.append(t[i] == False)
options['B'] = And(opt_b)
# C: third and fourth (2,3)
opt_c = []
for i in range(N):
    if i in [2,3]:
        opt_c.append(t[i] == True)
    else:
        opt_c.append(t[i] == False)
options['C'] = And(opt_c)
# D: third and fifth (2,4)
opt_d = []
for i in range(N):
    if i in [2,4]:
        opt_d.append(t[i] == True)
    else:
        opt_d.append(t[i] == False)
options['D'] = And(opt_d)
# E: fourth and fifth (3,4)
opt_e = []
for i in range(N):
    if i in [3,4]:
        opt_e.append(t[i] == True)
    else:
        opt_e.append(t[i] == False)
options['E'] = And(opt_e)

found_options = []
for letter, constr in [("A", options['A']), ("B", options['B']), ("C", options['C']), ("D", options['D']), ("E", options['E'])]:
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