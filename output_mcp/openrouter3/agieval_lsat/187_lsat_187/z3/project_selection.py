from z3 import *

# Create solver
solver = Solver()

# Define workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
worker_to_idx = {w: i for i, w in enumerate(workers)}
N = len(workers)

# Variables: selected[i] = True if worker i is selected as a project member
selected = [Bool(f"selected_{i}") for i in range(N)]

# Variables: leader[i] = True if worker i is the project leader
leader = [Bool(f"leader_{i}") for i in range(N)]

# Constraint 1: Exactly 3 workers are selected
solver.add(Sum([If(selected[i], 1, 0) for i in range(N)]) == 3)

# Constraint 2: Exactly 1 leader among selected workers
solver.add(Sum([If(leader[i], 1, 0) for i in range(N)]) == 1)

# Constraint 3: Leader must be among selected workers
for i in range(N):
    solver.add(Implies(leader[i], selected[i]))

# Constraint 4: Quinn or Ruiz can be a project member only if leading the project
# i.e., if selected, they must be the leader
quinn_idx = worker_to_idx["Quinn"]
ruiz_idx = worker_to_idx["Ruiz"]
solver.add(Implies(selected[quinn_idx], leader[quinn_idx]))
solver.add(Implies(selected[ruiz_idx], leader[ruiz_idx]))

# Constraint 5: If Smith is a project member, Taylor must also be
smith_idx = worker_to_idx["Smith"]
taylor_idx = worker_to_idx["Taylor"]
solver.add(Implies(selected[smith_idx], selected[taylor_idx]))

# Constraint 6: If Wells is a project member, neither Ruiz nor Verma can be
wells_idx = worker_to_idx["Wells"]
verma_idx = worker_to_idx["Verma"]
solver.add(Implies(selected[wells_idx], And(Not(selected[ruiz_idx]), Not(selected[verma_idx]))))

# Base constraint for the question: Verma could be the project leader
# This means we need to check if there exists a valid selection where Verma is the leader
base_constraint = leader[verma_idx]

# Now test each answer choice
found_options = []

# Option A: Neither Quinn nor Smith is selected
opt_a_constr = And(Not(selected[quinn_idx]), Not(selected[smith_idx]))

# Option B: Neither Ruiz nor Taylor is selected
opt_b_constr = And(Not(selected[ruiz_idx]), Not(selected[taylor_idx]))

# Option C: Neither Smith nor Taylor is selected
opt_c_constr = And(Not(selected[smith_idx]), Not(selected[taylor_idx]))

# Option D: Neither Smith nor Xue is selected
xue_idx = worker_to_idx["Xue"]
opt_d_constr = And(Not(selected[smith_idx]), Not(selected[xue_idx]))

# Option E: Neither Taylor nor Wells is selected
opt_e_constr = And(Not(selected[taylor_idx]), Not(selected[wells_idx]))

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(base_constraint)  # Verma is the leader
    solver.add(constr)  # Add the option constraint
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")