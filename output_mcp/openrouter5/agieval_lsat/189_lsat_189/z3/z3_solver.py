from z3 import *

# Seven workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
Q, R, S, T, V, W, X = 0, 1, 2, 3, 4, 5, 6

def count_solutions(extra_constraints):
    """Count the number of complete assignments (member + leader) satisfying all constraints."""
    solver = Solver()
    
    member = [Bool(f"member_{w}") for w in workers]
    leader = [Bool(f"leader_{w}") for w in workers]
    
    # Exactly three project members
    solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)
    
    # Exactly one project leader
    solver.add(Sum([If(leader[i], 1, 0) for i in range(7)]) == 1)
    
    # The leader must be a project member
    for i in range(7):
        solver.add(Implies(leader[i], member[i]))
    
    # Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
    solver.add(Implies(member[Q], leader[Q]))
    solver.add(Implies(member[R], leader[R]))
    
    # Constraint 2: If Smith is a project member, Taylor must also be.
    solver.add(Implies(member[S], member[T]))
    
    # Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
    solver.add(Implies(member[W], Not(member[R])))
    solver.add(Implies(member[W], Not(member[V])))
    
    # Add extra constraints for this option
    for c in extra_constraints:
        solver.add(c)
    
    # Enumerate all solutions
    solutions = []
    decision_vars = member + leader
    
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(v, model_completion=True) for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    
    return len(solutions)

# Evaluate each option
# We need to define member/leader variables for the options list
# Let's define them inside a function that returns the constraints

def get_option_constraints(letter):
    member = [Bool(f"member_{w}") for w in workers]
    if letter == "A":
        return [Not(member[Q]), Not(member[S])]
    elif letter == "B":
        return [Not(member[Q]), Not(member[T])]
    elif letter == "C":
        return [Not(member[Q]), Not(member[X])]
    elif letter == "D":
        return [Not(member[R]), Not(member[W])]
    elif letter == "E":
        return [Not(member[R]), Not(member[V])]

found_options = []

for letter in ["A", "B", "C", "D", "E"]:
    constr = get_option_constraints(letter)
    count = count_solutions(constr)
    print(f"Option {letter}: {count} solution(s)")
    if count == 1:
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