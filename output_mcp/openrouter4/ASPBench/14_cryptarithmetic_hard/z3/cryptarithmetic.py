from z3 import *

solver = Solver()

# Declare integer variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# All digits are between 0 and 9
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# All letters have distinct digits
solver.add(Distinct(letters))

# Leading letters cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Arithmetic constraint: DONALD + GERALD = ROBERT
# DONALD = D*100000 + O*10000 + N*1000 + A*100 + L*10 + D
# GERALD = G*100000 + E*10000 + R*1000 + A*100 + L*10 + D
# ROBERT = R*100000 + O*10000 + B*1000 + E*100 + R*10 + T

donlad = D*100000 + O*10000 + N*1000 + A*100 + L*10 + D
gerald = G*100000 + E*10000 + R*1000 + A*100 + L*10 + D
robert = R*100000 + O*10000 + B*1000 + E*100 + R*10 + T

solver.add(donlad + gerald == robert)

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