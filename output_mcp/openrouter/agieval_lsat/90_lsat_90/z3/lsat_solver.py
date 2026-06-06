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

# 2. Exactly two of the traditional pieces are performed consecutively.
# Define adjacent pair indicators
pair = [And(t[i] == 1, t[i+1] == 1) for i in range(4)]
solver.add(Sum([If(pair[i], 1, 0) for i in range(4)]) == 1)
# No three consecutive traditional pieces
for i in range(3):
    solver.add(Not(And(t[i] == 1, t[i+1] == 1, t[i+2] == 1)))

# 3. Fourth solo condition: either Wayne traditional OR Zara modern
solver.add(Or(And(p[3] == 0, t[3] == 1), And(p[3] == 1, t[3] == 0)))

# 4. Pianist of second solo does not perform fifth solo
solver.add(p[1] != p[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# For each position i where t[i]==1, there must exist a prior j < i with p[j]==0 (Wayne) and t[j]==0 (modern).
for i in range(5):
    # if t[i] is traditional then there exists prior j
    prior_exists = []
    for j in range(i):
        prior_exists.append(And(p[j] == 0, t[j] == 0))
    if prior_exists:
        solver.add(Implies(t[i] == 1, Or(prior_exists)))
    else:
        # i == 0, cannot have traditional because no prior Wayne modern
        solver.add(t[i] == 0)

# Premise: first and second solo same pianist
solver.add(p[0] == p[1])

# Define option constraints
# A: Zara performs first solo -> p[0]==1
opt_a = p[0] == 1
# B: Wayne performs third solo -> p[2]==0
opt_b = p[2] == 0
# C: Zara performs fifth solo -> p[4]==1
opt_c = p[4] == 1
# D: second solo is traditional -> t[1]==1
opt_d = t[1] == 1
# E: fourth solo is modern -> t[3]==0
opt_e = t[3] == 0

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