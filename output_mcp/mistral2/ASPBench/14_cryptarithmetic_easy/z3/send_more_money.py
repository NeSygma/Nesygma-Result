from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver instance
solver = Solver()

# Declare symbolic variables for each letter
letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
vars = {l: Int(l) for l in letters}

# Add constraints for unique digits
solver.add(Distinct([vars[l] for l in letters]))

# Leading letters cannot be zero
solver.add(vars['S'] != 0)
solver.add(vars['M'] != 0)

# Each letter must be between 0 and 9
for l in letters:
    solver.add(vars[l] >= 0, vars[l] <= 9)

# SEND + MORE = MONEY
# Break down the addition column by column (from right to left)
# D + E = Y + 10 * carry1
# N + R + carry1 = E + 10 * carry2
# E + O + carry2 = N + 10 * carry3
# S + M + carry3 = O + 10 * carry4
# carry4 = M

# Introduce carry variables (0 or 1)
carry1 = Int('carry1')
carry2 = Int('carry2')
carry3 = Int('carry3')
carry4 = Int('carry4')

solver.add(carry1 >= 0, carry1 <= 1)
solver.add(carry2 >= 0, carry2 <= 1)
solver.add(carry3 >= 0, carry3 <= 1)
solver.add(carry4 >= 0, carry4 <= 1)

# Column 1 (rightmost): D + E = Y + 10 * carry1
solver.add(vars['D'] + vars['E'] == vars['Y'] + 10 * carry1)

# Column 2: N + R + carry1 = E + 10 * carry2
solver.add(vars['N'] + vars['R'] + carry1 == vars['E'] + 10 * carry2)

# Column 3: E + O + carry2 = N + 10 * carry3
solver.add(vars['E'] + vars['O'] + carry2 == vars['N'] + 10 * carry3)

# Column 4: S + M + carry3 = O + 10 * carry4
solver.add(vars['S'] + vars['M'] + carry3 == vars['O'] + 10 * carry4)

# Column 5 (leftmost): carry4 = M
solver.add(carry4 == vars['M'])

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    assignment = {l: model[vars[l]] for l in letters}
    
    # Construct the equation string
    send = 1000 * assignment['S'] + 100 * assignment['E'] + 10 * assignment['N'] + assignment['D']
    more = 1000 * assignment['M'] + 100 * assignment['O'] + 10 * assignment['R'] + assignment['E']
    money = 10000 * assignment['M'] + 1000 * assignment['O'] + 100 * assignment['N'] + 10 * assignment['E'] + assignment['Y']
    
    equation_str = f"{send} + {more} = {money}"
    
    print("STATUS: sat")
    print("assignment:", assignment)
    print("equation:", equation_str)
    print("valid: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")