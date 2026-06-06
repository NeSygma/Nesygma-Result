from z3 import *

solver = Solver()

# Variables
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Each section has exactly 2 photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Each photographer has between 1 and 3 photos total
solver.add(1 <= L_F + M_F + S_F)
solver.add(L_F + M_F + S_F <= 3)
solver.add(1 <= L_G + M_G + S_G)
solver.add(L_G + M_G + S_G <= 3)
solver.add(1 <= L_H + M_H + S_H)
solver.add(L_H + M_H + S_H <= 3)

# At least one Lifestyle photo by a photographer who also has at least one Metro photo
solver.add(Or(
    And(L_F > 0, M_F > 0),
    And(L_G > 0, M_G > 0),
    And(L_H > 0, M_H > 0)
))

# Number of Hue's photos in Lifestyle equals number of Fuentes photos in Sports
solver.add(L_H == S_F)

# No Gagnon photos in Sports
solver.add(S_G == 0)

# Additional constraint from question: both Lifestyle photos are by Hue
solver.add(L_H == 2)
solver.add(L_F == 0)
solver.add(L_G == 0)

# Check if this is satisfiable
result = solver.check()
if result == sat:
    print("Base constraints are satisfiable")
    m = solver.model()
    print(f"L_F={m[L_F]}, L_G={m[L_G]}, L_H={m[L_H]}")
    print(f"M_F={m[M_F]}, M_G={m[M_G]}, M_H={m[M_H]}")
    print(f"S_F={m[S_F]}, S_G={m[S_G]}, S_H={m[S_H]}")
    
    # Calculate totals
    total_F = m[L_F].as_long() + m[M_F].as_long() + m[S_F].as_long()
    total_G = m[L_G].as_long() + m[M_G].as_long() + m[S_G].as_long()
    total_H = m[L_H].as_long() + m[M_H].as_long() + m[S_H].as_long()
    
    print(f"Total Fuentes: {total_F}")
    print(f"Total Gagnon: {total_G}")
    print(f"Total Hue: {total_H}")
    
    # Now evaluate each answer choice
    # A: Exactly one is by Fuentes
    # B: Exactly three are by Fuentes
    # C: Exactly one is by Gagnon
    # D: Exactly two are by Gagnon
    # E: Exactly two are by Hue
    
    found_options = []
    
    # Test A: Exactly one Fuentes
    solver.push()
    solver.add(total_F == 1)
    if solver.check() == sat:
        found_options.append("A")
    solver.pop()
    
    # Test B: Exactly three Fuentes
    solver.push()
    solver.add(total_F == 3)
    if solver.check() == sat:
        found_options.append("B")
    solver.pop()
    
    # Test C: Exactly one Gagnon
    solver.push()
    solver.add(total_G == 1)
    if solver.check() == sat:
        found_options.append("C")
    solver.pop()
    
    # Test D: Exactly two Gagnon
    solver.push()
    solver.add(total_G == 2)
    if solver.check() == sat:
        found_options.append("D")
    solver.pop()
    
    # Test E: Exactly two Hue
    solver.push()
    solver.add(total_H == 2)
    if solver.check() == sat:
        found_options.append("E")
    solver.pop()
    
    print(f"Found options: {found_options}")
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
        
elif result == unsat:
    print("STATUS: unsat")
    print("Base constraints are unsatisfiable")
else:
    print("STATUS: unknown")