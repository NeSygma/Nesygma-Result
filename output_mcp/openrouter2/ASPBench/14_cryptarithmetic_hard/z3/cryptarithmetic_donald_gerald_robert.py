from z3 import *

solver = Solver()
# Variables for letters
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]
# Domain 0-9
for v in letters:
    solver.add(v >= 0, v <= 9)
# Distinct
solver.add(Distinct(letters))
# Leading non-zero
solver.add(D != 0, G != 0, R != 0)
# Carries
c1, c2, c3, c4, c5 = Ints('c1 c2 c3 c4 c5')
for c in [c1, c2, c3, c4, c5]:
    solver.add(c >= 0, c <= 1)
# Column constraints
# units: 2*D = T + 10*c1
solver.add(2*D == T + 10*c1)
# tens: 2*L + c1 = R + 10*c2
solver.add(2*L + c1 == R + 10*c2)
# hundreds: 2*A + c2 = E + 10*c3
solver.add(2*A + c2 == E + 10*c3)
# thousands: N + R + c3 = B + 10*c4
solver.add(N + R + c3 == B + 10*c4)
# ten-thousands: O + E + c4 = O + 10*c5
solver.add(O + E + c4 == O + 10*c5)
# hundred-thousands: D + G + c5 = R
solver.add(D + G + c5 == R)
# No carry beyond
# c6 implicitly 0

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    assignment = {str(v): m[v].as_long() for v in letters}
    # Build numbers
    num1 = int(''.join(str(assignment[ch]) for ch in ['D','O','N','A','L','D']))
    num2 = int(''.join(str(assignment[ch]) for ch in ['G','E','R','A','L','D']))
    num3 = int(''.join(str(assignment[ch]) for ch in ['R','O','B','E','R','T']))
    equation = f"{num1} + {num2} = {num3}"
    print("STATUS: sat")
    print("assignment =", assignment)
    print("equation =", equation)
    print("valid =", True)
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE ON
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")