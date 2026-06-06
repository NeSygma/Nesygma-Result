from z3 import *

solver = Solver()
# Declare position variables for each composition
posF = Int('posF')
posH = Int('posH')
posL = Int('posL')
posO = Int('posO')
posP = Int('posP')
posR = Int('posR')
posS = Int('posS')
posT = Int('posT')

# Domain constraints: positions 1..8
for v in [posF, posH, posL, posO, posP, posR, posS, posT]:
    solver.add(v >= 1, v <= 8)

# All compositions performed exactly once
solver.add(Distinct([posF, posH, posL, posO, posP, posR, posS, posT]))

# T is performed either immediately before F or immediately after R
solver.add(Or(posT == posF - 1, posT == posR + 1))

# At least two compositions are performed either after F and before R, or after R and before F
solver.add(Or(posF - posR >= 3, posR - posF >= 3))

# O is performed either first or fifth
solver.add(Or(posO == 1, posO == 5))

# The eighth composition performed is either L or H
solver.add(Or(posL == 8, posH == 8))

# P is performed at some time before S
solver.add(posP < posS)

# At least one composition is performed either after O and before S, or after S and before O
solver.add(Or(posO - posS >= 2, posS - posO >= 2))

# Antecedent: exactly two compositions are performed after F but before O
# This means O is three positions after F
solver.add(posO == posF + 3)

# Option constraints for R's position
opt_a_constr = posR == 1
opt_b_constr = posR == 3
opt_c_constr = posR == 4
opt_d_constr = posR == 6
opt_e_constr = posR == 7

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