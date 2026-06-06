from z3 import *

solver = Solver()

# Define positions for each composition (1-8)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# All positions must be between 1 and 8
solver.add([And(1 <= var, var <= 8) for var in [F, H, L, O, P, R, S, T]])

# All positions must be distinct
solver.add(Distinct(F, H, L, O, P, R, S, T))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(F == T + 1, T == R + 1))

# Constraint 2: At least two compositions between F and R
solver.add(Abs(F - R) >= 3)

# Constraint 3: O is first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: Eighth composition is L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P before S
solver.add(P < S)

# Constraint 6: At least one composition between O and S
solver.add(Abs(O - S) >= 2)

# Additional: O is immediately after T
solver.add(O == T + 1)

# Find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {
        'F': m[F].as_long(),
        'H': m[H].as_long(),
        'L': m[L].as_long(),
        'O': m[O].as_long(),
        'P': m[P].as_long(),
        'R': m[R].as_long(),
        'S': m[S].as_long(),
        'T': m[T].as_long()
    }
    solutions.append(sol)
    # Block this solution
    solver.add(Or([var != m[var] for var in [F, H, L, O, P, R, S, T]]))

print(f"Found {len(solutions)} solutions with O immediately after T")
for i, sol in enumerate(solutions[:10]):  # Show first 10
    print(f"Solution {i+1}: F={sol['F']}, H={sol['H']}, L={sol['L']}, O={sol['O']}, P={sol['P']}, R={sol['R']}, S={sol['S']}, T={sol['T']}")

# Check what positions F can be in
f_positions = set(sol['F'] for sol in solutions)
print(f"\nF can be in positions: {sorted(f_positions)}")