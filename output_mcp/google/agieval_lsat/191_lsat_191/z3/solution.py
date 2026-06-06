from z3 import *

# Students: L=0, M=1, O=2, R=3, T=4, Y=5
# Years: 0=1921, 1=1922, 2=1923, 3=1924

def solve():
    solver = Solver()
    
    year_to_student = [Int(f'year_to_student_{y}') for y in range(4)]
    is_assigned = [Bool(f'is_assigned_{s}') for s in range(6)]
    
    for y in range(4):
        solver.add(year_to_student[y] >= 0, year_to_student[y] < 6)
    
    for s in range(6):
        solver.add(is_assigned[s] == Or([year_to_student[y] == s for y in range(4)]))
        
    solver.add(Sum([If(is_assigned[s], 1, 0) for s in range(6)]) == 4)
    
    for y1 in range(4):
        for y2 in range(y1 + 1, 4):
            solver.add(year_to_student[y1] != year_to_student[y2])
            
    solver.add(Or(year_to_student[2] == 0, year_to_student[2] == 4))
    solver.add(Implies(is_assigned[1], Or(year_to_student[0] == 1, year_to_student[1] == 1)))
    solver.add(Implies(is_assigned[4], is_assigned[3]))
    solver.add(Implies(is_assigned[3], year_to_student[0] != 3))
    for y in range(1, 4):
        solver.add(Implies(year_to_student[y] == 3, year_to_student[y-1] == 2))
        
    options = [
        ("A", year_to_student[3] == 0),
        ("B", year_to_student[0] == 2),
        ("C", year_to_student[3] == 2),
        ("D", year_to_student[2] == 4),
        ("E", year_to_student[0] == 5)
    ]
    
    found_options = []
    for label, opt_constr in options:
        solver.push()
        solver.add(opt_constr)
        # Check if (Constraints AND Option) -> (Mollie is in 1922)
        # Equivalent to: (Constraints AND Option AND Mollie is NOT in 1922) is UNSAT
        solver.add(year_to_student[1] != 1)
        if solver.check() == unsat:
            found_options.append(label)
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