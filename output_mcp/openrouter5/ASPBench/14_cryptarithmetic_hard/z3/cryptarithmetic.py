from z3 import *

solver = Solver()

# Declare integer variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# Constraint 1: Each letter is a digit from 0 to 9
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# Constraint 1: All letters have distinct values
solver.add(Distinct(letters))

# Constraint 2: Leading letters cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Constraint 3: Arithmetic correctness using columnar addition with carries
# We'll model the addition column by column from right to left
# Columns (right to left): units, tens, hundreds, thousands, ten-thousands, hundred-thousands

# Let c1, c2, c3, c4, c5 be the carry digits (0 or 1) from each column
c1, c2, c3, c4, c5 = Ints('c1 c2 c3 c4 c5')
for c in [c1, c2, c3, c4, c5]:
    solver.add(c >= 0, c <= 1)

# Column 1 (units): D + D = T + 10*c1
solver.add(D + D == T + 10 * c1)

# Column 2 (tens): L + L + c1 = R + 10*c2
solver.add(L + L + c1 == R + 10 * c2)

# Column 3 (hundreds): A + A + c2 = E + 10*c3
solver.add(A + A + c2 == E + 10 * c3)

# Column 4 (thousands): N + R + c3 = B + 10*c4
solver.add(N + R + c3 == B + 10 * c4)

# Column 5 (ten-thousands): O + E + c4 = O + 10*c5
solver.add(O + E + c4 == O + 10 * c5)

# Column 6 (hundred-thousands): D + G + c5 = R + 10*c6 (but c6 must be 0 since result is 6 digits)
# Actually ROBERT is 6 digits, so the final carry c6 must be 0
c6 = Int('c6')
solver.add(c6 >= 0, c6 <= 1)
solver.add(D + G + c5 == R + 10 * c6)
solver.add(c6 == 0)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    print(f"D = {m[D]}")
    print(f"O = {m[O]}")
    print(f"N = {m[N]}")
    print(f"A = {m[A]}")
    print(f"L = {m[L]}")
    print(f"G = {m[G]}")
    print(f"E = {m[E]}")
    print(f"R = {m[R]}")
    print(f"B = {m[B]}")
    print(f"T = {m[T]}")
    # Verify the equation
    d_val = m[D].as_long()
    o_val = m[O].as_long()
    n_val = m[N].as_long()
    a_val = m[A].as_long()
    l_val = m[L].as_long()
    g_val = m[G].as_long()
    e_val = m[E].as_long()
    r_val = m[R].as_long()
    b_val = m[B].as_long()
    t_val = m[T].as_long()
    donald_num = 100000*d_val + 10000*o_val + 1000*n_val + 100*a_val + 10*l_val + d_val
    gerald_num = 100000*g_val + 10000*e_val + 1000*r_val + 100*a_val + 10*l_val + d_val
    robert_num = 100000*r_val + 10000*o_val + 1000*b_val + 100*e_val + 10*r_val + t_val
    print(f"{donald_num} + {gerald_num} = {robert_num}")
    print(f"Valid: {donald_num + gerald_num == robert_num}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")