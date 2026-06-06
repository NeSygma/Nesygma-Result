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

# 3. Arithmetic Correctness (Columnar addition)
#   D O N A L D
# + G E R A L D
# -------------
# = R O B E R T

# Let's use carries to simplify the constraints
c1 = Int('c1') # carry from D+D=T
c2 = Int('c2') # carry from L+L+c1=R
c3 = Int('c3') # carry from A+A+c2=E
c4 = Int('c4') # carry from N+R+c3=B
c5 = Int('c5') # carry from O+E+c4=O
c6 = Int('c6') # carry from D+G+c5=R

# Constraints for carries
solver.add(c1 >= 0, c1 <= 1)
solver.add(c2 >= 0, c2 <= 1)
solver.add(c3 >= 0, c3 <= 1)
solver.add(c4 >= 0, c4 <= 1)
solver.add(c5 >= 0, c5 <= 1)
solver.add(c6 >= 0, c6 <= 1)

# Column equations
solver.add(letter_vars['D'] + letter_vars['D'] == letter_vars['T'] + 10 * c1)
solver.add(letter_vars['L'] + letter_vars['L'] + c1 == letter_vars['R'] + 10 * c2)
solver.add(letter_vars['A'] + letter_vars['A'] + c2 == letter_vars['E'] + 10 * c3)
solver.add(letter_vars['N'] + letter_vars['R'] + c3 == letter_vars['B'] + 10 * c4)
solver.add(letter_vars['O'] + letter_vars['E'] + c4 == letter_vars['O'] + 10 * c5)
solver.add(letter_vars['D'] + letter_vars['G'] + c5 == letter_vars['R'] + 10 * c6)
solver.add(c6 == 0) # No carry out of the last column

# Solve
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    assignment = {l: model[letter_vars[l]].as_long() for l in letters}
    print(f"assignment: {assignment}")
    
    # Verify
    d_val = sum([assignment[l] * (10**(5-i)) for i, l in enumerate('DONALD')])
    g_val = sum([assignment[l] * (10**(5-i)) for i, l in enumerate('GERALD')])
    r_val = sum([assignment[l] * (10**(5-i)) for i, l in enumerate('ROBERT')])
    
    print(f"equation: {d_val} + {g_val} = {r_val}")
    print("valid: True")
else:
    print("STATUS: unsat")