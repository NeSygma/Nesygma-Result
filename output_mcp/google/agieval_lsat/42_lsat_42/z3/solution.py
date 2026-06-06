from z3 import *

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Batches: O1, O2, O3, P1, P2, P3, S1, S2, S3
# Each batch is a day (0-4)

def solve():
    solver = Solver()
    
    # Variables
    O = [Int(f'O{i}') for i in range(1, 4)]
    P = [Int(f'P{i}') for i in range(1, 4)]
    S = [Int(f'S{i}') for i in range(1, 4)]
    all_batches = O + P + S
    
    # Domain constraints
    for b in all_batches:
        solver.add(b >= 0, b <= 4)
        
    # No two batches of the same kind on the same day
    solver.add(Distinct(O))
    solver.add(Distinct(P))
    solver.add(Distinct(S))
    
    # At least one batch on Monday (day 0)
    solver.add(Or([b == 0 for b in all_batches]))
    
    # O2 = P1
    solver.add(O[1] == P[0])
    
    # S2 = Thursday (day 3)
    solver.add(S[1] == 3)
    
    # "If one kind of cookie's first batch is made on the same day as another kind of cookie's third batch"
    # Condition I: (O1 == P3) or (O1 == S3) or (P1 == O3) or (P1 == S3) or (S1 == O3) or (S1 == P3)
    I = Or(O[0] == P[2], O[0] == S[2], P[0] == O[2], P[0] == S[2], S[0] == O[2], S[0] == P[2])
    solver.add(I)
    
    # Options
    # (A) At least one batch of cookies is made on each of the five days.
    # (B) At least two batches of cookies are made on Wednesday.
    # (C) Exactly one batch of cookies is made on Monday.
    # (D) Exactly two batches of cookies are made on Tuesday.
    # (E) Exactly one batch of cookies is made on Friday.
    
    def count_on_day(day):
        return Sum([If(b == day, 1, 0) for b in all_batches])
    
    opt_a = And([count_on_day(d) >= 1 for d in range(5)])
    opt_b = count_on_day(2) >= 2
    opt_c = count_on_day(0) == 1
    opt_d = count_on_day(1) == 2
    opt_e = count_on_day(4) == 1
    
    options = [
        ("A", opt_a),
        ("B", opt_b),
        ("C", opt_c),
        ("D", opt_d),
        ("E", opt_e)
    ]
    
    # We want to find which option could be false.
    # An option X could be false if (Constraints + I + Not(X)) is satisfiable.
    
    found_options = []
    for letter, constr in options:
        solver.push()
        solver.add(Not(constr))
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