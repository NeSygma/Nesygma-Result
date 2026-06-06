from z3 import *

# Create integer variables for each employee's parking space
R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

# Base constraints
base_constraints = [
    # Domain: each space 1-6
    R >= 1, R <= 6,
    S >= 1, S <= 6,
    T >= 1, T <= 6,
    V >= 1, V <= 6,
    X >= 1, X <= 6,
    Y >= 1, Y <= 6,
    # All distinct
    Distinct(R, S, T, V, X, Y),
    # Young > Togowa
    Y > T,
    # Xu > Souza
    X > S,
    # Robertson > Young
    R > Y,
    # Robertson must be #1, #2, #3, or #4
    Or(R == 1, R == 2, R == 3, R == 4)
]

# Options
options = {
    "A": S == 1,  # Souza is space #1
    "B": Y == 2,  # Young is space #2
    "C": V == 3,  # Vaughn is space #3
    "D": R == 4,  # Robertson is space #4
    "E": X == 5   # Xu is space #5
}

def is_uniquely_determined(opt_constraint):
    s = Solver()
    s.add(base_constraints)
    s.add(opt_constraint)
    
    result = s.check()
    if result != sat:
        return False  # No solution
    
    m = s.model()
    # Get the first solution values
    first_sol = {emp: m.eval(emp, model_completion=True) for emp in employees}
    
    # Block this exact solution
    block = Or([emp != first_sol[emp] for emp in employees])
    s.add(block)
    
    # Check if there's another solution
    result2 = s.check()
    return result2 == unsat  # Uniquely determined if no other solution

found_options = []
for letter, constr in options.items():
    if is_uniquely_determined(constr):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")