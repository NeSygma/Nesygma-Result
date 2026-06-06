from z3 import *

solver = Solver()

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# We'll assign each an integer from 1 to 6 (parking space number)
R, S, T, V, X, Y = Ints('R S T V X Y')

# Domain: each must be 1..6
employees = [R, S, T, V, X, Y]
for e in employees:
    solver.add(e >= 1, e <= 6)

# All distinct
solver.add(Distinct(employees))

# Constraints:
# Young > Togowa
solver.add(Y > T)
# Xu > Souza
solver.add(X > S)
# Robertson > Young
solver.add(R > Y)
# Robertson must be 1,2,3, or 4
solver.add(Or([R == i for i in [1,2,3,4]]))

# Now evaluate each option: if adding that option as an additional constraint
# results in exactly one unique solution (fully determined), that's the answer.
# "Fully and uniquely determined" means that for every employee, there is exactly
# one possible parking space. So we need to check that with the option added,
# the solution is unique. We can check uniqueness by finding one solution,
# then blocking it and checking if another exists.

def is_unique_determination(extra_constraint):
    """Returns True if adding extra_constraint yields exactly one solution."""
    s = Solver()
    # Add all base constraints
    for e in employees:
        s.add(e >= 1, e <= 6)
    s.add(Distinct(employees))
    s.add(Y > T)
    s.add(X > S)
    s.add(R > Y)
    s.add(Or([R == i for i in [1,2,3,4]]))
    # Add the extra constraint
    s.add(extra_constraint)
    
    # Check first solution
    result = s.check()
    if result != sat:
        return False
    m = s.model()
    # Block this solution
    s.add(Or([e != m.eval(e) for e in employees]))
    # Check if another solution exists
    if s.check() == sat:
        return False  # More than one solution
    else:
        return True  # Exactly one solution

# Define each option's constraint
opt_a = (S == 1)
opt_b = (Y == 2)
opt_c = (V == 3)
opt_d = (R == 4)
opt_e = (X == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    if is_unique_determination(constr):
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