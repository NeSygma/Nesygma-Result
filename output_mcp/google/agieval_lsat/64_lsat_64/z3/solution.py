from z3 import *

# Riders: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Bikes: 0:F, 1:G, 2:H, 3:J

def solve():
    solver = Solver()
    
    R1 = [Int(f'R1_{i}') for i in range(4)]
    R2 = [Int(f'R2_{i}') for i in range(4)]
    
    # Domain constraints
    for i in range(4):
        solver.add(R1[i] >= 0, R1[i] <= 3)
        solver.add(R2[i] >= 0, R2[i] <= 3)
        
    # All bikes tested each day
    solver.add(Distinct(R1))
    solver.add(Distinct(R2))
    
    # Reynaldo cannot test F (0)
    solver.add(R1[0] != 0)
    solver.add(R2[0] != 0)
    
    # Yuki cannot test J (3)
    solver.add(R1[3] != 3)
    solver.add(R2[3] != 3)
    
    # Theresa must test H (2) on one of the two days
    solver.add(Or(R1[2] == 2, R2[2] == 2))
    
    # Yuki's Day 1 bike = Seamus's Day 2 bike
    solver.add(R1[3] == R2[1])
    
    # Condition: Theresa tests J (3) on the first day
    solver.add(R1[2] == 3)
    
    # Options
    # (A) Reynaldo tests G (1) on the second day: R2[0] == 1
    # (B) Seamus tests H (2) on the first day: R1[1] == 2
    # (C) Yuki tests H (2) on the second day: R2[3] == 2
    # (D) Seamus is one of the testers for J (3): R1[1] == 3 or R2[1] == 3
    # (E) Theresa is one of the testers for G (1): R1[2] == 1 or R2[2] == 1
    
    options = [
        ("A", R2[0] == 1),
        ("B", R1[1] == 2),
        ("C", R2[3] == 2),
        ("D", Or(R1[1] == 3, R2[1] == 3)),
        ("E", Or(R1[2] == 1, R2[2] == 1))
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