from z3 import *

solver = Solver()

# Each composition gets a position 1-8
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F, H, L, O, P, R, S, T]

# All positions are between 1 and 8
for c in comps:
    solver.add(c >= 1, c <= 8)

# All distinct
solver.add(Distinct(comps))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R (in either direction)
solver.add(Or(F >= R + 3, R >= F + 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed before S
solver.add(P < S)

# Constraint 6: At least one composition between O and S (not adjacent)
solver.add(Or(S - O >= 2, O - S >= 2))

# Question constraint: Exactly two compositions are performed after F but before O
# This means F < O and O - F - 1 == 2, so O = F + 3
solver.add(F < O)
solver.add(O - F == 3)

# Now test each answer choice
found_options = []

# (A) R must be first
solver.push()
solver.add(R == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) R must be third
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) R must be fourth
solver.push()
solver.add(R == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) R must be sixth
solver.push()
solver.add(R == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) R must be seventh
solver.push()
solver.add(R == 7)
if solver.check() == sat:
    found_options.append("E")
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

# Also print a sample model for the correct answer
if len(found_options) == 1:
    print("\n--- Sample valid assignment ---")
    answer_map = {"A": 1, "B": 3, "C": 4, "D": 6, "E": 7}
    s2 = Solver()
    s2.add(solver.assertions())
    s2.add(R == answer_map[found_options[0]])
    if s2.check() == sat:
        m = s2.model()
        for c in comps:
            print(f"{c} = {m[c]}")