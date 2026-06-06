from z3 import *

# Define variables for positions of clues (1..7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
vars = [R, S, T, U, W, X, Z]

solver_base = Solver()
# Domain constraints
for v in vars:
    solver_base.add(v >= 1, v <= 7)
# All distinct
solver_base.add(Distinct(vars))
# T before W with exactly two chapters separating: pos_W = pos_T + 3
solver_base.add(W == T + 3)
# S and Z not adjacent
solver_base.add(Abs(S - Z) != 1)
# W and X not adjacent
solver_base.add(Abs(W - X) != 1)
# U and X adjacent
solver_base.add(Abs(U - X) == 1)

# Original constraint: T not in chapter 1
orig = T != 1

# Option constraints dictionary
options = {
    "A": U != 2,
    "B": W != 4,
    "C": X != 6,
    "D": U < T,
    "E": X < W,
}

found_options = []
for letter, opt in options.items():
    # Check if original implies option: base + original + Not(option) unsat?
    s1 = Solver()
    s1.add(solver_base.assertions())
    s1.add(orig)
    s1.add(Not(opt))
    res1 = s1.check()
    # Check if option implies original: base + option + Not(original) unsat?
    s2 = Solver()
    s2.add(solver_base.assertions())
    s2.add(opt)
    s2.add(Not(orig))
    res2 = s2.check()
    if res1 == unsat and res2 == unsat:
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