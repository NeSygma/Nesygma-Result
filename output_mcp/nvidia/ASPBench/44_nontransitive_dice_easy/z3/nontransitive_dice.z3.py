from z3 import *

solver = Solver()

# Declare the six faces of each die
A = [Int(f'A{i}') for i in range(6)]
B = [Int(f'B{i}') for i in range(6)]
C = [Int(f'C{i}') for i in range(6)]

# Domain constraints: each face is an integer between 0 and 6 inclusive
for var in A + B + C:
    solver.add(var >= 0, var <= 6)

# Count winning pairs: X beats Y if X's face > Y's face in more than 18 of 36 matchups
# Therefore we require at least 19 winning pairs
wins_AB = Sum([If(Ai > Bj, 1, 0) for Ai in A for Bj in B])
solver.add(wins_AB >= 19)

wins_BC = Sum([If(Bi > Cj, 1, 0) for Bi in B for Cj in C])
solver.add(wins_BC >= 19)

wins_CA = Sum([If(Ci > Aj, 1, 0) for Ci in C for Aj in A])
solver.add(wins_CA >= 19)

# Solve the constraints
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("A =", [m.evaluate(x).as_long() for x in A])
    print("B =", [m.evaluate(x).as_long() for x in B])
    print("C =", [m.evaluate(x).as_long() for x in C])
elif result == unsat:
    print("STATUS: unsat")
    # In benchmark mode an unsat result signals a modeling error that must be refined
    print("RAW_RESULT: unsat (semantic/modeling error; refine required)")
else:
    print("STATUS: unknown")