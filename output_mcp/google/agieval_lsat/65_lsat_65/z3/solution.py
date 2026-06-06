from z3 import *

# Riders: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Bikes: 0:F, 1:G, 2:H, 3:J

def solve():
    solver = Solver()
    
    # Variables: test[rider][day]
    # rider: 0..3, day: 0..1
    test = [[Int(f'test_{r}_{d}') for d in range(2)] for r in range(4)]
    
    # Domain constraints
    for r in range(4):
        for d in range(2):
            solver.add(test[r][d] >= 0, test[r][d] <= 3)
            
    # Each rider tests a different bike on the second day
    for r in range(4):
        solver.add(test[r][0] != test[r][1])
        
    # All four bikes are tested each day
    for d in range(2):
        solver.add(Distinct([test[r][d] for r in range(4)]))
        
    # Reynaldo cannot test F (0)
    solver.add(test[0][0] != 0, test[0][1] != 0)
    
    # Yuki cannot test J (3)
    solver.add(test[3][0] != 3, test[3][1] != 3)
    
    # Theresa must be one of the testers for H (2)
    solver.add(Or(test[2][0] == 2, test[2][1] == 2))
    
    # The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
    solver.add(test[3][0] == test[1][1])
    
    # Define options
    # (A) Both Reynaldo and Seamus test J (3)
    opt_a = And(Or(test[0][0] == 3, test[0][1] == 3), Or(test[1][0] == 3, test[1][1] == 3))
    # (B) Both Reynaldo and Theresa test J (3)
    opt_b = And(Or(test[0][0] == 3, test[0][1] == 3), Or(test[2][0] == 3, test[2][1] == 3))
    # (C) Both Reynaldo and Yuki test G (1)
    opt_c = And(Or(test[0][0] == 1, test[0][1] == 1), Or(test[3][0] == 1, test[3][1] == 1))
    # (D) Both Seamus and Theresa test G (1)
    opt_d = And(Or(test[1][0] == 1, test[1][1] == 1), Or(test[2][0] == 1, test[2][1] == 1))
    # (E) Both Theresa and Yuki test F (0)
    opt_e = And(Or(test[2][0] == 0, test[2][1] == 0), Or(test[3][0] == 0, test[3][1] == 0))
    
    options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
    
    found_options = []
    for letter, constr in options:
        solver.push()
        solver.add(constr)
        if solver.check() == sat:
            # This option CAN be true
            pass
        else:
            # This option CANNOT be true
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