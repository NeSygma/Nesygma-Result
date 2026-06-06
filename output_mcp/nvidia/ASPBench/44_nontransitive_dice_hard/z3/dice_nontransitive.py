from z3 import *

# Declare variables for each die's faces
a0, a1, a2, a3 = Ints('a0 a1 a2 a3')
b0, b1, b2, b3 = Ints('b0 b1 b2 b3')
c0, c1, c2, c3 = Ints('c0 c1 c2 c3')
d0, d1, d2, d3 = Ints('d0 d1 d2 d3')

solver = Solver()

# Domain constraints: values between 1 and 8 inclusive
for v in [a0,a1,a2,a3,b0,b1,b2,b3,c0,c1,c2,c3,d0,d1,d2,d3]:
    solver.add(v >= 1, v <= 8)

# Sorted (non-decreasing) order for each die
solver.add(a0 <= a1, a1 <= a2, a2 <= a3)
solver.add(b0 <= b1, b1 <= b2, b2 <= b3)
solver.add(c0 <= c1, c1 <= c2, c2 <= c3)
solver.add(d0 <= d1, d1 <= d2, d2 <= d3)

# Equal sum constraint across all dice
sum_a = a0 + a1 + a2 + a3
sum_b = b0 + b1 + b2 + b3
sum_c = c0 + c1 + c2 + c3
sum_d = d0 + d1 + d2 + d3
solver.add(sum_a == sum_b)
solver.add(sum_b == sum_c)
solver.add(sum_c == sum_d)
common_sum = sum_a  # just a placeholder, not a separate variable

# Unique value set constraints (ensure dice tuples are not identical)
solver.add(Or(a0 != b0, a1 != b1, a2 != b2, a3 != b3))
solver.add(Or(a0 != c0, a1 != c1, a2 != c2, a3 != c3))
solver.add(Or(a0 != d0, a1 != d1, a2 != d2, a3 != d3))
solver.add(Or(b0 != c0, b1 != c1, b2 != c2, b3 != c3))
solver.add(Or(b0 != d0, b1 != d1, b2 != d2, b3 != d3))
solver.add(Or(c0 != d0, c1 != d1, c2 != d2, c3 != d3))

# Helper to encode "X beats Y" with >8 wins out of 16
def add_win_gt8(x0,x1,x2,x3, y0,y1,y2,y3):
    # Compute sum of wins: 1 if xi > yj else 0
    wins = (If(x0 > y0, 1, 0) + If(x0 > y1, 1, 0) + If(x0 > y2, 1, 0) + If(x0 > y3, 1, 0) +
           (If(x1 > y0, 1, 0) + If(x1 > y1, 1, 0) + If(x1 > y2, 1, 0) + If(x1 > y3, 1, 0) +
           (If(x2 > y0, 1, 0) + If(x2 > y1, 1, 0) + If(x2 > y2, 1, 0) + If(x2 > y3, 1, 0) +
           (If(x3 > y0, 1, 0) + If(x3 > y1, 1, 0) + If(x3 > y2, 1, 0) + If(x3 > y3, 1, 0))
    solver.add(wins >= 9)  # >8 wins means at least 9

# A beats B, B beats C, C beats D, D beats A
add_win_gt8(a0,a1,a2,a3, b0,b1,b2,b3)
add_win_gt8(b0,b1,b2,b3, c0,c1,c2,c3)
add_win_gt8(c0,c1,c2,c3, d0,d1,d2,d3)
add_win_gt8(d0,d1,d2,d3, a0,a1,a2,a3)

# Check solution
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Helper to extract integer value from model
    def eval_int(var):
        return m.eval(var, model_completion=True).as_long()
    a_vals = [eval_int(a0), eval_int(a1), eval_int(a2), eval_int(a3)]
    b_vals = [eval_int(b0), eval_int(b1), eval_int(b2), eval_int(b3)]
    c_vals = [eval_int(c0), eval_int(c1), eval_int(c2), eval_int(c3)]
    d_vals = [eval_int(d0), eval_int(d1), eval_int(d2), eval_int(d3)]
    print("A:", a_vals)
    print("B:", b_vals)
    print("C:", c_vals)
    print("D:", d_vals)
    # Compute win counts for reporting
    def win_count(xs, ys):
        cnt = 0
        for i in range(4):
            for j in range(4):
                if xs[i] > ys[j]:
                    cnt += 1
        return cnt
    win_AB = win_count(a_vals, b_vals)
    win_BC = win_count(b_vals, c_vals)
    win_CD = win_count(c_vals, d_vals)
    win_DA = win_count(d_vals, a_vals)
    print("common_sum:", sum(a_vals))
    print("win_counts: A_beats_B=", win_AB, "B_beats_C=", win_BC, "C_beats_D=", win_CD, "D_beats_A=", win_DA)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")