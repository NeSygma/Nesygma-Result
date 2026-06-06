from z3 import *

# Define the workers
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
worker_to_idx = {w: i for i, w in enumerate(workers)}
N = len(workers)

# Create symbolic variables
# is_member[i] = True if worker i is a project member
is_member = [Bool(f"is_member_{i}") for i in range(N)]
# is_leader[i] = True if worker i is the project leader
is_leader = [Bool(f"is_leader_{i}") for i in range(N)]

solver = Solver()

# Constraint 1: Exactly 3 members
solver.add(Sum([If(is_member[i], 1, 0) for i in range(N)]) == 3)

# Constraint 2: Exactly 1 leader
solver.add(Sum([If(is_leader[i], 1, 0) for i in range(N)]) == 1)

# Constraint 3: Leader must be a member
for i in range(N):
    solver.add(Implies(is_leader[i], is_member[i]))

# Constraint 4: Quinn or Ruiz can be a project member only if leading the project
# This means: If Quinn is a member, then Quinn must be leader
# Similarly for Ruiz
quinn_idx = worker_to_idx["Quinn"]
ruiz_idx = worker_to_idx["Ruiz"]
solver.add(Implies(is_member[quinn_idx], is_leader[quinn_idx]))
solver.add(Implies(is_member[ruiz_idx], is_leader[ruiz_idx]))

# Constraint 5: If Smith is a project member, Taylor must also be
smith_idx = worker_to_idx["Smith"]
taylor_idx = worker_to_idx["Taylor"]
solver.add(Implies(is_member[smith_idx], is_member[taylor_idx]))

# Constraint 6: If Wells is a project member, neither Ruiz nor Verma can be
wells_idx = worker_to_idx["Wells"]
verma_idx = worker_to_idx["Verma"]
solver.add(Implies(is_member[wells_idx], And(Not(is_member[ruiz_idx]), Not(is_member[verma_idx]))))

# Now evaluate each option
# Option A: Ruiz (leader), Taylor, Wells
opt_a = And(
    is_leader[ruiz_idx], is_member[ruiz_idx],
    is_member[taylor_idx],
    is_member[wells_idx],
    Not(is_member[quinn_idx]),
    Not(is_member[smith_idx]),
    Not(is_member[verma_idx]),
    Not(is_member[xue_idx])
)

# Option B: Verma (leader), Quinn, Taylor
opt_b = And(
    is_leader[verma_idx], is_member[verma_idx],
    is_member[quinn_idx],
    is_member[taylor_idx],
    Not(is_member[ruiz_idx]),
    Not(is_member[smith_idx]),
    Not(is_member[wells_idx]),
    Not(is_member[xue_idx])
)

# Option C: Verma (leader), Smith, Taylor
opt_c = And(
    is_leader[verma_idx], is_member[verma_idx],
    is_member[smith_idx],
    is_member[taylor_idx],
    Not(is_member[quinn_idx]),
    Not(is_member[ruiz_idx]),
    Not(is_member[wells_idx]),
    Not(is_member[xue_idx])
)

# Option D: Verma (leader), Smith, Xue
opt_d = And(
    is_leader[verma_idx], is_member[verma_idx],
    is_member[smith_idx],
    is_member[xue_idx],
    Not(is_member[quinn_idx]),
    Not(is_member[ruiz_idx]),
    Not(is_member[taylor_idx]),
    Not(is_member[wells_idx])
)

# Option E: Xue (leader), Verma, Wells
xue_idx = worker_to_idx["Xue"]
opt_e = And(
    is_leader[xue_idx], is_member[xue_idx],
    is_member[verma_idx],
    is_member[wells_idx],
    Not(is_member[quinn_idx]),
    Not(is_member[ruiz_idx]),
    Not(is_member[smith_idx]),
    Not(is_member[taylor_idx])
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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