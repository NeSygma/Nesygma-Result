from z3 import *

# Create solver
solver = Solver()

# Declare face values for each die (6 faces each)
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Constraint 1: Each face value must be in {0, 1, 2, 3, 4, 5, 6}
for i in range(6):
    solver.add(And(A[i] >= 0, A[i] <= 6))
    solver.add(And(B[i] >= 0, B[i] <= 6))
    solver.add(And(C[i] >= 0, C[i] <= 6))

# Function to count wins where die X beats die Y
def count_wins(X, Y):
    """Count number of pairs (x, y) where x > y"""
    wins = 0
    for i in range(6):
        for j in range(6):
            # Use If to count 1 when X[i] > Y[j], 0 otherwise
            wins += If(X[i] > Y[j], 1, 0)
    return wins

# Count wins for each pair
wins_A_over_B = count_wins(A, B)
wins_B_over_C = count_wins(B, C)
wins_C_over_A = count_wins(C, A)

# Constraint 2: A beats B (more than 18 wins out of 36)
solver.add(wins_A_over_B > 18)

# Constraint 3: B beats C (more than 18 wins out of 36)
solver.add(wins_B_over_C > 18)

# Constraint 4: C beats A (more than 18 wins out of 36)
solver.add(wins_C_over_A > 18)

# Check for solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract dice values
    dice = {
        "A": [model[A[i]].as_long() for i in range(6)],
        "B": [model[B[i]].as_long() for i in range(6)],
        "C": [model[C[i]].as_long() for i in range(6)]
    }
    
    # Calculate actual win probabilities
    def calc_prob(X, Y):
        wins = 0
        for i in range(6):
            for j in range(6):
                if X[i] > Y[j]:
                    wins += 1
        return wins / 36.0
    
    prob_AB = calc_prob(dice["A"], dice["B"])
    prob_BC = calc_prob(dice["B"], dice["C"])
    prob_CA = calc_prob(dice["C"], dice["A"])
    
    win_probabilities = {
        "A_beats_B": prob_AB,
        "B_beats_C": prob_BC,
        "C_beats_A": prob_CA
    }
    
    print("dice:", dice)
    print("win_probabilities:", win_probabilities)
    
    # Verify all probabilities > 0.5
    assert prob_AB > 0.5, f"A beats B probability {prob_AB} <= 0.5"
    assert prob_BC > 0.5, f"B beats C probability {prob_BC} <= 0.5"
    assert prob_CA > 0.5, f"C beats A probability {prob_CA} <= 0.5"
    
    print("\nVerification:")
    print(f"A beats B: {prob_AB:.3f} (> 0.5: {prob_AB > 0.5})")
    print(f"B beats C: {prob_BC:.3f} (> 0.5: {prob_BC > 0.5})")
    print(f"C beats A: {prob_CA:.3f} (> 0.5: {prob_CA > 0.5})")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")