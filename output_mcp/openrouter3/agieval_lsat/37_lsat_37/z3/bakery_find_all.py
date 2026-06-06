from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# For each cookie type, we have 3 batches (1st, 2nd, 3rd)
O1, O2, O3 = Ints('O1 O2 O3')  # oatmeal batches 1,2,3
P1, P2, P3 = Ints('P1 P2 P3')  # peanut butter batches 1,2,3
S1, S2, S3 = Ints('S1 S2 S3')  # sugar batches 1,2,3

solver = Solver()

# Base constraints
solver.add(O1 >= 0, O1 <= 4)
solver.add(O2 >= 0, O2 <= 4)
solver.add(O3 >= 0, O3 <= 4)
solver.add(P1 >= 0, P1 <= 4)
solver.add(P2 >= 0, P2 <= 4)
solver.add(P3 >= 0, P3 <= 4)
solver.add(S1 >= 0, S1 <= 4)
solver.add(S2 >= 0, S2 <= 4)
solver.add(S3 >= 0, S3 <= 4)

solver.add(Distinct([O1, O2, O3]))
solver.add(Distinct([P1, P2, P3]))
solver.add(Distinct([S1, S2, S3]))

solver.add(Or(O1 == 0, O2 == 0, O3 == 0,
              P1 == 0, P2 == 0, P3 == 0,
              S1 == 0, S2 == 0, S3 == 0))

solver.add(O2 == P1)
solver.add(S2 == 3)

# Find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {
        'O1': m[O1], 'O2': m[O2], 'O3': m[O3],
        'P1': m[P1], 'P2': m[P2], 'P3': m[P3],
        'S1': m[S1], 'S2': m[S2], 'S3': m[S3]
    }
    solutions.append(sol)
    # Block this solution
    solver.add(Or(
        O1 != m[O1], O2 != m[O2], O3 != m[O3],
        P1 != m[P1], P2 != m[P2], P3 != m[P3],
        S1 != m[S1], S2 != m[S2], S3 != m[S3]
    ))

print(f"Found {len(solutions)} solutions:")
for i, sol in enumerate(solutions):
    print(f"\nSolution {i+1}:")
    print(f"  Oatmeal: {days[sol['O1']]}, {days[sol['O2']]}, {days[sol['O3']]}")
    print(f"  Peanut butter: {days[sol['P1']]}, {days[sol['P2']]}, {days[sol['P3']]}")
    print(f"  Sugar: {days[sol['S1']]}, {days[sol['S2']]}, {days[sol['S3']]}")