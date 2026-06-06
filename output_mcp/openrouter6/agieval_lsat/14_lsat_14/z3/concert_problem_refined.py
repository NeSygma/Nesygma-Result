from z3 import *

solver = Solver()

# Declare position variables for each composition
pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T = Ints('pos_F pos_H pos_L pos_O pos_P pos_R pos_S pos_T')

# Domain constraints: positions between 1 and 8
solver.add(pos_F >= 1, pos_F <= 8)
solver.add(pos_H >= 1, pos_H <= 8)
solver.add(pos_L >= 1, pos_L <= 8)
solver.add(pos_O >= 1, pos_O <= 8)
solver.add(pos_P >= 1, pos_P <= 8)
solver.add(pos_R >= 1, pos_R <= 8)
solver.add(pos_S >= 1, pos_S <= 8)
solver.add(pos_T >= 1, pos_T <= 8)

# All positions distinct
solver.add(Distinct([pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]))

# Condition 1: T is immediately before F or immediately after R
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))

# Condition 2: At least two compositions between F and R
solver.add(Or(pos_F - pos_R >= 3, pos_R - pos_F >= 3))

# Condition 3: O is first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))

# Condition 4: Eighth composition is L or H
solver.add(Or(pos_L == 8, pos_H == 8))

# Condition 5: P before S
solver.add(pos_P < pos_S)

# Condition 6: At least one composition between O and S
solver.add(Or(pos_O - pos_S >= 2, pos_S - pos_O >= 2))

# Extra given: T is fifth and F is sixth
solver.add(pos_T == 5)
solver.add(pos_F == 6)

# Deduction: O cannot be 5 because T is 5, so O must be 1
solver.add(pos_O == 1)

# Now test each answer choice
found_options = []

# Option A: S == 4 or S == 7
solver.push()
solver.add(Or(pos_S == 4, pos_S == 7))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: S == 3 or S == 6
solver.push()
solver.add(Or(pos_S == 3, pos_S == 6))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S == 3 or S == 4
solver.push()
solver.add(Or(pos_S == 3, pos_S == 4))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: S == 2 or S == 7
solver.push()
solver.add(Or(pos_S == 2, pos_S == 7))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: S == 1 or S == 4
solver.push()
solver.add(Or(pos_S == 1, pos_S == 4))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")