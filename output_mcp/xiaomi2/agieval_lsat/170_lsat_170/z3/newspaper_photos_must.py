from z3 import *

# For "must be true" questions, an option must hold in ALL valid configurations.
# Equivalently, Not(option) must be UNSATISFIABLE given the constraints.
# So we check: for each option, is (constraints AND Not(option)) unsat?

def check_must_be_true(opt_constr, letter):
    s = Solver()
    # Base constraints
    L_F, L_G, L_H = Ints('L_F L_G L_H')
    M_F, M_G, M_H = Ints('M_F M_G M_H')
    S_F, S_G, S_H = Ints('S_F S_G S_H')
    
    s.add(L_F + L_G + L_H == 2)
    s.add(M_F + M_G + M_H == 2)
    s.add(S_F + S_G + S_H == 2)
    for v in [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]:
        s.add(v >= 0)
    
    s.add(L_F + M_F + S_F >= 1, L_F + M_F + S_F <= 3)
    s.add(L_G + M_G + S_G >= 1, L_G + M_G + S_G <= 3)
    s.add(L_H + M_H + S_H >= 1, L_H + M_H + S_H <= 3)
    
    s.add(Or(And(L_F >= 1, M_F >= 1), And(L_G >= 1, M_G >= 1), And(L_H >= 1, M_H >= 1)))
    s.add(L_H == S_F)
    s.add(S_G == 0)
    
    # Additional condition: One Lifestyle photo by Gagnon, one by Hue
    s.add(L_G == 1, L_H == 1, L_F == 0)
    
    # Check if Not(option) is satisfiable
    s.add(Not(opt_constr))
    result = s.check()
    if result == unsat:
        return True  # Option must be true
    else:
        return False  # Option can be false

# Define options
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

options = [
    ("A", M_F == 1),           # Exactly one Metro photo by Fuentes
    ("B", M_G == 1),           # Exactly one Metro photo by Gagnon
    ("C", M_G == 2),           # Both Metro photos by Gagnon
    ("D", S_H == 1),           # Exactly one Sports photo by Hue
    ("E", S_H == 2),           # Both Sports photos by Hue
]

must_be_true = []
for letter, constr in options:
    if check_must_be_true(constr, letter):
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (negation is sat)")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")