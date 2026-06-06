from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare dice faces as integer variables
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

solver = Solver()

# Each face value must be between 0 and 6 inclusive
for i in range(6):
    solver.add(0 <= A[i], A[i] <= 6)
    solver.add(0 <= B[i], B[i] <= 6)
    solver.add(0 <= C[i], C[i] <= 6)

# Helper to count wins: number of pairs where X > Y
def count_wins(X, Y):
    # X and Y are lists of 6 integer variables
    wins = []
    for i in range(6):
        for j in range(6):
            wins.append(If(X[i] > Y[j], 1, 0))
    return Sum(wins)

# Compute win counts
wins_AB = count_wins(A, B)
wins_BC = count_wins(B, C)
wins_CA = count_wins(C, A)

# Winning condition: > 18 wins out of 36
solver.add(wins_AB > 18)
solver.add(wins_BC > 18)
solver.add(wins_CA > 18)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract dice values
    dice = {}
    dice['A'] = [model[A[i]].as_long() for i in range(6)]
    dice['B'] = [model[B[i]].as_long() for i in range(6)]
    dice['C'] = [model[C[i]].as_long() for i in range(6)]
    
    # Compute win probabilities
    def prob_win(X, Y):
        wins = 0
        for x in X:
            for y in Y:
                if x > y:
                    wins += 1
        return wins / 36.0
    
    prob_AB = prob_win(dice['A'], dice['B'])
    prob_BC = prob_win(dice['B'], dice['C'])
    prob_CA = prob_win(dice['C'], dice['A'])
    
    win_probabilities = {
        'A_beats_B': prob_AB,
        'B_beats_C': prob_BC,
        'C_beats_A': prob_CA
    }
    
    print("STATUS: sat")
    print("dice:", dice)
    print("win_probabilities:", win_probabilities)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")