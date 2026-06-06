from z3 import *

solver = Solver()

# Positions 1-8
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

vars_list = [F, H, L, O, P, R, S, T]
for v in vars_list:
    solver.add(v >= 1, v <= 8)

solver.add(Distinct(vars_list))

# Condition 1
solver.add(Or(T == F - 1, T == R + 1))

# Condition 2: |F-R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: Eighth is L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P before S
solver.add(P < S)

# Condition 6: |O-S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Given: T=5, F=6
solver.add(T == 5)
solver.add(F == 6)

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {v: m.eval(v, model_completion=True).as_long() for v in vars_list}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != sol[v] for v in vars_list]))

print(f"Total solutions: {len(solutions)}")
# Collect possible S values
s_positions = set()
for sol in solutions:
    s_positions.add(sol[S])
    print(f"F={sol[F]}, H={sol[H]}, L={sol[L]}, O={sol[O]}, P={sol[P]}, R={sol[R]}, S={sol[S]}, T={sol[T]}")

print(f"\nPossible S positions: {sorted(s_positions)}")