from z3 import *

# Declare variables for each letter and carries
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')
c1, c2, c3 = Ints('c1 c2 c3')

solver = Solver()

# Leading zero constraints
solver.add(S != 0)
solver.add(M != 0)

# All letters must be distinct digits
solver.add(Distinct([S, E, N, D, M, O, R, Y]))

# Each letter is a digit 0-9
for var in [S, E, N, D, M, O, R, Y]:
    solver.add(var >= 0, var <= 9)

# Carries are 0 or 1
solver.add(c1 >= 0, c1 <= 1)
solver.add(c2 >= 0, c2 <= 1)
solver.add(c3 >= 0, c3 <= 1)

# From puzzle analysis, M must be 1 (the only possible carry out)
solver.add(M == 1)

# Columnar addition constraints
solver.add(D + E == Y + 10 * c1)
solver.add(N + R + c1 == E + 10 * c2)
solver.add(E + O + c2 == N + 10 * c3)
solver.add(S + M + c3 == O + 10)

# Solve and output
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"S = {model[S].as_long()}")
    print(f"E = {model[E].as_long()}")
    print(f"N = {model[N].as_long()}")
    print(f"D = {model[D].as_long()}")
    print(f"M = {model[M].as_long()}")
    print(f"O = {model[O].as_long()}")
    print(f"R = {model[R].as_long()}")
    print(f"Y = {model[Y].as_long()}")
    # Compute the numeric values
    SEND = 1000*model[S].as_long() + 100*model[E].as_long() + 10*model[N].as_long() + model[D].as_long()
    MORE = 1000*model[M].as_long() + 100*model[O].as_long() + 10*model[R].as_long() + model[E].as_long()
    MONEY = 10000*model[M].as_long() + 1000*model[O].as_long() + 100*model[N].as_long() + 10*model[E].as_long() + model[Y].as_long()
    print(f"{SEND} + {MORE} = {MONEY}")
else:
    print("STATUS: unsat")