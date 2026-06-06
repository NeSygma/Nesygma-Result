from z3 import *

# Students: 0:Grecia, 1:Hakeem, 2:Joe, 3:Katya, 4:Louise
# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
# Shifts: 0:1st, 1:2nd

def solve():
    solver = Solver()
    
    # work[day][shift]
    work = [[Int(f'work_{d}_{s}') for s in range(2)] for d in range(5)]
    
    # Domain constraints
    for d in range(5):
        for s in range(2):
            solver.add(work[d][s] >= 0, work[d][s] <= 4)
            
    # Each student works exactly 2 shifts
    for st in range(5):
        solver.add(Sum([If(work[d][s] == st, 1, 0) for d in range(5) for s in range(2)]) == 2)
        
    # No student works both shifts of any day
    for d in range(5):
        solver.add(work[d][0] != work[d][1])
        
    # Louise (4) works the 2nd shift on two consecutive days
    # Since she works exactly 2 shifts, these must be her only shifts.
    # So work[d][1] == 4 and work[d+1][1] == 4 for some d, and no other shifts for L.
    # Actually, the constraint is just "On two consecutive days, Louise works the second shift."
    # Let's encode: exists d in {0,1,2,3} s.t. work[d][1] == 4 and work[d+1][1] == 4
    l_consecutive = Or([And(work[d][1] == 4, work[d+1][1] == 4) for d in range(4)])
    solver.add(l_consecutive)
    
    # Grecia (0) works the 1st shift on two nonconsecutive days
    # exists d1, d2 s.t. d2 > d1 + 1 and work[d1][0] == 0 and work[d2][0] == 0
    g_nonconsecutive = Or([And(work[d1][0] == 0, work[d2][0] == 0) for d1 in range(5) for d2 in range(d1 + 2, 5)])
    solver.add(g_nonconsecutive)
    
    # Katya (3) works on Tuesday (d=1) and Friday (d=4)
    # K works on Tuesday: work[1][0] == 3 or work[1][1] == 3
    # K works on Friday: work[4][0] == 3 or work[4][1] == 3
    solver.add(Or(work[1][0] == 3, work[1][1] == 3))
    solver.add(Or(work[4][0] == 3, work[4][1] == 3))
    
    # Hakeem (1) and Joe (2) work on the same day at least once
    h_j_same_day = Or([Or(And(work[d][0] == 1, work[d][1] == 2), And(work[d][0] == 2, work[d][1] == 1)) for d in range(5)])
    solver.add(h_j_same_day)
    
    # Grecia (0) and Louise (4) never work on the same day
    for d in range(5):
        g_works_d = Or(work[d][0] == 0, work[d][1] == 0)
        l_works_d = Or(work[d][0] == 4, work[d][1] == 4)
        solver.add(Not(And(g_works_d, l_works_d)))
        
    # Answer choices for second shifts (S2)
    # 0:Grecia, 1:Hakeem, 2:Joe, 3:Katya, 4:Louise
    # (A) Hakeem, Louise, Louise, Hakeem, Katya -> 1, 4, 4, 1, 3
    # (B) Joe, Hakeem, Grecia, Louise, Louise -> 2, 1, 0, 4, 4
    # (C) Joe, Katya, Hakeem, Louise, Katya -> 2, 3, 1, 4, 3
    # (D) Louise, Katya, Joe, Louise, Katya -> 4, 3, 2, 4, 3
    # (E) Louise, Louise, Hakeem, Joe, Joe -> 4, 4, 1, 2, 2
    
    options = [
        ("A", [1, 4, 4, 1, 3]),
        ("B", [2, 1, 0, 4, 4]),
        ("C", [2, 3, 1, 4, 3]),
        ("D", [4, 3, 2, 4, 3]),
        ("E", [4, 4, 1, 2, 2])
    ]
    
    found_options = []
    for letter, s2_list in options:
        solver.push()
        for d in range(5):
            solver.add(work[d][1] == s2_list[d])
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