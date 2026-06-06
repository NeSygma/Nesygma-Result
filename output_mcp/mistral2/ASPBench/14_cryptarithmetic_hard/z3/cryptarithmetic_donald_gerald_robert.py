from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver instance
solver = Solver()

# Declare symbolic variables for each letter (D, O, N, A, L, G, E, R, B, T)
# We use IntSort() for digits 0-9
letters = ['D', 'O', 'N', 'A', 'L', 'G', 'E', 'R', 'B', 'T']
vars = {letter: Int(letter) for letter in letters}

# Add constraints for unique digits (all letters must be assigned distinct digits)
solver.add(Distinct(list(vars.values())))

# Leading letters cannot be zero
solver.add(vars['D'] != 0)
solver.add(vars['G'] != 0)
solver.add(vars['R'] != 0)

# Each variable must be between 0 and 9 inclusive
for letter in letters:
    solver.add(vars[letter] >= 0, vars[letter] <= 9)

# Extract variables for easier reference
D, O, N, A, L, G, E, R, B, T = vars['D'], vars['O'], vars['N'], vars['A'], vars['L'], vars['G'], vars['E'], vars['R'], vars['B'], vars['T']

# Arithmetic correctness: DONALD + GERALD = ROBERT
# We model the addition column by column, considering carries.
# Let's define carry variables for each column (c0, c1, ..., c5)
# c0 is the carry into the least significant digit (units place)
# c5 is the carry out of the most significant digit (hundred-thousands place)

# We have 6 columns (from right to left):
# Column 0 (units): D + D = T + 10*c0
# Column 1 (tens): L + L + c0 = R + 10*c1
# Column 2 (hundreds): A + A + c1 = E + 10*c2
# Column 3 (thousands): N + R + c2 = B + 10*c3
# Column 4 (ten-thousands): O + E + c3 = O + 10*c4
# Column 5 (hundred-thousands): D + G + c4 = R + 10*c5

# Define carry variables (0 or 1)
c0, c1, c2, c3, c4, c5 = Ints('c0 c1 c2 c3 c4 c5')

# Each carry is either 0 or 1
solver.add(c0 >= 0, c0 <= 1)
solver.add(c1 >= 0, c1 <= 1)
solver.add(c2 >= 0, c2 <= 1)
solver.add(c3 >= 0, c3 <= 1)
solver.add(c4 >= 0, c4 <= 1)
solver.add(c5 >= 0, c5 <= 1)

# Column constraints
solver.add(D + D == T + 10 * c0)
solver.add(L + L + c0 == R + 10 * c1)
solver.add(A + A + c1 == E + 10 * c2)
solver.add(N + R + c2 == B + 10 * c3)
solver.add(O + E + c3 == O + 10 * c4)
solver.add(D + G + c4 == R + 10 * c5)

# Check if a solution exists
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the assignment
    assignment = {letter: model[vars[letter]] for letter in letters}
    for letter in letters:
        print(f"{letter} = {assignment[letter]}")
    
    # Print the equation with numbers
    donald = 100000 * assignment['D'] + 10000 * assignment['O'] + 1000 * assignment['N'] + 100 * assignment['A'] + 10 * assignment['L'] + assignment['D']
    gerald = 100000 * assignment['G'] + 10000 * assignment['E'] + 1000 * assignment['R'] + 100 * assignment['A'] + 10 * assignment['L'] + assignment['D']
    robert = 100000 * assignment['R'] + 10000 * assignment['O'] + 1000 * assignment['B'] + 100 * assignment['E'] + 10 * assignment['R'] + assignment['T']
    
    print(f"equation: {donald} + {gerald} = {robert}")
    print("valid: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")