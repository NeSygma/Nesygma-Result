from z3 import *
from itertools import product

def count_wins(rolls_a, rolls_b):
    """Count the number of times rolls_a > rolls_b in all possible pairs."""
    wins = 0
    for a, b in product(rolls_a, rolls_b):
        if a > b:
            wins += 1
    return wins

def unique_sorted_values(die_faces):
    """Return the sorted unique values of a die."""
    return sorted(list(set(die_faces)))

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

# Unique value sets constraint
unique_A = unique_sorted_values(A)
unique_B = unique_sorted_values(B)
unique_C = unique_sorted_values(C)
unique_D = unique_sorted_values(D)

# Ensure unique value sets are distinct
solver.add(unique_A != unique_B)
solver.add(unique_A != unique_C)
solver.add(unique_A != unique_D)
solver.add(unique_B != unique_C)
solver.add(unique_B != unique_D)
solver.add(unique_C != unique_D)

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

# Sort the faces for each die (non-decreasing order)
for die in [A, B, C, D]:
    for i in range(3):
        solver.add(die[i] <= die[i+1])

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")

    # Extract the dice faces from the model
    dice = {
        'A': [model.eval(face) for face in A],
        'B': [model.eval(face) for face in B],
        'C': [model.eval(face) for face in C],
        'D': [model.eval(face) for face in D]
    }

    # Print the dice configuration
    for die_name in ['A', 'B', 'C', 'D']:
        print(f"{die_name} = {sorted([model.eval(face).as_long() for face in dice[die_name]])}")

    # Calculate the common sum
    common_sum = model.eval(sum_A).as_long()
    print(f"common_sum = {common_sum}")

    # Calculate win counts
    wins_AB_count = count_wins([model.eval(face).as_long() for face in A],
                               [model.eval(face).as_long() for face in B])
    wins_BC_count = count_wins([model.eval(face).as_long() for face in B],
                               [model.eval(face).as_long() for face in C])
    wins_CD_count = count_wins([model.eval(face).as_long() for face in C],
                               [model.eval(face).as_long() for face in D])
    wins_DA_count = count_wins([model.eval(face).as_long() for face in D],
                               [model.eval(face).as_long() for face in A])

    print(f"win_counts = {{'A_beats_B': {wins_AB_count}, 'B_beats_C': {wins_BC_count}, 'C_beats_D': {wins_CD_count}, 'D_beats_A': {wins_DA_count}}}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")