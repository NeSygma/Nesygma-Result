from z3 import *

# Declare integer variables for each letter
S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')

solver = Solver()

# Constraint 1: Each letter gets a digit from 0 to 9
letters = [S, E, N, D, M, O, R, Y]
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# Constraint 2: All letters must have different digits
solver.add(Distinct(letters))

# Constraint 3: Leading letters cannot be zero
solver.add(S != 0)
solver.add(M != 0)

# Constraint 4: Arithmetic correctness
# SEND = 1000*S + 100*E + 10*N + D
# MORE = 1000*M + 100*O + 10*R + E
# MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
solver.add(1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E == 10000*M + 1000*O + 100*N + 10*E + Y)

# Check for solution
BENCHMARK_MODE = True  # This is a model-finding problem
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract assignment
    assignment = {}
    for letter in letters:
        assignment[letter] = model[letter]
    
    # Build equation string
    send_val = 1000*assignment[S] + 100*assignment[E] + 10*assignment[N] + assignment[D]
    more_val = 1000*assignment[M] + 100*assignment[O] + 10*assignment[R] + assignment[E]
    money_val = 10000*assignment[M] + 1000*assignment[O] + 100*assignment[N] + 10*assignment[E] + assignment[Y]
    equation = f"{send_val} + {more_val} = {money_val}"
    
    # Print results
    print("STATUS: sat")
    print("assignment:", {str(k): int(v) for k, v in assignment.items()})
    print("equation:", equation)
    print("valid: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")