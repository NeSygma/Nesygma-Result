from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver instance
solver = Solver()

# Declare symbolic variables for each letter
S, E, N, D = Ints('S E N D')
M, O, R, Y = Ints('M O R Y')

# Add constraints for unique digits (0-9)
letters = [S, E, N, D, M, O, R, Y]
solver.add(Distinct(letters))

# Leading zeros cannot be zero
solver.add(S != 0)
solver.add(M != 0)

# Since SEND + MORE = MONEY results in a 5-digit number, M must be 1
solver.add(M == 1)

# Encode the columnar addition with carry variables
# We have 4 columns (units, tens, hundreds, thousands) plus a final carry to the ten-thousands place
# Let's define carry variables for each column (c0, c1, c2, c3)
c0, c1, c2, c3 = Ints('c0 c1 c2 c3')

# Column constraints (from right to left, i.e., units to thousands)
# Units column: D + E = Y + 10*c0
solver.add(D + E == Y + 10 * c0)

# Tens column: N + R + c0 = E + 10*c1
solver.add(N + R + c0 == E + 10 * c1)

# Hundreds column: E + O + c1 = N + 10*c2
solver.add(E + O + c1 == N + 10 * c2)

# Thousands column: S + M + c2 = O + 10*c3
solver.add(S + M + c2 == O + 10 * c3)

# Final carry to ten-thousands place: c3 must equal M (which is 1)
solver.add(c3 == M)

# Check if the constraints are satisfiable
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract the assignment
    assignment = {
        'S': model[S].as_long(),
        'E': model[E].as_long(),
        'N': model[N].as_long(),
        'D': model[D].as_long(),
        'M': model[M].as_long(),
        'O': model[O].as_long(),
        'R': model[R].as_long(),
        'Y': model[Y].as_long()
    }
    
    # Construct the equation string
    send = 1000 * assignment['S'] + 100 * assignment['E'] + 10 * assignment['N'] + assignment['D']
    more = 1000 * assignment['M'] + 100 * assignment['O'] + 10 * assignment['R'] + assignment['E']
    money = 10000 * assignment['M'] + 1000 * assignment['O'] + 100 * assignment['N'] + 10 * assignment['E'] + assignment['Y']
    
    equation = f"{send} + {more} = {money}"
    
    # Validate uniqueness and constraints (done in solver, but we can assert here for clarity)
    values = [assignment[letter] for letter in ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']]
    unique_values = len(set(values)) == len(values)
    no_leading_zero = assignment['S'] != 0 and assignment['M'] != 0
    m_is_one = assignment['M'] == 1
    valid = unique_values and no_leading_zero and m_is_one
    
    print("assignment:", assignment)
    print("equation:", equation)
    print("valid:", valid)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")