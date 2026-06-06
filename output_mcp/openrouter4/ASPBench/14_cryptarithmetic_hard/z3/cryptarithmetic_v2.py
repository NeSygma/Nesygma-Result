from z3 import *

solver = Solver()

# Declare integer variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# Carry variables (c0 is carry into column 0, always 0; c1..c6 are carries out of columns 0..5)
c0, c1, c2, c3, c4, c5, c6 = Ints('c0 c1 c2 c3 c4 c5 c6')

# All digits are between 0 and 9
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# Carries are 0 or 1 (except c0 which is always 0, and c6 which must be 0 for a 6-digit result)
for c in [c0, c1, c2, c3, c4, c5, c6]:
    solver.add(c >= 0, c <= 1)

solver.add(c0 == 0)
solver.add(c6 == 0)

# All letters have distinct digits
solver.add(Distinct(letters))

# Leading letters cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Columnar addition with carries (right to left):
# Column 0 (units): D + D = 2*D = T + 10*c1
solver.add(2 * D == T + 10 * c1)

# Column 1 (tens): L + L + c1 = 2*L + c1 = R + 10*c2
solver.add(2 * L + c1 == R + 10 * c2)

# Column 2 (hundreds): A + A + c2 = 2*A + c2 = E + 10*c3
solver.add(2 * A + c2 == E + 10 * c3)

# Column 3 (thousands): N + R + c3 = B + 10*c4
solver.add(N + R + c3 == B + 10 * c4)

# Column 4 (ten-thousands): O + E + c4 = O + 10*c5
# This simplifies to: E + c4 = 10*c5
solver.add(E + c4 == 10 * c5)

# Column 5 (hundred-thousands): D + G + c5 = R + 10*c6
# Since c6 == 0: D + G + c5 = R
solver.add(D + G + c5 == R)

# Check and print result
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    print(f"D = {model[D]}")
    print(f"O = {model[O]}")
    print(f"N = {model[N]}")
    print(f"A = {model[A]}")
    print(f"L = {model[L]}")
    print(f"G = {model[G]}")
    print(f"E = {model[E]}")
    print(f"R = {model[R]}")
    print(f"B = {model[B]}")
    print(f"T = {model[T]}")
    
    # Print the equation
    d_val = model[D].as_long()
    o_val = model[O].as_long()
    n_val = model[N].as_long()
    a_val = model[A].as_long()
    l_val = model[L].as_long()
    g_val = model[G].as_long()
    e_val = model[E].as_long()
    r_val = model[R].as_long()
    b_val = model[B].as_long()
    t_val = model[T].as_long()
    
    donald_num = d_val*100000 + o_val*10000 + n_val*1000 + a_val*100 + l_val*10 + d_val
    gerald_num = g_val*100000 + e_val*10000 + r_val*1000 + a_val*100 + l_val*10 + d_val
    robert_num = r_val*100000 + o_val*10000 + b_val*1000 + e_val*100 + r_val*10 + t_val
    
    print(f"  {donald_num:6d}")
    print(f"+ {gerald_num:6d}")
    print(f"  -------")
    print(f"= {robert_num:6d}")
    print(f"Valid: {donald_num + gerald_num == robert_num}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")