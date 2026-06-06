from z3 import *

solver = Solver()

# Declare dice face variables
A = [Int(f'A_{i}') for i in range(4)]
B = [Int(f'B_{i}') for i in range(4)]
C = [Int(f'C_{i}') for i in range(4)]
D = [Int(f'D_{i}') for i in range(4)]
all_vars = A + B + C + D

# Domain constraints and sorting
for die in [A, B, C, D]:
    for face in die:
        solver.add(face >= 1, face <= 8)
    # non-decreasing order
    for i in range(3):
        solver.add(die[i] <= die[i+1])

# Equal sum constraint
sumA = Sum(A)
sumB = Sum(B)
sumC = Sum(C)
sumD = Sum(D)
common_sum = Int('common_sum')
solver.add(common_sum == sumA, sumB == common_sum, sumC == common_sum, sumD == common_sum)

# Presence booleans for each value 1..8
presence = {}
for die_name, die in [('A', A), ('B', B), ('C', C), ('D', D)]:
    for v in range(1, 9):
        presence[(die_name, v)] = Bool(f'present_{die_name}_{v}')
        solver.add(presence[(die_name, v)] == Or([face == v for face in die]))

# Unique value sets: for each pair, ensure sets differ
pairs = [('A','B'),('A','C'),('A','D'),('B','C'),('B','D'),('C','D')]
for (d1,d2) in pairs:
    diffs = []
    for v in range(1,9):
        diffs.append(presence[(d1,v)] != presence[(d2,v)])
    solver.add(Or(diffs))

# Function to compute win count between two dice
def win_count(die1, die2):
    return Sum([If(die1[i] > die2[j], 1, 0) for i in range(4) for j in range(4)])

win_AB = win_count(A, B)
win_BC = win_count(B, C)
win_CD = win_count(C, D)
win_DA = win_count(D, A)

# Must be >8 (i.e., >=9)
solver.add(win_AB >= 9)
solver.add(win_BC >= 9)
solver.add(win_CD >= 9)
solver.add(win_DA >= 9)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    # Extract dice values
    A_vals = [m.eval(v).as_long() for v in A]
    B_vals = [m.eval(v).as_long() for v in B]
    C_vals = [m.eval(v).as_long() for v in C]
    D_vals = [m.eval(v).as_long() for v in D]
    common = m.eval(common_sum).as_long()
    # Compute win counts from model (should match constraints)
    def compute_wc(d1,d2):
        cnt = 0
        for x in d1:
            for y in d2:
                if x > y:
                    cnt += 1
        return cnt
    wc_AB = compute_wc(A_vals, B_vals)
    wc_BC = compute_wc(B_vals, C_vals)
    wc_CD = compute_wc(C_vals, D_vals)
    wc_DA = compute_wc(D_vals, A_vals)
    print("STATUS: sat")
    print(f"A = {A_vals}")
    print(f"B = {B_vals}")
    print(f"C = {C_vals}")
    print(f"D = {D_vals}")
    print(f"common_sum = {common}")
    print(f"A_beats_B = {wc_AB}")
    print(f"B_beats_C = {wc_BC}")
    print(f"C_beats_D = {wc_CD}")
    print(f"D_beats_A = {wc_DA}")
else:
    print("STATUS: unsat")