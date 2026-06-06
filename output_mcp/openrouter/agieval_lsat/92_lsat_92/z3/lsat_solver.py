from z3 import *

# Define variables for 5 positions (0-indexed)
p = [Int(f'p{i}') for i in range(5)]  # 0 = Wayne, 1 = Zara
t = [Int(f't{i}') for i in range(5)]  # 0 = Modern, 1 = Traditional

solver = Solver()

# Domain constraints
for i in range(5):
    solver.add(Or(p[i] == 0, p[i] == 1))
    solver.add(Or(t[i] == 0, t[i] == 1))

# Base constraints
# 1. third solo is traditional (position 2)
solver.add(t[2] == 1)
# 2. Exactly two of the traditional pieces are performed consecutively -> exactly one adjacent pair of T's
adjacent_T = [If(And(t[i] == 1, t[i+1] == 1), 1, 0) for i in range(4)]
solver.add(Sum(adjacent_T) == 1)
# 3. Fourth solo condition: (Wayne & Traditional) OR (Zara & Modern)
cond3 = Or(And(p[3] == 0, t[3] == 1), And(p[3] == 1, t[3] == 0))
solver.add(cond3)
# 4. Pianist of second solo != pianist of fifth solo (positions 1 and 4)
solver.add(p[1] != p[4])
# 5. No traditional piece until Wayne performs at least one modern piece.
# For each position i, if there is no earlier (j < i) with (p[j]==0 and t[j]==0), then t[i]==0.
for i in range(5):
    earlier_conditions = []
    for j in range(i):
        earlier_conditions.append(And(p[j] == 0, t[j] == 0))
    if earlier_conditions:
        solver.add(Implies(Not(Or(earlier_conditions)), t[i] == 0))
    else:
        # i == 0, no earlier positions, so cannot be traditional
        solver.add(t[i] == 0)
# Additional given condition: fifth solo Wayne performs a traditional piece
solver.add(p[4] == 0)
solver.add(t[4] == 1)

# Define option constraints
opt_constraints = []
# A: Zara performs the first solo
opt_a = p[0] == 1
opt_constraints.append(("A", opt_a))
# B: Wayne performs the second solo
opt_b = p[1] == 0
opt_constraints.append(("B", opt_b))
# C: Zara performs the third solo
opt_c = p[2] == 1
opt_constraints.append(("C", opt_c))
# D: The second solo is a modern piece
opt_d = t[1] == 0
opt_constraints.append(("D", opt_d))
# E: The fourth solo is a traditional piece
opt_e = t[3] == 1
opt_constraints.append(("E", opt_e))

found_options = []
for letter, constr in opt_constraints:
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