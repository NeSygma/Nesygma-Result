from z3 import *

solver = Solver()

# Declare variables for each letter
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')
letters = [S, E, N, D, M, O, R, Y]

# Domain constraints: 0-9
solver.add([And(l >= 0, l <= 9) for l in letters])

# All letters must be different
solver.add(Distinct(letters))

# Leading letters cannot be zero
solver.add(S != 0, M != 0)

# Arithmetic constraint: SEND + MORE = MONEY
SEND  = 1000*S + 100*E + 10*N + D
MORE  = 1000*M + 100*O + 10*R + E
MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
solver.add(SEND + MORE == MONEY)

# Check for a solution
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print assignment for each letter
    for l in letters:
        print(f"{l} = {int(m[l])}")
    # Build numeric equation string
    send_val  = int(m[S])*1000 + int(m[E])*100 + int(m[N])*10 + int(m[D])
    more_val  = int(m[M])*1000 + int(m[O])*100 + int(m[R])*10 + int(m[E])
    money_val = int(m[M])*10000 + int(m[O])*1000 + int(m[N])*100 + int(m[E])*10 + int(m[Y])
    print(f"equation = {send_val} + {more_val} = {money_val}")
    print("valid = True")
else:
    print("STATUS: unsat")