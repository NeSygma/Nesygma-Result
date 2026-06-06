from z3 import *

# BENCHMARK_MODE: ON (problem guaranteed solvable)
BENCHMARK_MODE = True

# Create solver
solver = Solver()

# Number of dice and faces
num_dice = 4
faces_per_die = 4
values_range = list(range(1, 9))  # 1..8

# Variables for each die's faces (sorted non-decreasing)
A = [Int(f'A_{i}') for i in range(faces_per_die)]
B = [Int(f'B_{i}') for i in range(faces_per_die)]
C = [Int(f'C_{i}') for i in range(faces_per_die)]
D = [Int(f'D_{i}') for i in range(faces_per_die)]

# Sorting constraints
for i in range(faces_per_die - 1):
    solver.add(A[i] <= A[i+1])
    solver.add(B[i] <= B[i+1])
    solver.add(C[i] <= C[i+1])
    solver.add(D[i] <= D[i+1])

# Domain constraints: each face between 1 and 8 inclusive
for die in [A, B, C, D]:
    for face in die:
        solver.add(face >= 1)
        solver.add(face <= 8)

# Equal sum constraint
sum_A = Sum(A)
sum_B = Sum(B)
sum_C = Sum(C)
sum_D = Sum(D)
solver.add(sum_A == sum_B)
solver.add(sum_B == sum_C)
solver.add(sum_C == sum_D)

# Unique value sets: for each die, define presence of each value 1..8
def present(die):
    # returns a list of Bool for values 1..8
    return [Or([face == v for face in die]) for v in range(1, 9)]

present_A = present(A)
present_B = present(B)
present_C = present(C)
present_D = present(D)

# Ensure sets are distinct for each pair
def ensure_sets_different(p1, p2):
    # p1, p2 are lists of Bool of length 8 (index 0 corresponds to value 1)
    # Ensure there exists at least one value where presence differs
    return Or([p1[i] != p2[i] for i in range(8)])

solver.add(ensure_sets_different(present_A, present_B))
solver.add(ensure_sets_different(present_A, present_C))
solver.add(ensure_sets_different(present_A, present_D))
solver.add(ensure_sets_different(present_B, present_C))
solver.add(ensure_sets_different(present_B, present_D))
solver.add(ensure_sets_different(present_C, present_D))

# Helper to compute win count between two dice (X beats Y)
def win_count(X, Y):
    # X and Y are lists of 4 integers
    # Count number of pairs (i,j) where X[i] > Y[j]
    count = Sum([If(X[i] > Y[j], 1, 0) for i in range(4) for j in range(4)])
    return count

# Cyclic dominance constraints
win_AB = win_count(A, B)
win_BC = win_count(B, C)
win_CD = win_count(C, D)
win_DA = win_count(D, A)

solver.add(win_AB > 8)
solver.add(win_BC > 8)
solver.add(win_CD > 8)
solver.add(win_DA > 8)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract sorted faces for each die
    dice_faces = {}
    for die_name, die_vars in [('A', A), ('B', B), ('C', C), ('D', D)]:
        faces = [model.eval(face, model_completion=True).as_long() for face in die_vars]
        dice_faces[die_name] = faces
    
    # Compute common sum
    common_sum = model.eval(sum_A, model_completion=True).as_long()
    
    # Compute win counts
    win_counts = {
        'A_beats_B': model.eval(win_AB, model_completion=True).as_long(),
        'B_beats_C': model.eval(win_BC, model_completion=True).as_long(),
        'C_beats_D': model.eval(win_CD, model_completion=True).as_long(),
        'D_beats_A': model.eval(win_DA, model_completion=True).as_long()
    }
    
    # Print output in required format
    print("STATUS: sat")
    print("dice:", dice_faces)
    print("analysis:", {"common_sum": common_sum, "win_counts": win_counts})
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")