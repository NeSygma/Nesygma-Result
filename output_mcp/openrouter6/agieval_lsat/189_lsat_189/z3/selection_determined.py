from z3 import *

# Define workers and indices
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
n = len(workers)

# Symbolic variables
member = [Bool(f"member_{i}") for i in range(n)]
leader = [Bool(f"leader_{i}") for i in range(n)]

# Base constraints
solver = Solver()

# Exactly three members
solver.add(Sum(member) == 3)

# Exactly one leader
solver.add(Sum(leader) == 1)

# Leader must be a member
for i in range(n):
    solver.add(Implies(leader[i], member[i]))

# Quinn or Ruiz can be member only if leader (indices 0 and 1)
for i in [0, 1]:
    solver.add(Implies(member[i], leader[i]))

# If Smith (2) is member, Taylor (3) must be member
solver.add(Implies(member[2], member[3]))

# If Wells (4) is member, then Ruiz (1) and Verma (5) are not members
solver.add(Implies(member[4], And(Not(member[1]), Not(member[5]))))

# Options
opt_a = And(Not(member[0]), Not(member[2]))  # Neither Quinn nor Smith
opt_b = And(Not(member[0]), Not(member[3]))  # Neither Quinn nor Taylor
opt_c = And(Not(member[0]), Not(member[6]))  # Neither Quinn nor Xue
opt_d = And(Not(member[1]), Not(member[4]))  # Neither Ruiz nor Wells
opt_e = And(Not(member[1]), Not(member[5]))  # Neither Ruiz nor Verma

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []

for letter, constr in options:
    solver.push()
    solver.add(constr)
    
    # Count solutions by enumerating all models
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        # Capture the assignment of members and leader as a tuple of bools
        mem_assign = tuple(m.eval(member[i], model_completion=True) for i in range(n))
        lead_assign = tuple(m.eval(leader[i], model_completion=True) for i in range(n))
        sol = (mem_assign, lead_assign)
        solutions.append(sol)
        # Block this exact assignment
        block = Or([member[i] != m.eval(member[i], model_completion=True) for i in range(n)] +
                   [leader[i] != m.eval(leader[i], model_completion=True) for i in range(n)])
        solver.add(block)
    
    solver.pop()
    
    if len(solutions) == 1:
        found_options.append(letter)

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")