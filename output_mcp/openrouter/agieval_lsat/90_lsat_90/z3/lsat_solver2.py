from z3 import *

solver = Solver()

# 0 = Wayne, 1 = Zara
p = [Int(f'p{i}') for i in range(1,6)]
# 0 = modern, 1 = traditional
t = [Int(f't{i}') for i in range(1,6)]

# domain constraints
for i in range(5):
    solver.add(Or(p[i] == 0, p[i] == 1))
    solver.add(Or(t[i] == 0, t[i] == 1))

# 1. third solo is traditional (position 3)
solver.add(t[2] == 1)

# 2. Exactly two traditional pieces, and they are consecutive.
solver.add(Sum(t) == 2)
# there is exactly one adjacent pair of traditional pieces
pair = [And(t[i] == 1, t[i+1] == 1) for i in range(4)]
solver.add(Sum([If(pair[i], 1, 0) for i in range(4)]) == 1)
# No three consecutive traditional pieces (redundant but safe)
for i in range(3):
    solver.add(Not(And(t[i] == 1, t[i+1] == 1, t[i+2] == 1)))

# 3. Fourth solo condition: either Wayne traditional OR Zara modern
solver.add(Or(And(p[3] == 0, t[3] == 1), And(p[3] == 1, t[3] == 0)))

# 4. Pianist of second solo does not perform fifth solo
solver.add(p[1] != p[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
for i in range(5):
    prior = []
    for j in range(i):
        prior.append(And(p[j] == 0, t[j] == 0))
    if prior:
        solver.add(Implies(t[i] == 1, Or(prior)))
    else:
        solver.add(t[i] == 0)  # first solo cannot be traditional

# Premise: first and second solo same pianist
solver.add(p[0] == p[1])

# Option constraints
opt_a = p[0] == 1          # Zara first
opt_b = p[2] == 0          # Wayne third
opt_c = p[4] == 1          # Zara fifth
opt_d = t[1] == 1          # second traditional
opt_e = t[3] == 0          # fourth modern

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
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