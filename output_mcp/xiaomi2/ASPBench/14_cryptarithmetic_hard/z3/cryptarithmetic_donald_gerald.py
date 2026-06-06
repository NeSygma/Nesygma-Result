from z3 import *

solver = Solver()

# Declare symbolic variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# Constraint 1: Each letter is a digit 0-9
for l in letters:
    solver.add(l >= 0, l <= 9)

# Constraint 2: All letters have distinct digits (all 10 digits used exactly once)
solver.add(Distinct(letters))

# Constraint 3: Leading digits cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Constraint 4: Arithmetic correctness
# DONALD = D*100000 + O*10000 + N*1000 + A*100 + L*10 + D
# GERALD = G*100000 + E*10000 + R*1000 + A*100 + L*10 + D
# ROBERT = R*100000 + O*10000 + B*1000 + E*100 + R*10 + T

donald = D*100000 + O*10000 + N*1000 + A*100 + L*10 + D
gerald = G*100000 + E*10000 + R*1000 + A*100 + L*10 + D
robert = R*100000 + O*10000 + B*1000 + E*100 + R*10 + T

solver.add(donald + gerald == robert)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Extract digit assignments
    assignment = {}
    for var in letters:
        assignment[str(var)] = m.evaluate(var).as_long()
    
    print("Assignment:")
    for letter, digit in sorted(assignment.items()):
        print(f"  {letter} = {digit}")
    
    # Compute the actual numbers
    d_val = assignment['D']
    o_val = assignment['O']
    n_val = assignment['N']
    a_val = assignment['A']
    l_val = assignment['L']
    g_val = assignment['G']
    e_val = assignment['E']
    r_val = assignment['R']
    b_val = assignment['B']
    t_val = assignment['T']
    
    donald_num = d_val*100000 + o_val*10000 + n_val*1000 + a_val*100 + l_val*10 + d_val
    gerald_num = g_val*100000 + e_val*10000 + r_val*1000 + a_val*100 + l_val*10 + d_val
    robert_num = r_val*100000 + o_val*10000 + b_val*1000 + e_val*100 + r_val*10 + t_val
    
    print(f"\nEquation: {donald_num} + {gerald_num} = {robert_num}")
    print(f"Valid: {donald_num + gerald_num == robert_num}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")