from z3 import *

solver = Solver()

# Define face values for each die (sorted non-decreasing)
A = [Int(f'A_{i}') for i in range(4)]
B = [Int(f'B_{i}') for i in range(4)]
C = [Int(f'C_{i}') for i in range(4)]
D = [Int(f'D_{i}') for i in range(4)]

all_dice_list = [A, B, C, D]
all_dice_named = [('A', A), ('B', B), ('C', C), ('D', D)]

# Domain constraints: values between 1 and 8
for die in all_dice_list:
    for face in die:
        solver.add(face >= 1, face <= 8)

# Sorted order constraints (non-decreasing)
for die in all_dice_list:
    for i in range(3):
        solver.add(die[i] <= die[i + 1])

# Equal sum constraint
common_sum = Int('common_sum')
for die in all_dice_list:
    solver.add(Sum(die) == common_sum)

# Win counting for nontransitive cycle
# A beats B: wins > 8 out of 16 roll combinations
win_AB = Sum([If(A[i] > B[j], 1, 0) for i in range(4) for j in range(4)])
solver.add(win_AB > 8)

win_BC = Sum([If(B[i] > C[j], 1, 0) for i in range(4) for j in range(4)])
solver.add(win_BC > 8)

win_CD = Sum([If(C[i] > D[j], 1, 0) for i in range(4) for j in range(4)])
solver.add(win_CD > 8)

win_DA = Sum([If(D[i] > A[j], 1, 0) for i in range(4) for j in range(4)])
solver.add(win_DA > 8)

# Unique value sets constraint
# For each die, define which values (1-8) appear on it
def has_value(die, v):
    return Or([die[i] == v for i in range(4)])

# For each pair of dice, their sets of distinct values must differ
for i in range(4):
    for j in range(i + 1, 4):
        name_i, die_i = all_dice_named[i]
        name_j, die_j = all_dice_named[j]
        # There must exist some value v where presence differs
        solver.add(Or([has_value(die_i, v) != has_value(die_j, v) for v in range(1, 9)]))

# Mild symmetry breaking: fix A's smallest face to be <= others' smallest
solver.add(A[0] <= B[0])
solver.add(A[0] <= C[0])
solver.add(A[0] <= D[0])

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")

    A_vals = [int(str(m[A[i]])) for i in range(4)]
    B_vals = [int(str(m[B[i]])) for i in range(4)]
    C_vals = [int(str(m[C[i]])) for i in range(4)]
    D_vals = [int(str(m[D[i]])) for i in range(4)]

    print(f"dice_A = {A_vals}")
    print(f"dice_B = {B_vals}")
    print(f"dice_C = {C_vals}")
    print(f"dice_D = {D_vals}")
    print(f"common_sum = {int(str(m[common_sum]))}")

    # Verify win counts
    def count_wins(die1_vals, die2_vals):
        return sum(1 for v1 in die1_vals for v2 in die2_vals if v1 > v2)

    ab = count_wins(A_vals, B_vals)
    bc = count_wins(B_vals, C_vals)
    cd = count_wins(C_vals, D_vals)
    da = count_wins(D_vals, A_vals)

    print(f"A_beats_B = {ab}")
    print(f"B_beats_C = {bc}")
    print(f"C_beats_D = {cd}")
    print(f"D_beats_A = {da}")

    # Verify unique value sets
    def get_value_set(vals):
        return sorted(set(vals))

    sets = {
        'A': get_value_set(A_vals),
        'B': get_value_set(B_vals),
        'C': get_value_set(C_vals),
        'D': get_value_set(D_vals)
    }
    print(f"value_sets = {sets}")

    # Verify all sets are distinct
    set_list = list(sets.values())
    all_distinct = len(set_list) == len(set(tuple(s) for s in set_list))
    print(f"all_value_sets_distinct = {all_distinct}")

    # Verify equal sums
    sums = {
        'A': sum(A_vals),
        'B': sum(B_vals),
        'C': sum(C_vals),
        'D': sum(D_vals)
    }
    print(f"sums = {sums}")
    print(f"all_sums_equal = {len(set(sums.values())) == 1}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")