from z3 import *

solver = Solver()

# Declare integer variables for each letter
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')

# Domain constraints: each letter is a digit 0-9
letters = [S, E, N, D, M, O, R, Y]
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# All letters must have different digits
solver.add(Distinct(letters))

# Leading letters cannot be zero
solver.add(S != 0)
solver.add(M != 0)

# Arithmetic constraint: SEND + MORE = MONEY
# SEND = 1000*S + 100*E + 10*N + D
# MORE = 1000*M + 100*O + 10*R + E
# MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
solver.add(1000*S + 100*E + 10*N + D +
           1000*M + 100*O + 10*R + E ==
           10000*M + 1000*O + 100*N + 10*E + Y)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"S = {model[S]}")
    print(f"E = {model[E]}")
    print(f"N = {model[N]}")
    print(f"D = {model[D]}")
    print(f"M = {model[M]}")
    print(f"O = {model[O]}")
    print(f"R = {model[R]}")
    print(f"Y = {model[Y]}")
    send_val = 1000*model[S].as_long() + 100*model[E].as_long() + 10*model[N].as_long() + model[D].as_long()
    more_val = 1000*model[M].as_long() + 100*model[O].as_long() + 10*model[R].as_long() + model[E].as_long()
    money_val = 10000*model[M].as_long() + 1000*model[O].as_long() + 100*model[N].as_long() + 10*model[E].as_long() + model[Y].as_long()
    print(f"Equation: {send_val} + {more_val} = {money_val}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")