from z3 import *

solver = Solver()

# Declare symbolic variables for each letter
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')
letters = [S, E, N, D, M, O, R, Y]

# 1. Unique Digits: Each letter must be a different digit from 0-9
for l in letters:
    solver.add(l >= 0, l <= 9)
solver.add(Distinct(letters))

# 2. Leading Zeros: S and M cannot be 0
solver.add(S != 0)
solver.add(M != 0)

# 3. Arithmetic Correctness: SEND + MORE = MONEY
# SEND = 1000*S + 100*E + 10*N + D
# MORE = 1000*M + 100*O + 10*R + E
# MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
SEND = 1000*S + 100*E + 10*N + D
MORE = 1000*M + 100*O + 10*R + E
MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

solver.add(SEND + MORE == MONEY)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Build assignment dictionary
    assignment = {
        'S': m[S].as_long(),
        'E': m[E].as_long(),
        'N': m[N].as_long(),
        'D': m[D].as_long(),
        'M': m[M].as_long(),
        'O': m[O].as_long(),
        'R': m[R].as_long(),
        'Y': m[Y].as_long()
    }
    
    send_val = 1000*assignment['S'] + 100*assignment['E'] + 10*assignment['N'] + assignment['D']
    more_val = 1000*assignment['M'] + 100*assignment['O'] + 10*assignment['R'] + assignment['E']
    money_val = 10000*assignment['M'] + 1000*assignment['O'] + 100*assignment['N'] + 10*assignment['E'] + assignment['Y']
    
    print(f"assignment: {assignment}")
    print(f"equation: {send_val} + {more_val} = {money_val}")
    print(f"valid: {send_val + more_val == money_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")