from z3 import *

# Declare variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
vars = [D, O, N, A, L, G, E, R, B, T]

solver = Solver()
# Domain constraints 0-9
for v in vars:
    solver.add(v >= 0, v <= 9)
# All distinct
solver.add(Distinct(vars))
# Leading letters non-zero
solver.add(D != 0, G != 0, R != 0)
# Construct numbers
DONALD = D*10**5 + O*10**4 + N*10**3 + A*10**2 + L*10 + D
GERALD = G*10**5 + E*10**4 + R*10**3 + A*10**2 + L*10 + D
ROBERT = R*10**5 + O*10**4 + B*10**3 + E*10**2 + R*10 + T
# Arithmetic constraint
solver.add(DONALD + GERALD == ROBERT)

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print assignment
    for name, var in [('D', D), ('O', O), ('N', N), ('A', A), ('L', L), ('G', G), ('E', E), ('R', R), ('B', B), ('T', T)]:
        print(f"{name} = {m[var]}")
    # Also print the equation with numbers
    don = m.evaluate(DONALD, model_completion=True).as_long()
    ger = m.evaluate(GERALD, model_completion=True).as_long()
    rob = m.evaluate(ROBERT, model_completion=True).as_long()
    print(f"{don} + {ger} = {rob}")
else:
    print("STATUS: unsat")