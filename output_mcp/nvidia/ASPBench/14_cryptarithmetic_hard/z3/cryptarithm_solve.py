from z3 import *

solver = Solver()

# Declare letter variables
D = Int('D'); O = Int('O'); N = Int('N'); A = Int('A'); L = Int('L')
G = Int('G'); E = Int('E'); R = Int('R'); B = Int('B'); T = Int('T')

# Carry variables
c1 = Int('c1'); c2 = Int('c2'); c3 = Int('c3'); c4 = Int('c4'); c5 = Int('c5')

# All letters must be digits 0-9
for var in [D,O,N,A,L,G,E,R,B,T]:
    solver.add(var >= 0, var <= 9)

# Leading letters cannot be zero
solver.add(D != 0, G != 0, R != 0)

# All letters distinct (covers all 10 digits)
solver.add(Distinct([D,O,N,A,L,G,E,R,B,T]))

# Column constraints with carries
solver.add(D + D == T + 10*c1)                     # units
solver.add(L + L + c1 == R + 10*c2)                # tens
solver.add(A + A + c2 == E + 10*c3)                # hundreds
solver.add(N + R + c3 == B + 10*c4)                # thousands
solver.add(O + E + c4 == O + 10*c5)                # ten-thousands (simplifies to E + c4 == 10*c5)
solver.add(D + G + c5 == R)                        # hundred-thousands

# Carries are 0 or 1
for c in [c1,c2,c3,c4,c5]:
    solver.add(c >= 0, c <= 1)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print each letter assignment
    for var in [D,O,N,A,L,G,E,R,B,T]:
        print(f"{var.name} = {model[var]}")
else:
    print("STATUS: unsat")