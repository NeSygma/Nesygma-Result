from z3 import *

solver = Solver()
# Variables for positions
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')
vars = [F,H,L,O,P,R,S,T]
# domain 1..8
for v in vars:
    solver.add(v >= 1, v <= 8)
# all distinct
solver.add(Distinct(vars))
# Base constraints
solver.add(Or(T == F - 1, T == R + 1))
solver.add(Abs(F - R) >= 3)
solver.add(Or(O == 1, O == 5))
solver.add(Or(L == 8, H == 8))
solver.add(P < S)
solver.add(Abs(O - S) >= 2)
# Condition: exactly two compositions after F but before O => O - F == 3
solver.add(O - F == 3)

# Now test each option for R position
options = {
    'A': 1,
    'B': 3,
    'C': 4,
    'D': 6,
    'E': 7
}
found = []
for letter, pos in options.items():
    solver.push()
    solver.add(R == pos)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

print('found_options =', found)
if len(found) == 1:
    print('STATUS: sat')
    print('answer:' + found[0])
elif len(found) > 1:
    print('STATUS: unsat')
    print('Refine: Multiple options found', found)
else:
    print('STATUS: unsat')
    print('Refine: No options found')