from z3 import *

# Define the letters
letters = ['D', 'O', 'N', 'A', 'L', 'G', 'E', 'R', 'B', 'T']
letter_vars = {l: Int(l) for l in letters}

solver = Solver()

# 1. Unique Digits: Each letter is 0-9
for l in letters:
    solver.add(letter_vars[l] >= 0, letter_vars[l] <= 9)

# All letters must be distinct
solver.add(Distinct([letter_vars[l] for l in letters]))

# 2. Leading Zeros: D, G, R cannot be 0
solver.add(letter_vars['D'] != 0)
solver.add(letter_vars['G'] != 0)
solver.add(letter_vars['R'] != 0)

# 3. Arithmetic Correctness
# DONALD = 100000*D + 10000*O + 1000*N + 100*A + 10*L + D
# GERALD = 100000*G + 10000*E + 1000*R + 100*A + 10*L + D
# ROBERT = 100000*R + 10000*O + 1000*B + 100*E + 10*R + T

donald = 100000 * letter_vars['D'] + 10000 * letter_vars['O'] + 1000 * letter_vars['N'] + 100 * letter_vars['A'] + 10 * letter_vars['L'] + letter_vars['D']
gerald = 100000 * letter_vars['G'] + 10000 * letter_vars['E'] + 1000 * letter_vars['R'] + 100 * letter_vars['A'] + 10 * letter_vars['L'] + letter_vars['D']
robert = 100000 * letter_vars['R'] + 10000 * letter_vars['O'] + 1000 * letter_vars['B'] + 100 * letter_vars['E'] + 10 * letter_vars['R'] + letter_vars['T']

solver.add(donald + gerald == robert)

# Solve
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    assignment = {l: model[letter_vars[l]].as_long() for l in letters}
    print(f"assignment: {assignment}")
    
    d_val = sum([assignment[l] * (10**(5-i)) for i, l in enumerate('DONALD')])
    g_val = sum([assignment[l] * (10**(5-i)) for i, l in enumerate('GERALD')])
    r_val = sum([assignment[l] * (10**(5-i)) for i, l in enumerate('ROBERT')])
    
    print(f"equation: {d_val} + {g_val} = {r_val}")
    print("valid: True")
else:
    print("STATUS: unsat")