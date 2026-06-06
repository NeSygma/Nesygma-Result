from z3 import *

# Create dice variables
A = [Int(f'A_{i}') for i in range(4)]
B = [Int(f'B_{i}') for i in range(4)]
C = [Int(f'C_{i}') for i in range(4)]
D = [Int(f'D_{i}') for i in range(4)]

# Common sum variable
common_sum = Int('common_sum')

solver = Solver()

# Constraints for each die
for die in [A, B, C, D]:
    for val in die:
        solver.add(val >= 1, val <= 8)
    # Sorted constraint
    for i in range(3):
        solver.add(die[i] <= die[i+1])

# Equal sum constraint
solver.add(Sum(A) == common_sum)
solver.add(Sum(B) == common_sum)
solver.add(Sum(C) == common_sum)
solver.add(Sum(D) == common_sum)

# Unique value sets constraint
# Since dice are sorted, we can just check that the lists are not equal
solver.add(A != B)
solver.add(A != C)
solver.add(A != D)
solver.add(B != C)
solver.add(B != D)
solver.add(C != D)

# Count wins for A vs B
wins_AB = [If(A[i] > B[j], 1, 0) for i in range(4) for j in range(4)]
count_AB = Int('count_AB')
solver.add(count_AB == Sum(wins_AB))
solver.add(count_AB > 8)

# Count wins for B vs C
wins_BC = [If(B[i] > C[j], 1, 0) for i in range(4) for j in range(4)]
count_BC = Int('count_BC')
solver.add(count_BC == Sum(wins_BC))
solver.add(count_BC > 8)

# Count wins for C vs D
wins_CD = [If(C[i] > D[j], 1, 0) for i in range(4) for j in range(4)]
count_CD = Int('count_CD')
solver.add(count_CD == Sum(wins_CD))
solver.add(count_CD > 8)

# Count wins for D vs A
wins_DA = [If(D[i] > A[j], 1, 0) for i in range(4) for j in range(4)]
count_DA = Int('count_DA')
solver.add(count_DA == Sum(wins_DA))
solver.add(count_DA > 8)

# Check and print result
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract dice values
    dice = {
        'A': [model.eval(v) for v in A],
        'B': [model.eval(v) for v in B],
        'C': [model.eval(v) for v in C],
        'D': [model.eval(v) for v in D]
    }
    # Extract common sum
    common_sum_val = model.eval(common_sum)
    # Extract win counts
    win_counts = {
        'A_beats_B': model.eval(count_AB),
        'B_beats_C': model.eval(count_BC),
        'C_beats_D': model.eval(count_CD),
        'D_beats_A': model.eval(count_DA)
    }
    # Print results
    print("dice:", dice)
    print("analysis:", {
        'common_sum': common_sum_val,
        'win_counts': win_counts
    })
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")