from z3 import *

# Photographers: 0: Fuentes, 1: Gagnon, 2: Hue
# Sections: L (L1, L2), M (M1, M2), S (S1, S2)
# Total 6 photos, 2 per section.

def solve():
    solver = Solver()
    
    # Variables
    L1, L2 = Int('L1'), Int('L2')
    M1, M2 = Int('M1'), Int('M2')
    S1, S2 = Int('S1'), Int('S2')
    photos = [L1, L2, M1, M2, S1, S2]
    
    # Domain
    for p in photos:
        solver.add(p >= 0, p <= 2)
        
    # Constraint 1: Each photographer appears 1-3 times
    for ph in range(3):
        count = Sum([If(p == ph, 1, 0) for p in photos])
        solver.add(count >= 1, count <= 3)
        
    # Constraint 2: At least one photo in L is by a photographer who has at least one photo in M
    # Let SetL = {L1, L2}, SetM = {M1, M2}
    # Exists p in SetL s.t. p in SetM
    solver.add(Or(
        L1 == M1, L1 == M2,
        L2 == M1, L2 == M2
    ))
    
    # Constraint 3: Count(H in L) == Count(F in S)
    # H = 2, F = 0
    count_H_L = Sum([If(p == 2, 1, 0) for p in [L1, L2]])
    count_F_S = Sum([If(p == 0, 1, 0) for p in [S1, S2]])
    solver.add(count_H_L == count_F_S)
    
    # Constraint 4: None of Gagnon's (1) photos in S
    solver.add(S1 != 1, S2 != 1)
    
    # Question condition: Both photos in one section are by Gagnon (1)
    # Since G cannot be in S, it must be L or M.
    gagnon_in_L = And(L1 == 1, L2 == 1)
    gagnon_in_M = And(M1 == 1, M2 == 1)
    solver.add(Or(gagnon_in_L, gagnon_in_M))
    
    # Options
    options = [
        ("A", And(L1 == 2, L2 == 2)),
        ("B", Or(And(L1 == 0, L2 == 2), And(L1 == 2, L2 == 0))),
        ("C", And(M1 == 0, M2 == 0)),
        ("D", Or(And(M1 == 1, M2 == 2), And(M1 == 2, M2 == 1))),
        ("E", And(S1 == 2, S2 == 2))
    ]
    
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