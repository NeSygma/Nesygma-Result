from z3 import *

solver = Solver()

# Each composition gets a position 1-8, all distinct
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F, H, L, O, P, R, S, T]

# All positions are between 1 and 8, all distinct
for c in comps:
    solver.add(And(c >= 1, c <= 8))
solver.add(Distinct(comps))

# Given: T is performed fifth and F is performed sixth
solver.add(T == 5)
solver.add(F == 6)

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R (in either direction)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed before S
solver.add(P < S)

# Constraint 6: At least one composition between O and S (in either direction)
solver.add(Or(S - O >= 2, O - S >= 2))

# Now evaluate each answer choice for S
# (A) fourth or seventh: S == 4 or S == 7
# (B) third or sixth: S == 3 or S == 6
# (C) third or fourth: S == 3 or S == 4
# (D) second or seventh: S == 2 or S == 7
# (E) first or fourth: S == 1 or S == 4

options = {
    "A": Or(S == 4, S == 7),
    "B": Or(S == 3, S == 6),
    "C": Or(S == 3, S == 4),
    "D": Or(S == 2, S == 7),
    "E": Or(S == 1, S == 4),
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: F={m[F]}, H={m[H]}, L={m[L]}, O={m[O]}, P={m[P]}, R={m[R]}, S={m[S]}, T={m[T]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")