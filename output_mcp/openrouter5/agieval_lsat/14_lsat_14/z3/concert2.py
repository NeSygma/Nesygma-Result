from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)

F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

solver = Solver()

# Each composition is performed exactly once, positions 1..8
compositions = [F, H, L, O, P, R, S, T]
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All distinct positions
solver.add(Distinct(compositions))

# Condition 1: T is performed either immediately before F or immediately after R.
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# Number of compositions between F and R >= 2 means |F - R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S.
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Given: T is fifth, F is sixth.
solver.add(T == 5)
solver.add(F == 6)

# Let's enumerate all possible solutions to see what positions S can take.
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {c: m.eval(c, model_completion=True).as_long() for c in compositions}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([c != m.eval(c, model_completion=True).as_long() for c in compositions]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: F={sol[F]}, H={sol[H]}, L={sol[L]}, O={sol[O]}, P={sol[P]}, R={sol[R]}, S={sol[S]}, T={sol[T]}")

# Collect all possible S values
s_positions = set(sol[S] for sol in solutions)
print(f"Possible S positions: {sorted(s_positions)}")

# Now evaluate each answer choice.
# Re-create solver for option checking
solver2 = Solver()
for c in compositions:
    solver2.add(c >= 1, c <= 8)
solver2.add(Distinct(compositions))
solver2.add(Or(T + 1 == F, R + 1 == T))
solver2.add(Or(F - R >= 3, R - F >= 3))
solver2.add(Or(O == 1, O == 5))
solver2.add(Or(L == 8, H == 8))
solver2.add(P < S)
solver2.add(Or(O - S >= 2, S - O >= 2))
solver2.add(T == 5)
solver2.add(F == 6)

options = {
    "A": Or(S == 4, S == 7),
    "B": Or(S == 3, S == 6),
    "C": Or(S == 3, S == 4),
    "D": Or(S == 2, S == 7),
    "E": Or(S == 1, S == 4)
}

found_options = []
for letter, constr in options.items():
    solver2.push()
    solver2.add(constr)
    res = solver2.check()
    if res == sat:
        found_options.append(letter)
    solver2.pop()

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")