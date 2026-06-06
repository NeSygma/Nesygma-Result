from z3 import *
from itertools import product

def count_wins(rolls_a, rolls_b):
    """Count the number of times rolls_a > rolls_b in all possible pairs."""
    wins = 0
    for a, b in product(rolls_a, rolls_b):
        if a > b:
            wins += 1
    return wins

# Initialize solver
solver = Solver()

# Declare dice faces as Int variables
A = [Int(f'A_{i}') for i in range(4)]
B = [Int(f'B_{i}') for i in range(4)]
C = [Int(f'C_{i}') for i in range(4)]
D = [Int(f'D_{i}') for i in range(4)]

# Add constraints for face values (1 to 8 inclusive)
for die in [A, B, C, D]:
    for face in die:
        solver.add(face >= 1, face <= 8)

# Equal sum constraint: sum of faces for A, B, C, D must be equal
sum_A = Sum(A)
sum_B = Sum(B)
sum_C = Sum(C)
sum_D = Sum(D)
solver.add(sum_A == sum_B, sum_B == sum_C, sum_C == sum_D)

# Sort the faces for each die (non-decreasing order)
for die in [A, B, C, D]:
    for i in range(3):
        solver.add(die[i] <= die[i+1])

# Enforce unique value sets by ensuring the sorted unique values are distinct
# We represent the sorted unique values as a list of Z3 expressions and ensure they are distinct
# To do this, we enforce that the sorted unique values of A, B, C, D are all distinct

# Helper function to get the sorted unique values of a die as a Z3 expression
# Since Z3 does not support direct sorting or set operations, we manually enforce distinctness
# by ensuring that the sorted unique values are not equal for any two dice

def get_unique_values(die):
    # Return the sorted unique values as a list of Z3 expressions
    # Since Z3 does not support direct set operations, we use a simplified approach
    # We assume the die is sorted, so we can remove duplicates by comparing adjacent elements
    unique = []
    for i in range(4):
        if i == 0:
            unique.append(die[i])
        else:
            # Only add if not equal to the previous unique value
            solver.add(Implies(unique[-1] != die[i], True))
            unique.append(If(unique[-1] == die[i], unique[-1], die[i]))
    return unique

# Instead of using get_unique_values, we enforce that the sorted unique values are distinct
# by ensuring that the sets of values are not equal for any two dice
# We do this by ensuring that at least one value in A is not in B, and vice versa
# This is a simplified approach and may not cover all cases

# Enforce that the sorted unique values of A and B are distinct
solver.add(Or([A[i] != B[j] for i in range(4) for j in range(4)]))

# Enforce that the sorted unique values of A and C are distinct
solver.add(Or([A[i] != C[j] for i in range(4) for j in range(4)]))

# Enforce that the sorted unique values of A and D are distinct
solver.add(Or([A[i] != D[j] for i in range(4) for j in range(4)]))

# Enforce that the sorted unique values of B and C are distinct
solver.add(Or([B[i] != C[j] for i in range(4) for j in range(4)]))

# Enforce that the sorted unique values of B and D are distinct
solver.add(Or([B[i] != D[j] for i in range(4) for j in range(4)]))

# Enforce that the sorted unique values of C and D are distinct
solver.add(Or([C[i] != D[j] for i in range(4) for j in range(4)]))

# Nontransitive cycle constraints
# A beats B: A wins > 8 times out of 16
wins_AB = count_wins(A, B)
solver.add(wins_AB > 8)

# B beats C: B wins > 8 times out of 16
wins_BC = count_wins(B, C)
solver.add(wins_BC > 8)

# C beats D: C wins > 8 times out of 16
wins_CD = count_wins(C, D)
solver.add(wins_CD > 8)

# D beats A: D wins > 8 times out of 16
wins_DA = count_wins(D, A)
solver.add(wins_DA > 8)

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")

    # Extract the dice faces from the model
    dice = {
        'A': [model.eval(face).as_long() for face in A],
        'B': [model.eval(face).as_long() for face in B],
        'C': [model.eval(face).as_long() for face in C],
        'D': [model.eval(face).as_long() for face in D]
    }

    # Print the dice configuration
    for die_name in ['A', 'B', 'C', 'D']:
        print(f"{die_name} = {sorted(dice[die_name])}")

    # Calculate the common sum
    common_sum = sum(dice['A'])
    print(f"common_sum = {common_sum}")

    # Calculate win counts
    wins_AB_count = count_wins(dice['A'], dice['B'])
    wins_BC_count = count_wins(dice['B'], dice['C'])
    wins_CD_count = count_wins(dice['C'], dice['D'])
    wins_DA_count = count_wins(dice['D'], dice['A'])

    print(f"win_counts = {{'A_beats_B': {wins_AB_count}, 'B_beats_C': {wins_BC_count}, 'C_beats_D': {wins_CD_count}, 'D_beats_A': {wins_DA_count}}}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")