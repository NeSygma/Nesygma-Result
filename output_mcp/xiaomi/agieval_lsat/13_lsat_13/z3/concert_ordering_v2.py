from z3 import *

solver = Solver()

# Define positions for each composition (1-8)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Each composition is in a unique position from 1 to 8
for c in compositions:
    solver.add(c >= 1, c <= 8)
solver.add(Distinct(compositions))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions are performed either after F and before R, 
# or after R and before F
# This means |pos(F) - pos(R)| >= 3 (at least 2 compositions between them)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed before S
solver.add(P < S)

# Constraint 6: At least one composition is performed either after O and before S,
# or after S and before O
# This means |pos(O) - pos(S)| >= 2 (at least 1 composition between them)
solver.add(Or(O - S >= 2, S - O >= 2))

# Now test each option for P's position - we want to find which one is UNSATISFIABLE
impossible_options = []

# Option A: P is second
solver.push()
solver.add(P == 2)
if solver.check() == unsat:
    impossible_options.append("A")
solver.pop()

# Option B: P is third
solver.push()
solver.add(P == 3)
if solver.check() == unsat:
    impossible_options.append("B")
solver.pop()

# Option C: P is fourth
solver.push()
solver.add(P == 4)
if solver.check() == unsat:
    impossible_options.append("C")
solver.pop()

# Option D: P is sixth
solver.push()
solver.add(P == 6)
if solver.check() == unsat:
    impossible_options.append("D")
solver.pop()

# Option E: P is seventh
solver.push()
solver.add(P == 7)
if solver.check() == unsat:
    impossible_options.append("E")
solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")

# Print details for debugging
print(f"\nImpossible positions for P: {impossible_options}")
print(f"Possible positions for P: {[x for x in ['A','B','C','D','E'] if x not in impossible_options]}")