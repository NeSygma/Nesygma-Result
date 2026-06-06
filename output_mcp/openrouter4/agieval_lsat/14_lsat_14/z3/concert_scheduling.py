from z3 import *

solver = Solver()

# Positions 1-8
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# All positions are from 1 to 8
vars_list = [F, H, L, O, P, R, S, T]
for v in vars_list:
    solver.add(v >= 1, v <= 8)

# All different positions
solver.add(Distinct(vars_list))

# Condition 1: T is either immediately before F or immediately after R
# T = F - 1  OR  T = R + 1
solver.add(Or(T == F - 1, T == R + 1))

# Condition 2: At least two compositions between F and R
# |F - R| - 1 >= 2  => |F - R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is before S
solver.add(P < S)

# Condition 6: At least one composition between O and S
# |O - S| - 1 >= 1 => |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Given: T is fifth, F is sixth
solver.add(T == 5)
solver.add(F == 6)

# Now evaluate each answer choice

# Option A: S is fourth or seventh
opt_a = Or(S == 4, S == 7)
# Option B: S is third or sixth
opt_b = Or(S == 3, S == 6)
# Option C: S is third or fourth
opt_c = Or(S == 3, S == 4)
# Option D: S is second or seventh
opt_d = Or(S == 2, S == 7)
# Option E: S is first or fourth
opt_e = Or(S == 1, S == 4)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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