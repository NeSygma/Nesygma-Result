from z3 import *

# Define worker indices
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
Q, R, S, T, V, W, X = range(7)

# Create Boolean variables for membership and leadership
member = [Bool(f"member_{i}") for i in range(7)]
leader = [Bool(f"leader_{i}") for i in range(7)]

solver = Solver()

# Base constraints
# 1. Exactly 3 members
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)

# 2. Exactly 1 leader among members
solver.add(Sum([If(leader[i], 1, 0) for i in range(7)]) == 1)
for i in range(7):
    solver.add(Implies(leader[i], member[i]))

# 3. Quinn or Ruiz can be a member only if leading
solver.add(Implies(member[Q], leader[Q]))
solver.add(Implies(member[R], leader[R]))

# 4. If Smith is a member, Taylor must also be
solver.add(Implies(member[S], member[T]))

# 5. If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(member[W], And(Not(member[R]), Not(member[V]))))

# Define option conditions
opt_a = And(Not(member[Q]), Not(member[S]))  # Neither Quinn nor Smith is selected
opt_b = And(Not(member[Q]), Not(member[T]))  # Neither Quinn nor Taylor is selected
opt_c = And(Not(member[Q]), Not(member[X]))  # Neither Quinn nor Xue is selected
opt_d = And(Not(member[R]), Not(member[W]))  # Neither Ruiz nor Wells is selected
opt_e = And(Not(member[R]), Not(member[V]))  # Neither Ruiz nor Verma is selected

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    
    # Check if solution becomes unique
    # We need to check if there's exactly one satisfying assignment
    # Strategy: find first solution, then block it and check if another exists
    if solver.check() == sat:
        # Get first solution
        m1 = solver.model()
        # Block this solution
        block_clause = Or([member[i] != m1[member[i]] for i in range(7)] + 
                         [leader[i] != m1[leader[i]] for i in range(7)])
        solver.add(block_clause)
        # Check if another solution exists
        if solver.check() == unsat:
            # Only one solution found
            found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")