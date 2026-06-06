from z3 import *

# Define the problem constraints
def check_options():
    solver = Solver()
    
    # Employees: Robertson(R), Souza(S), Togowa(T), Vaughn(V), Xu(X), Young(Y)
    # Spaces: 1, 2, 3, 4, 5, 6
    R, S, T, V, X, Y = Ints('R S T V X Y')
    employees = [R, S, T, V, X, Y]
    
    # Each space is 1-6
    for e in employees:
        solver.add(e >= 1, e <= 6)
        
    # All distinct
    solver.add(Distinct(employees))
    
    # Rules
    solver.add(Y > T)
    solver.add(X > S)
    solver.add(R > Y)
    solver.add(Or(R == 1, R == 2, R == 3, R == 4))
    
    # Options
    options = [
        ("A", S == 1),
        ("B", Y == 2),
        ("C", V == 3),
        ("D", R == 4),
        ("E", X == 5)
    ]
    
    found_options = []
    for letter, constr in options:
        solver.push()
        solver.add(constr)
        
        # Count solutions for this option
        count = 0
        while solver.check() == sat:
            count += 1
            m = solver.model()
            # Block this solution
            solver.add(Or([e != m[e] for e in employees]))
            if count > 1: break
            
        if count == 1:
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

check_options()