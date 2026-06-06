from z3 import *

# Create the solver
solver = Solver()

# Define the dice faces
# Each die has 6 faces, values in {0, 1, 2, 3, 4, 5, 6}
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Constraints on face values
for i in range(6):
    solver.add(A[i] >= 0, A[i] <= 6)
    solver.add(B[i] >= 0, B[i] <= 6)
    solver.add(C[i] >= 0, C[i] <= 6)

# Function to calculate number of wins
def count_wins(die1, die2):
    return Sum([If(die1[i] > die2[j], 1, 0) for i in range(6) for j in range(6)])

# Winning criteria: P(X > Y) > 0.5 means > 18 wins out of 36
solver.add(count_wins(A, B) > 18)
solver.add(count_wins(B, C) > 18)
solver.add(count_wins(C, A) > 18)

# Solve
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    def get_vals(die):
        return sorted([m.eval(f).as_long() for f in die])
    
    A_vals = get_vals(A)
    B_vals = get_vals(B)
    C_vals = get_vals(C)
    
    print(f"A = {A_vals}")
    print(f"B = {B_vals}")
    print(f"C = {C_vals}")
    
    def calc_prob(d1, d2):
        wins = 0
        for x in d1:
            for y in d2:
                if x > y:
                    wins += 1
        return wins / 36.0

    print(f"A_beats_B: {calc_prob(A_vals, B_vals)}")
    print(f"B_beats_C: {calc_prob(B_vals, C_vals)}")
    print(f"C_beats_A: {calc_prob(C_vals, A_vals)}")
else:
    print("STATUS: unsat")