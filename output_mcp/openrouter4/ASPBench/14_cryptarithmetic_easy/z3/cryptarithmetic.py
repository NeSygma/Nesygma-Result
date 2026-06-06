from z3 import *

solver = Solver()

# Create integer variables for each letter
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')

# Each letter must be a digit from 0 to 9
letters = [S, E, N, D, M, O, R, Y]
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# All letters must have different digits
solver.add(Distinct(letters))

# Leading letters S and M cannot be 0
solver.add(S != 0)
solver.add(M != 0)

# Arithmetic constraint: SEND + MORE = MONEY
send = 1000*S + 100*E + 10*N + D
more = 1000*M + 100*O + 10*R + E
money = 10000*M + 1000*O + 100*N + 10*E + Y

solver.add(send + more == money)

# Check and print results
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
    
    s_val = model[S].as_long()
    e_val = model[E].as_long()
    n_val = model[N].as_long()
    d_val = model[D].as_long()
    m_val = model[M].as_long()
    o_val = model[O].as_long()
    r_val = model[R].as_long()
    y_val = model[Y].as_long()
    
    send_val = 1000*s_val + 100*e_val + 10*n_val + d_val
    more_val = 1000*m_val + 100*o_val + 10*r_val + e_val
    money_val = 10000*m_val + 1000*o_val + 100*n_val + 10*e_val + y_val
    
    equation_str = f"{send_val} + {more_val} = {money_val}"
    print(f"\nequation: {equation_str}")
    
    # Use the Z3 variables as keys, not strings
    var_map = {
        'S': S, 'E': E, 'N': N, 'D': D,
        'M': M, 'O': O, 'R': R, 'Y': Y
    }
    assignment = {letter: model[var].as_long() for letter, var in var_map.items()}
    print(f"\nassignment: {assignment}")
else:
    print("STATUS: unsat")