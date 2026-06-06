from z3 import *

solver = Solver()

# Declare variables for each letter
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')
letters = [S, E, N, D, M, O, R, Y]

# Constraint 1: Each letter is a digit 0-9
for l in letters:
    solver.add(And(l >= 0, l <= 9))

# Constraint 2: All letters have unique digits
solver.add(Distinct(letters))

# Constraint 3: Leading digits cannot be zero
solver.add(S != 0)
solver.add(M != 0)

# Constraint 4: Arithmetic correctness
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
    assignment = {}
    for var in letters:
        assignment[str(var)] = m[var].as_long()
    
    print("Assignment:")
    for letter in ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']:
        print(f"  {letter} = {assignment[letter]}")
    
    # Compute the numeric values
    s_val = assignment['S']
    e_val = assignment['E']
    n_val = assignment['N']
    d_val = assignment['D']
    m_val = assignment['M']
    o_val = assignment['O']
    r_val = assignment['R']
    y_val = assignment['Y']
    
    send_val = 1000*s_val + 100*e_val + 10*n_val + d_val
    more_val = 1000*m_val + 100*o_val + 10*r_val + e_val
    money_val = 10000*m_val + 1000*o_val + 100*n_val + 10*e_val + y_val
    
    print(f"\nEquation: {send_val} + {more_val} = {money_val}")
    print(f"Valid: {send_val + more_val == money_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")