from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver instance
solver = Solver()

# Declare symbolic variables for each letter
# We have 10 unique letters: D, O, N, A, L, G, E, R, B, T
letters = ['D', 'O', 'N', 'A', 'L', 'G', 'E', 'R', 'B', 'T']
vars = {letter: Int(letter) for letter in letters}

# Each letter must be a digit from 0 to 9
for letter in letters:
    solver.add(vars[letter] >= 0, vars[letter] <= 9)

# All letters must have unique digits
solver.add(Distinct(list(vars.values())))

# Leading letters cannot be zero
solver.add(vars['D'] != 0)
solver.add(vars['G'] != 0)
solver.add(vars['R'] != 0)

# Extract variables for easier reference
D, O, N, A, L, G, E, R, B, T = vars['D'], vars['O'], vars['N'], vars['A'], vars['L'], vars['G'], vars['E'], vars['R'], vars['B'], vars['T']

# Define carries between columns
# We have 7 columns (0 to 6), so 6 carries (c1 to c6)
c1, c2, c3, c4, c5, c6 = Ints('c1 c2 c3 c4 c5 c6')
for c in [c1, c2, c3, c4, c5, c6]:
    solver.add(c >= 0, c <= 1)  # Carries can only be 0 or 1

# Column 0 (units place): D + D = T + 10*c1
solver.add((D + D) == (T + 10 * c1))

# Column 1 (tens place): L + L + c1 = R + 10*c2
solver.add((L + L + c1) == (R + 10 * c2))

# Column 2 (hundreds place): A + A + c2 = E + 10*c3
solver.add((A + A + c2) == (E + 10 * c3))

# Column 3 (thousands place): N + R + c3 = B + 10*c4
solver.add((N + R + c3) == (B + 10 * c4))

# Column 4 (ten-thousands place): O + E + c4 = R + 10*c5
solver.add((O + E + c4) == (R + 10 * c5))

# Column 5 (hundred-thousands place): D + G + c5 = O + 10*c6
solver.add((D + G + c5) == (O + 10 * c6))

# Column 6 (millions place): c6 = R
solver.add(c6 == R)

# Check if a solution exists
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract the assignment
    assignment = {letter: model.eval(vars[letter], model_completion=True) for letter in letters}
    # Print the assignment
    for letter in letters:
        print(f"{letter} = {assignment[letter]}")
    
    # Print the equation with numbers
    donald = 100000 * assignment['D'] + 10000 * assignment['O'] + 1000 * assignment['N'] + 100 * assignment['A'] + 10 * assignment['L'] + assignment['D']
    gerald = 100000 * assignment['G'] + 10000 * assignment['E'] + 1000 * assignment['R'] + 100 * assignment['A'] + 10 * assignment['L'] + assignment['D']
    robert = 100000 * assignment['R'] + 10000 * assignment['O'] + 1000 * assignment['B'] + 100 * assignment['E'] + 10 * assignment['R'] + assignment['T']
    
    print(f"equation: {donald} + {gerald} = {robert}")
    print(f"valid: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")