from z3 import *

solver = Solver()

# Each composition gets a position 1-8
# F, H, L, O, P, R, S, T
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# All positions are between 1 and 8
for c in comps:
    solver.add(c >= 1, c <= 8)

# All distinct
solver.add(Distinct(comps))

# Given: P is third, S is sixth
solver.add(P == 3)
solver.add(S == 6)

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R (|F-R| >= 3)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed before S (already satisfied: P=3 < S=6)
solver.add(P < S)

# Constraint 6: At least one composition between O and S (|O-S| >= 2)
solver.add(Or(O - S >= 2, S - O >= 2))

# Now evaluate each answer choice for position 5
# (A) F or H at position 5
opt_a = Or(F == 5, H == 5)
# (B) F or O at position 5
opt_b = Or(F == 5, O == 5)
# (C) F or T at position 5
opt_c = Or(F == 5, T == 5)
# (D) H or L at position 5
opt_d = Or(H == 5, L == 5)
# (E) O or R at position 5
opt_e = Or(O == 5, R == 5)

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