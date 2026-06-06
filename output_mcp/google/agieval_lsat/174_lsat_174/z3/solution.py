from z3 import *

# Sections: L, M, S
# Photographers: F=0, G=1, H=2
# 2 photos per section
# Total 6 photos

def solve():
    solver = Solver()
    
    # Variables: P[section][photo_index]
    # Sections: 0:L, 1:M, 2:S
    P = [[Int(f"P_{s}_{j}") for j in range(2)] for s in range(3)]
    
    # Domain: 0, 1, 2
    for s in range(3):
        for j in range(2):
            solver.add(P[s][j] >= 0, P[s][j] <= 2)
            
    # Constraint: Each photographer has at least 1 and at most 3 photos
    for p in range(3):
        count = Sum([If(P[s][j] == p, 1, 0) for s in range(3) for j in range(2)])
        solver.add(count >= 1, count <= 3)
        
    # Constraint: None of Gagnon's (1) photos in Sports (2)
    for j in range(2):
        solver.add(P[2][j] != 1)
        
    # Constraint: Count(H in L) == Count(F in S)
    h_in_l = Sum([If(P[0][j] == 2, 1, 0) for j in range(2)])
    f_in_s = Sum([If(P[2][j] == 0, 1, 0) for j in range(2)])
    solver.add(h_in_l == f_in_s)
    
    # Constraint: At least one photo in L must be by a photographer who has at least one photo in M
    # Photographers in M:
    m_photographers = [P[1][0], P[1][1]]
    # At least one photo in L (P[0][0] or P[0][1]) must be in m_photographers
    solver.add(Or(
        Or([P[0][0] == m_photographers[k] for k in range(2)]),
        Or([P[0][1] == m_photographers[k] for k in range(2)])
    ))
    
    # Question condition: M has 1 F (0) and 1 H (2)
    solver.add(Or(
        And(P[1][0] == 0, P[1][1] == 2),
        And(P[1][0] == 2, P[1][1] == 0)
    ))
    
    # Options
    options = [
        ("A", And(P[0][0] == 0, P[0][1] == 0)),
        ("B", And(P[0][0] == 1, P[0][1] == 1)),
        ("C", Or(And(P[0][0] == 1, P[0][1] == 2), And(P[0][0] == 2, P[0][1] == 1))),
        ("D", And(P[0][0] == 2, P[0][1] == 2)),
        ("E", And(P[2][0] == 0, P[2][1] == 0))
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