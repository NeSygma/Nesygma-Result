from z3 import *

K_fall, L_fall, M_fall, N_fall, O_fall, P_fall = Bools('K_fall L_fall M_fall N_fall O_fall P_fall')
all_vars = [K_fall, L_fall, M_fall, N_fall, O_fall, P_fall]

def find_all_solutions(extra_constraints, label):
    s = Solver()
    # Base constraints
    s.add(M_fall != P_fall)
    s.add(K_fall == N_fall)
    s.add(Implies(K_fall, O_fall))
    s.add(Implies(M_fall, Not(N_fall)))
    s.add(extra_constraints)
    
    count = 0
    while s.check() == sat:
        count += 1
        m = s.model()
        vals = {str(v): m.eval(v, model_completion=True) for v in all_vars}
        print(f"  Solution {count}: K={vals['K_fall']}, L={vals['L_fall']}, M={vals['M_fall']}, N={vals['N_fall']}, O={vals['O_fall']}, P={vals['P_fall']}")
        # Block this exact assignment
        s.add(Or([v != m.eval(v, model_completion=True) for v in all_vars]))
    print(f"  Total: {count} solution(s)")

print("Option B: O fall, P spring")
find_all_solutions(And(O_fall == True, P_fall == False), "B")