from z3 import *

solver = Solver()
# Declare dice faces
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]
# Domain constraints
for die in (A+B+C):
    solver.add(die >= 0, die <= 6)
# Helper to compute win count
def win_count(X, Y):
    return Sum([If(x > y, 1, 0) for x in X for y in Y])

win_AB = win_count(A, B)
win_BC = win_count(B, C)
win_CA = win_count(C, A)
# Winning > 18 (out of 36)
solver.add(win_AB > 18)
solver.add(win_BC > 18)
solver.add(win_CA > 18)

result = solver.check()
if result == sat:
    m = solver.model()
    # extract faces
    A_vals = [m.eval(v).as_long() for v in A]
    B_vals = [m.eval(v).as_long() for v in B]
    C_vals = [m.eval(v).as_long() for v in C]
    # compute win counts
    def eval_win(X_vals, Y_vals):
        cnt = 0
        for x in X_vals:
            for y in Y_vals:
                if x > y:
                    cnt += 1
        return cnt
    cnt_AB = eval_win(A_vals, B_vals)
    cnt_BC = eval_win(B_vals, C_vals)
    cnt_CA = eval_win(C_vals, A_vals)
    print("STATUS: sat")
    print("A =", A_vals)
    print("B =", B_vals)
    print("C =", C_vals)
    print(f"A beats B: {cnt_AB}/36 = {cnt_AB/36:.3f}")
    print(f"B beats C: {cnt_BC}/36 = {cnt_BC/36:.3f}")
    print(f"C beats A: {cnt_CA}/36 = {cnt_CA/36:.3f}")
else:
    print("STATUS: unsat")