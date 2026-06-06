from z3 import *

# Reps: Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall
# Zones: 1, 2, 3
# Each rep works in exactly one zone.

def solve():
    solver = Solver()
    
    # Variables: zone for each rep
    K, M, P, Q, S, T, U = Ints('K M P Q S T U')
    reps = [K, M, P, Q, S, T, U]
    
    for r in reps:
        solver.add(r >= 1, r <= 3)
        
    # 1. Either Parra or Tiao (but not both) works in Zone 1.
    solver.add(Xor(P == 1, T == 1))
    
    # 2. Either Tiao or Udall (but not both) works in Zone 2.
    solver.add(Xor(T == 2, U == 2))
    
    # 3. Parra and Quinn work in the same sales zone as each other.
    solver.add(P == Q)
    
    # 4. Stuckey and Udall work in the same sales zone as each other.
    solver.add(S == U)
    
    # 5. There are more of the sales representatives working in Zone 3 than in Zone 2.
    count_z2 = Sum([If(r == 2, 1, 0) for r in reps])
    count_z3 = Sum([If(r == 3, 1, 0) for r in reps])
    solver.add(count_z3 > count_z2)
    
    # Define options
    # (A) Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
    opt_a = And(K==1, P==1, S==2, U==2, M==3, Q==3, T==3)
    # (B) Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
    opt_b = And(K==1, T==1, S==2, U==2, M==3, P==3, Q==3)
    # (C) Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
    opt_c = And(P==1, Q==1, K==2, U==2, M==3, S==3, T==3)
    # (D) Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
    opt_d = And(S==1, U==1, K==2, T==2, M==3, P==3, Q==3)
    # (E) Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
    opt_e = And(T==1, K==2, P==2, Q==2, S==3, U==3)
    
    options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
    
    found_options = []
    for letter, constr in options:
        solver.push()
        solver.add(constr)
        if solver.check() == sat:
            found_options.append(letter)
        solver.pop()
        
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

solve()