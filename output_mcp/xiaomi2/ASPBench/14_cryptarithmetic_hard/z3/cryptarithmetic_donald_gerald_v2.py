from z3 import *

solver = Solver()

# Declare symbolic variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# Constraint 1: Each letter is a digit 0-9
for l in letters:
    solver.add(l >= 0, l <= 9)

# Constraint 2: All letters have distinct digits
solver.add(Distinct(letters))

# Constraint 3: Leading digits cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Constraint 4: Columnar addition with carry variables
#   D O N A L D
# + G E R A L D
# = R O B E R T
#
# Column 0 (ones):     D + D = T + 10*c1
# Column 1 (tens):     L + L + c1 = R + 10*c2
# Column 2 (hundreds): A + A + c2 = E + 10*c3
# Column 3 (thousands):N + R + c3 = B + 10*c4
# Column 4 (ten-thousands): O + E + c4 = O + 10*c5
# Column 5 (hundred-thousands): D + G + c5 = R

c1, c2, c3, c4, c5 = Ints('c1 c2 c3 c4 c5')

# Carry values must be 0 or 1 (or 2 for columns with two same digits added)
solver.add(c1 >= 0, c1 <= 1)
solver.add(c2 >= 0, c2 <= 1)
solver.add(c3 >= 0, c3 <= 1)
solver.add(c4 >= 0, c4 <= 1)
solver.add(c5 >= 0, c5 <= 1)

# Column 0: D + D = T + 10*c1
solver.add(D + D == T + 10 * c1)

# Column 1: L + L + c1 = R + 10*c2
solver.add(L + L + c1 == R + 10 * c2)

# Column 2: A + A + c2 = E + 10*c3
solver.add(A + A + c2 == E + 10 * c3)

# Column 3: N + R + c3 = B + 10*c4
solver.add(N + R + c3 == B + 10 * c4)

# Column 4: O + E + c4 = O + 10*c5
solver.add(O + E + c4 == O + 10 * c5)

# Column 5: D + G + c5 = R
solver.add(D + G + c5 == R)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Extract digit assignments
    assignment = {}
    for var in letters:
        assignment[str(var)] = m.evaluate(var).as_long()
    
    print("Assignment:")
    for letter, digit in sorted(assignment.items()):
        print(f"  {letter} = {digit}")
    
    # Compute the actual numbers
    d_val = assignment['D']
    o_val = assignment['O']
    n_val = assignment['N']
    a_val = assignment['A']
    l_val = assignment['L']
    g_val = assignment['G']
    e_val = assignment['E']
    r_val = assignment['R']
    b_val = assignment['B']
    t_val = assignment['T']
    
    donald_num = d_val*100000 + o_val*10000 + n_val*1000 + a_val*100 + l_val*10 + d_val
    gerald_num = g_val*100000 + e_val*10000 + r_val*1000 + a_val*100 + l_val*10 + d_val
    robert_num = r_val*100000 + o_val*10000 + b_val*1000 + e_val*100 + r_val*10 + t_val
    
    print(f"\nEquation: {donald_num} + {gerald_num} = {robert_num}")
    print(f"Valid: {donald_num + gerald_num == robert_num}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")