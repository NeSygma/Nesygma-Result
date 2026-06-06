from z3 import *

solver = Solver()

# Dice faces
A = [Int(f"A_{i}") for i in range(4)]
B = [Int(f"B_{i}") for i in range(4)]
C = [Int(f"C_{i}") for i in range(4)]
D = [Int(f"D_{i}") for i in range(4)]

all_dice = [A, B, C, D]
die_names = ["A", "B", "C", "D"]

# Domain constraints: each face value between 1 and 8
for die in all_dice:
    for face in die:
        solver.add(face >= 1, face <= 8)

# Sorting: non-decreasing order
for die in all_dice:
    for i in range(3):
        solver.add(die[i] <= die[i+1])

# Equal sum constraint
sum_A = Sum(A)
sum_B = Sum(B)
sum_C = Sum(C)
sum_D = Sum(D)
solver.add(sum_A == sum_B)
solver.add(sum_B == sum_C)
solver.add(sum_C == sum_D)

# Win function
def win_count(X, Y):
    return Sum([If(X[i] > Y[j], 1, 0) for i in range(4) for j in range(4)])

# Cyclic dominance constraints
solver.add(win_count(A, B) > 8)
solver.add(win_count(B, C) > 8)
solver.add(win_count(C, D) > 8)
solver.add(win_count(D, A) > 8)

# Unique value set constraints
# For each die, compute has_value[v] for v in 1..8
def value_set(die):
    return [Or([die[i] == v for i in range(4)]) for v in range(1, 9)]

sets = [value_set(A), value_set(B), value_set(C), value_set(D)]

# For each pair of dice, ensure their value sets are different
for i in range(4):
    for j in range(i+1, 4):
        # sets are equal if has_X[v] == has_Y[v] for all v
        equal_conditions = [sets[i][v-1] == sets[j][v-1] for v in range(1, 9)]
        solver.add(Not(And(equal_conditions)))

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract and print sorted values for each die
    dice_vals = {}
    for name, die in zip(die_names, all_dice):
        vals = sorted([model.eval(face).as_long() for face in die])
        dice_vals[name] = vals
        print(f"{name}: {vals}")
    
    common_sum = sum(dice_vals['A'])
    print(f"common_sum = {common_sum}")
    
    # Compute win counts
    def compute_wins(X_vals, Y_vals):
        count = 0
        for x in X_vals:
            for y in Y_vals:
                if x > y:
                    count += 1
        return count
    
    print(f"A_beats_B = {compute_wins(dice_vals['A'], dice_vals['B'])}")
    print(f"B_beats_C = {compute_wins(dice_vals['B'], dice_vals['C'])}")
    print(f"C_beats_D = {compute_wins(dice_vals['C'], dice_vals['D'])}")
    print(f"D_beats_A = {compute_wins(dice_vals['D'], dice_vals['A'])}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")