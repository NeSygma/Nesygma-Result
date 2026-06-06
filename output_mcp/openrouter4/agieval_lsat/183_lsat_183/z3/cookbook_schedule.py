from z3 import *

# Define Boolean variables: True = Fall, False = Spring
k, l, m, n, o, p = Bools('k l m n o p')

# Base constraints
def get_base_solver():
    solver = Solver()
    # 1. M and P cannot be same season
    solver.add(m != p)
    # 2. K and N must be same season
    solver.add(k == n)
    # 3. If K is fall, O must be fall
    solver.add(Implies(k, o))
    # 4. If M is fall, N must be spring
    solver.add(Implies(m, Not(n)))
    return solver

# Define option constraints
options = [
    ("A", And(k, Not(l))),  # K fall, L spring
    ("B", And(o, Not(p))),  # O fall, P spring
    ("C", And(p, Not(l))),  # P fall, L spring
    ("D", And(Not(k), Not(l))),  # Both K and L spring
    ("E", And(m, l)),  # Both M and L fall
]

found_unique = []
found_options = []

for letter, constr in options:
    solver = get_base_solver()
    solver.add(constr)
    
    # Check satisfiability
    result = solver.check()
    if result == sat:
        # Get the first model
        model = solver.model()
        # Build blocking clause: at least one variable different
        vars_list = [k, l, m, n, o, p]
        blocking = Or([v != model.eval(v) for v in vars_list])
        
        # Push to check uniqueness
        solver.push()
        solver.add(blocking)
        result2 = solver.check()
        solver.pop()
        
        if result2 == unsat:
            # Unique solution found
            found_unique.append(letter)
            found_options.append(letter)
        else:
            # Multiple solutions exist
            found_options.append(letter)
    else:
        # Option is impossible (unsat)
        pass

if len(found_unique) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unique[0]}")
elif len(found_unique) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple unique options found {found_unique}")
else:
    print("STATUS: unsat")
    print(f"Refine: No options found with unique determination. Options that were satisfiable: {found_options}")