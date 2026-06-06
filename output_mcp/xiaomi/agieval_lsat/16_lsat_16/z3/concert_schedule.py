from z3 import *

solver = Solver()

# Eight compositions: F, H, L, O, P, R, S, T
# Position variables: pos[X] = position (1-8) where composition X is performed
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
comps = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Each composition is in a unique position from 1 to 8
for c in comps:
    solver.add(c >= 1, c <= 8)
solver.add(Distinct(comps))

# S is performed fourth
solver.add(S == 4)

# Condition 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R,
# or after R and before F
# This means |pos[F] - pos[R]| >= 3 (at least 2 compositions between them)
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S,
# or after S and before O
# This means |pos[O] - pos[S]| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Now test each answer choice for positions 1, 2, 3
# (A) F=1, H=2, P=3
opt_a = And(F == 1, H == 2, P == 3)
# (B) H=1, P=2, L=3
opt_b = And(H == 1, P == 2, L == 3)
# (C) O=1, P=2, R=3
opt_c = And(O == 1, P == 2, R == 3)
# (D) O=1, P=2, T=3
opt_d = And(O == 1, P == 2, T == 3)
# (E) P=1, R=2, T=3
opt_e = And(P == 1, R == 2, T == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for n, c in zip(names, comps):
            print(f"  {n} = {m[c]}")
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