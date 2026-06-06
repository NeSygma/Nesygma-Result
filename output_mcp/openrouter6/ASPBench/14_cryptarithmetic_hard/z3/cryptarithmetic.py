from z3 import *

# Create solver
solver = Solver()

# Declare letter variables (digits 0-9)
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# All letters must be distinct digits 0-9
solver.add(Distinct(letters))
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# Leading digits cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Carries for each column (0 or 1)
c0, c1, c2, c3, c4, c5 = Ints('c0 c1 c2 c3 c4 c5')
for c in [c0, c1, c2, c3, c4, c5]:
    solver.add(c >= 0, c <= 1)

# Column-wise addition constraints
# Column 0 (units): D + D = T + 10*c0
solver.add(D + D == T + 10*c0)

# Column 1 (tens): L + L + c0 = R + 10*c1
solver.add(L + L + c0 == R + 10*c1)

# Column 2 (hundreds): A + A + c1 = E + 10*c2
solver.add(A + A + c1 == E + 10*c2)

# Column 3 (thousands): N + R + c2 = B + 10*c3
solver.add(N + R + c2 == B + 10*c3)

# Column 4 (ten-thousands): O + E + c3 = O + 10*c4  => E + c3 = 10*c4
solver.add(E + c3 == 10*c4)

# Column 5 (hundred-thousands): D + G + c4 = R + 10*c5
# Since ROBERT is 6 digits, c5 must be 0
solver.add(c5 == 0)
solver.add(D + G + c4 == R)

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract assignment
    assignment = {chr(65 + i): model[letters[i]] for i in range(10)}  # A=65, B=66, etc.
    # But letters are D,O,N,A,L,G,E,R,B,T - need mapping
    # Let's map manually
    assignment = {
        'D': model[D],
        'O': model[O],
        'N': model[N],
        'A': model[A],
        'L': model[L],
        'G': model[G],
        'E': model[E],
        'R': model[R],
        'B': model[B],
        'T': model[T]
    }
    # Print assignment
    print("assignment:", assignment)
    # Build equation string
    donald = f"{assignment['D']}{assignment['O']}{assignment['N']}{assignment['A']}{assignment['L']}{assignment['D']}"
    gerald = f"{assignment['G']}{assignment['E']}{assignment['R']}{assignment['A']}{assignment['L']}{assignment['D']}"
    robert = f"{assignment['R']}{assignment['O']}{assignment['B']}{assignment['E']}{assignment['R']}{assignment['T']}"
    equation = f"{donald} + {gerald} = {robert}"
    print("equation:", equation)
    print("valid: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")