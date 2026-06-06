from z3 import *

# Create solver
solver = Solver()

# Declare die face variables
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Domain constraints: each face value is between 0 and 6 inclusive
for var in A + B + C:
    solver.add(var >= 0, var <= 6)

# Helper to compute win count between two dice
def win_count(die1, die2):
    return Sum([If(die1[i] > die2[j], 1, 0) for i in range(6) for j in range(6)])

# Nontransitive constraints
solver.add(win_count(A, B) > 18)  # A beats B
solver.add(win_count(B, C) > 18)  # B beats C
solver.add(win_count(C, A) > 18)  # C beats A

# Check for a solution
result = solver.check()
if result == sat:
    m = solver.model()
    # Extract dice values
    dice = {
        'A': [m.eval(A[i]).as_long() for i in range(6)],
        'B': [m.eval(B[i]).as_long() for i in range(6)],
        'C': [m.eval(C[i]).as_long() for i in range(6)]
    }
    # Compute win probabilities
    def prob(die1, die2):
        count = sum(1 for i in range(6) for j in range(6)
                    if m.eval(die1[i]).as_long() > m.eval(die2[j]).as_long())
        return count / 36.0
    win_probabilities = {
        'A_beats_B': prob(A, B),
        'B_beats_C': prob(B, C),
        'C_beats_A': prob(C, A)
    }
    # Output results
    print("STATUS: sat")
    print("dice =", dice)
    print("win_probabilities =", win_probabilities)
else:
    print("STATUS: unsat")