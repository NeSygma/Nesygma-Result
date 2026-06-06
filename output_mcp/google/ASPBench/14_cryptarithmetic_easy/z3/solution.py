from z3 import *

# Define the letters
letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
# Create integer variables for each letter
vars = {l: Int(l) for l in letters}

solver = Solver()

# Constraint 1: Each letter is a digit 0-9
for l in letters:
    solver.add(vars[l] >= 0, vars[l] <= 9)

# Constraint 2: All letters must have different digits
solver.add(Distinct([vars[l] for l in letters]))

# Constraint 3: Leading letters cannot be 0
solver.add(vars['S'] != 0)
solver.add(vars['M'] != 0)

# Constraint 4: Arithmetic correctness
# SEND = 1000*S + 100*E + 10*N + D
# MORE = 1000*M + 100*O + 10*R + E
# MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

send = 1000 * vars['S'] + 100 * vars['E'] + 10 * vars['N'] + vars['D']
more = 1000 * vars['M'] + 100 * vars['O'] + 10 * vars['R'] + vars['E']
money = 10000 * vars['M'] + 1000 * vars['O'] + 100 * vars['N'] + 10 * vars['E'] + vars['Y']

solver.add(send + more == money)

# Solve
result = solver.check()

if result == sat:
    m = solver.model()
    assignment = {l: m[vars[l]].as_long() for l in letters}
    
    # Construct the equation string
    s_val = assignment['S']
    e_val = assignment['E']
    n_val = assignment['N']
    d_val = assignment['D']
    m_val = assignment['M']
    o_val = assignment['O']
    r_val = assignment['R']
    y_val = assignment['Y']
    
    send_num = 1000 * s_val + 100 * e_val + 10 * n_val + d_val
    more_num = 1000 * m_val + 100 * o_val + 10 * r_val + e_val
    money_num = 10000 * m_val + 1000 * o_val + 100 * n_val + 10 * e_val + y_val
    
    print("STATUS: sat")
    print(f"assignment: {assignment}")
    print(f"equation: {send_num} + {more_num} = {money_num}")
    print("valid: True")
else:
    print("STATUS: unsat")